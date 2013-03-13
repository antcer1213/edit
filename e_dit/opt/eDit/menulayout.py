#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
import evas
import edje
import ecore
import dexml
from dexml import fields


"""eDit

An lxde/e17 menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""

HOME = os.getenv("HOME")
local = "%s/.config/menus/" %HOME
system = "/etc/xdg/menus/"



class MenuLayout(object):
    def __init__(self, tb=False, tbi=False, win=False, vbox=False):

#----Main Window
        if vbox:
            vbox.delete()

        self.win = win

        self.vipbox()

    def vipbox(self):
        from edit import Launchers
        from menuitem import MenuItem


        vbox = self.vbox = elm.Box(self.win)
        vbox.padding_set(5, 0)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Launcher View", Launchers, self.win, vbox)
        tb.item_append("", "Menu View")
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Item View", MenuItem, self.win, vbox)
        tb.item_append("", "Layout View")
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.separator(vbox)
        self.gl(None, None, vbox)
        self.add_files(self.maingl, None, local)
        self.separator(vbox)

        item = "None"
        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Add", self.system_launcher)
        tb.item_append("", "Edit", self.editor, vbox)
        tb.item_append("", "Create", self.editor_core, vbox)
        tb.item_append("", "Remove", self.rm_popup)
        tb.item_append("", "Refresh", self.gl, vbox)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.win.resize_object_add(vbox)
        self.win.resize(410, 460)
        self.win.show()

    def gl(self, tb=False, tbi=False, vbox=False):
        if tb:
            self.maingl.clear()
            self.add_files(self.maingl, None, local)
        else:
            gl = self.maingl = elm.Genlist(self.win)
            gl.size_hint_weight_set(1.0, 1.0)
            gl.size_hint_align_set(-1.0, -1.0)
            gl.bounce_set(False, True)
            gl.callback_clicked_double_add(self.dubclick)
            gl.multi_select_set(False)
            gl.show()
            vbox.pack_end(gl)

#-----Crucial
    def add_files(self, gl, bt= None, fil=None ):
        if fil:
            if not os.path.isdir(fil):
                data = {};data['fullpath'] = fil
                split = fil.split("/")
                fil = os.path.basename(fil);fil = os.path.splitext(fil)[0]
                data['name'] = fil
                self.add_file(gl, data)
                return
            else:
                files = os.listdir(fil)
                for f in files:
                    if not f.endswith('.menu'):
                        files.remove(f)
                if files == []:
                    return
                files.sort()
                for f in files:
                    if fil == system:
                        f = system + f
                    else:
                        f = local + f
                    self.add_files(gl, False, f)

    def add_file(self, gl, data ):
        itc = elm.GenlistItemClass(item_style="default", text_get_func=self.name_return, content_get_func=self.icon_return)

        gl.item_append(itc, data, None)

    def add_group(self, gl, data ):
        itc = elm.GenlistItemClass(item_style="default", text_get_func=self.name_return, content_get_func=self.icon_return)

        gl.item_append(itc, data, None)

    def get_name(self, path, item=False):
        split = path.split("/")
        path = os.path.basename(path)
        path = os.path.splitext(path)[0]

        if not item:
            if "-" in path:
                name = path.replace("-", " ")
            else:
                name = path
            name = name.title()
        else:
            name = path

        return name

    def name_return(self, obj, part, data ):
        path = data["fullpath"]
        label = ""
        label = self.get_name(path)
        return label

    def icon_return(self, obj, part, data ):
        if part == "elm.swallow.icon":
            path = data['fullpath']
            f = elm.Box(self.win)
            f.horizontal_set(True)
            f.show()
            sep = elm.Separator(self.win)
            sep.show()

            ic = elm.Icon(self.win)
            ic.standard_set("text-xml")
            ic.size_hint_weight_set(1.0, 1.0)
            ic.size_hint_align_set(-1.0, -1.0)
            ic.show()

            f.pack_end(ic)
            f.pack_end(sep)

            return f

    def sys_cb(self, tb=False, tbi=False):
        item = self.sysgl.selected_item_get()
        if item:
            num = '0123456789'
            path = item.data["fullpath"]
            name = item.data["name"]
            copy = name[:]
            for x in num:
                name.strip('-0123456789')
                name = name + "-" + x
                newpath = "%s%s.menu" %(local, name)
                if not os.path.exists(newpath):
                    ecore.Exe("cp '%s' '%s'" %(path, newpath))
                    ecore.Timer(0.3, self.add_files, self.maingl, None, newpath)
                    break
                else:
                    name = copy

#-----------INNER WINDOWS
    def editor(self, tb, tbi, vbox):
        item = self.maingl.selected_item_get()
        if item:
            self.editor_core(tb, tbi, vbox, item)

    def system_launcher(self, tb, bt):
        obt = bt
        obt.disabled_set(True)

        vbox = elm.Box(self.win)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        gl = self.sysgl = elm.Genlist(self.win)
        gl.size_hint_weight_set(1.0, 1.0)
        gl.size_hint_align_set(-1.0, -1.0)
        gl.callback_clicked_double_add(self.dubclick)
        gl.bounce_set(False, True)
        gl.multi_select_set(False)
        gl.show()
        vbox.pack_end(gl)

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Add", self.sys_cb)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        iw = elm.InnerWindow(self.win)
        iw.content = vbox
        iw.show()
        iw.activate()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Close", self.iwin_close, obt, iw)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.add_files(gl, None, system)

    def editor_core(self, tb=None, tbi=None, vbox=None, item=None, n=None):
        def new():
            num = '0123456789'
            dest = "%snew" %local
            copy = dest[:]
            for x in num:
                dest.strip('-0123456789')
                dest = dest + "-" + x
                newpath = "%s.menu" %dest
                if not os.path.exists(newpath):
                    ecore.Exe("cp '/opt/eDit/new.menu' '%s'" %newpath)
                    break
                else:
                    dest = copy
            return newpath

        if n:
            self.n.delete()
        if item:
            if type(item) is unicode or type(item) is str:
                path = self.path = item
                item = 1
                pathname = self.get_name(path, item)
            else:
                path = self.path = item.data['fullpath']
                pathname = item.data['name']
        else:
            n = self.n = elm.Notify(self.win)
            n.orient = 1
            n.allow_events_set(False)
            n.show()
            path = new()
            ecore.Timer(1.0, self.editor_core, None, None, vbox, path, n)
            return

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 460)
        vbox.padding_set(2, 2)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        fr = elm.Frame(self.win)
        fr.text = "File Name(no suffix):"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.dtfp = elm.Entry(self.win)
        en.size_hint_weight_set(1.0, 1.0)
        en.text = pathname
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        fr = elm.Frame(self.win)
        fr.text = "Content:"
        fr.size_hint_weight_set(1.0, 1.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        sc = elm.Scroller(self.win)
        sc.size_hint_align_set(-1.0, -1.0)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.policy_set(True, True)
        fr.content_set(sc)
        sc.show()

        man = self.man = elm.Entry(self.win)
        man.line_wrap_set(0)
        man.autosave_set(False)
        man.file_set(path, 0)
        man.size_hint_align_set(-1.0, -1.0)
        man.size_hint_weight_set(1.0, 1.0)
        sc.content_set(man)
        man.editable_set(True)
        man.scrollable_set(False)
        man.show()

        btnb = elm.Box(self.win)
        btnb.horizontal_set(True)
        btnb.size_hint_weight_set(1.0, 0.0)
        vbox.pack_end(btnb)
        btnb.show()

        if item:
            val = 1
            bt = elm.Button(self.win)
            bt.size_hint_weight_set(1.0, 1.0)
            bt.text_set("Save")
            bt.callback_clicked_add(self.editor_save, None, vbox, val)
            btnb.pack_end(bt)
            bt.show()

        bt = elm.Button(self.win)
        bt.size_hint_weight_set(1.0, 1.0)
        bt.text_set("Manual")
        if item:
            bt.callback_clicked_add(self.manual_win, path, vbox, item)
        else:
            bt.callback_clicked_add(self.manual_win, path, vbox)
        btnb.pack_end(bt)
        bt.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        if item:
            tb.item_append("", "Done", self.editor_save, vbox)
        else:
            tb.item_append("", "Create", self.creator_create, vbox, dest)
        if item:
            tb.item_append("", "Cancel", self.editor_close, vbox)
        else:
            tb.item_append("", "Cancel", self.creator_close, vbox, dest)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

#---------POPUPS
    def rm_popup(self, tb, bt):
        if self.maingl.selected_item_get():
            popup = self.rmp = elm.Popup(self.win)
            popup.size_hint_weight = (1.0, 1.0)
            popup.text = "<b>Confirmation</><br><br>Click <i>Delete</i> if you wish to delete the launcher. Otherwise, click <i>Close</i>."
            bt = elm.Button(self.win)
            bt.text = "Close"
            val = 2
            bt.callback_clicked_add(self.remove_files, val)
            popup.part_content_set("button1", bt)
            bt = elm.Button(self.win)
            bt.text = "Delete"
            val = 1
            bt.callback_clicked_add(self.remove_files, val)
            popup.part_content_set("button2", bt)
            popup.show()

#---------GENERAL
    def separator(self, vbox=False, addto=False):
        sep = elm.Separator(self.win)
        sep.horizontal_set(True)
        sep.show()
        if vbox:
            vbox.pack_end(sep)
        else:
            addto.content_set(sep)

    def iw_close(self, tb=False, tbi=False, obt=False):
        self.iw.delete()
        if obt:
            obt.disabled_set(False)
    def iwin_close(self, tb=False, tbi=False, obt=False, iw=False):
        iw.delete()
        if obt:
            obt.disabled_set(False)

    def editor_save(self, tb=False, tbi=False, vbox=False, val=False):
        #~ repl = self.line_list()
        #~ search = self.search_list()
        self.man.file_save()
        dest = self.dtfp.entry_get()
        dest = local + dest + ".menu"
        path = self.path

        #~ with open(path) as file:
            #~ data = file.readlines()
        #~ for i, line in enumerate(data):
            #~ data[i]= line.decode('utf-8')
        #~ for x in search:
            #~ if x:
                #~ y = search.index(x)
                #~ data = self.return_data(data, repl, x, y)
        #~ for x in search:
            #~ if x:
                #~ y = search.index(x)
                #~ data = self.return_new(data, repl, x, y)
        #~ for i, line in enumerate(data):
            #~ data[i]= line.encode('utf-8')
        #~ with open(path, 'w') as file:
            #~ file.writelines(data)

        if not path == dest:
            ecore.Exe("mv '%s' '%s'" %(path, dest))

        ecore.Exe("update-menus")

        if val:
            self.editor_core(None, None, vbox, dest)
            return
        else:
            vbox.delete()
            self.vipbox()

    def creator_create(self, tb=False, tbi=False, vbox=False, dest=False):
        new = self.line_list()
        path = self.dtfp.entry_get()

        with open(dest) as file:
            data = file.readlines()
        data[1] = new[0]
        del new[0]
        data.extend(new)

        with open(dest, 'w') as file:
            file.writelines(data)

        ecore.Exe("mv '%s' '%s%s.menu'" %(dest, local, path))
        vbox.delete()
        self.vipbox()

        ecore.Exe("update-menus")

    def manual_win(self, bt, path, vbox, item=False):
        if not item:
            with open(path) as file:
                data = file.readlines()
            new = self.line_list()
            data[1] = new[0]
            del new[0]
            data.extend(new)
            with open(path, 'w') as file:
                file.writelines(data)
            item = path

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 460)
        vbox.padding_set(0 , 5)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        self.separator(vbox)

        self.desktop_file(path, vbox, item)

    def dubclick(self, maingl, item):
        path = item.data['fullpath']

        box = elm.Box(self.win)
        box.padding_set(0 , 5)
        box.size_hint_weight_set(1.0, 1.0)
        box.show()

        iw = self.iw = elm.InnerWindow(self.win)
        iw.content_set(box)
        iw.show()
        iw.activate()

        val = 1
        self.desktop_file(path, box, item, val)


    def desktop_file(self, path, vbox, item, val=None):
        sc = elm.Scroller(self.win)
        sc.size_hint_align_set(-1.0, -1.0)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.policy_set(True, True)
        vbox.pack_end(sc)
        sc.show()

        man = self.man = elm.Entry(self.win)
        man.line_wrap_set(0)
        if val:
            man.autosave_set(False)
        else:
            man.autosave_set(True)
        man.file_set(path, 0)
        man.size_hint_align_set(-1.0, -1.0)
        man.size_hint_weight_set(1.0, 1.0)
        sc.content_set(man)
        if val:
            man.editable_set(False)
        else:
            man.editable_set(True)
        man.scrollable_set(False)
        man.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        if val:
            tb.item_append("", "Close", self.iw_close)
        else:
            tb.item_append("", "Done", self.delay, vbox, item)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

    def editor_full(self, bt=False, vbox=False):
        vbox.delete()
        self.vipbox()
    def creator_full(self, bt=False, vbox=False, dest=False):
        ecore.Exe("rm '%s'" %dest)
        vbox.delete()
        self.vipbox()

    def editor_close(self, tb=False, tbi=False, vbox=False):
        vbox.delete()
        self.vipbox()
    def creator_close(self, tb=False, tbi=False, vbox=False, dest=False):
        ecore.Exe("rm '%s'" %dest)
        vbox.delete()
        self.vipbox()

    def remove_files(self, bt, val):
        item = self.maingl.selected_item_get()
        path = item.data["fullpath"]
        self.rmp.delete()
        if val == 2:
            return
        if os.path.exists(path):
            ecore.Exe("rm '%s'" %path)
        item.delete()

    def return_data(self, data=False, repl=False, x=False, y=False):
        for i, line in enumerate(data):
            if x == "Name=":
                if x in line:
                    data[i] = repl[y]
                    break
            if x in line:
                data[i] = repl[y]
                break
        return data

    def return_new(self, data=False, repl=False, x=False, y=False):
        for line in data:
            if x == "Name=":
                break
            check = " ".join(data)
            if x in check:
                break
            if not x in data:
                data.append(repl[y])
                break
        return data

    def line_list(self):
        L = []
        name = "Name=%s" %self.name.entry_get();L.append(name)
        typ  = "Type=Directory";L.append(typ)
        com  = "Comment=%s" %self.com.entry_get();L.append(com)
        icon = "Icon=%s" %self.icon.entry_get();L.append(icon)
        L = [x+"\n" for x in L]
        return L

    def search_list(self):
        S = []
        name = "Name=";S.append(name)
        typ  = "";S.append(typ)
        com  = "Comment=";S.append(com)
        icon = "Icon=";S.append(icon)
        return S

    def delay(self, tb, tbi, vbox, item):
        tb.disabled_set(True)
        n = self.n = elm.Notify(self.win)
        n.orient = 1
        n.allow_events_set(False)
        n.show()
        tb = "filler"

        ecore.Timer(1.5, self.editor_core, tb, tbi, vbox, item, n)

#~
#~ class Menu(dexml.Model):
    #~ menus = fields.List(Menu)
