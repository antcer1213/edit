#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
import evas
import edje
import ecore
from time import sleep


"""eDit

An lxde/e17 menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""

HOME = os.getenv("HOME")
LOCAL = "%s/.local/share/desktop-directories/" %HOME
SYSTEM = "/usr/share/desktop-directories/"
NUM = '0123456789'



class MenuItem(object):
    def __init__(self, tb, tbi, win, vbox=False):
        if vbox:
            vbox.delete()

        self.win = win

        self.vipbox()

#----------------------MAIN WINDOW
    def vipbox(self):
        from launchers import Launchers
        from menulayout import MenuLayout

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
        tb.item_append("", "Item View")
        tb.item_append("", "Layout View", MenuLayout, self.win, vbox)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.separator(vbox)
        self.gl(None, None, vbox)
        self.add_files(self.maingl, LOCAL)
        self.separator(vbox)

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Add", self.system_launcher)
        tb.item_append("", "Edit", self.editor, vbox)
        tb.item_append("", "Create", self.creator, vbox)
        tb.item_append("", "Remove", self.rm_popup)
        tb.item_append("", "Refresh", self.gl, vbox)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
        self.win.show()


#----------------------MAIN LIST
    def gl(self, tb=False, tbi=False, vbox=False):
        if tb:
            self.maingl.clear()
            self.add_files(self.maingl, LOCAL)
        else:
            gl = self.maingl = elm.Genlist(self.win)
            gl.size_hint_weight_set(1.0, 1.0)
            gl.size_hint_align_set(-1.0, -1.0)
            gl.callback_clicked_double_add(self.dubclick)
            vbox.pack_end(gl)
            gl.show()

#----------------------FILE ADDER - NAME/CONTENT RETRIEVAL
    def add_files(self, gl, fil):
        if not os.path.isdir(fil):
            data = {};data['fullpath'] = fil
            fil = os.path.basename(fil)
            fil = os.path.splitext(fil)[0]
            data['name'] = fil
            self.add_file(gl, data)
            return
        else:
            files = os.listdir(fil)
            for f in files:
                if not f.endswith('.directory'):
                    files.remove(f)
            if files == []:
                return
            name = ['one']
            for f in files:
                location = fil + f
                name = self.get_name(location, name)
            namefile = dict()
            for i, n in enumerate(name):
                namefile.setdefault(n, files[i])
            old = namefile.values();new = old[:]
            for i, k in enumerate(new):
                new[i] = k.capitalize()
            capfile = dict()
            for i, n in enumerate(new):
                capfile.setdefault(n, old[i])
            new.sort()
            for n in new:
                l = capfile.get(n)
                n = fil + l
                self.add_files(gl, n)

    def add_file(self, gl, data):
        itc = elm.GenlistItemClass(item_style="default", text_get_func=self.name_return, content_get_func=self.icon_return)
        gl.item_append(itc, data, None)

    def add_group(self, gl):
        itc = elm.GenlistItemClass(item_style="default", text_get_func=self.name_return, content_get_func=self.icon_return)
        gl.item_append(itc, data, None)

    def name_return(self, obj, part, data ):
        path = data["fullpath"]
        label = self.get_name(path)
        return label

    def icon_return(self, obj, part, data ):
        if part == "elm.swallow.icon":
            path = data['fullpath']
            f = elm.Box(self.win)
            f.horizontal_set(True)
            f.show()

            icon = "none"
            with open(path) as file:
                data = file.readlines()
            for x in data:
                if "Icon=" in x:
                    icon = x.split("=")[-1]
                    if not icon == "\n":
                        icon = icon[:-1]
                    break

            ic = elm.Icon(self.win)
            if ic.standard_set(icon):
                pass
            else:
                ic.standard_set("none")
            ic.size_hint_weight_set(1.0, 1.0)
            ic.size_hint_align_set(-1.0, -1.0)
            f.pack_end(ic)
            ic.show()

            return f

    def get_name(self, path, name=False, check=False):
        copy = path[:]
        path = os.path.basename(path)
        path = os.path.splitext(path)[0]

        if not check:
            with open(copy) as file:
                data = file.readlines()
            for x in data:
                full = " ".join(data)
                if not "Name=" in full:
                    label = "None"
                    if name:
                        if name[0] == "one":
                            name[0] = label
                        else:
                            name.append(label)
                    break
                if "Name=" in x:
                    label = x.split("=")[-1]
                    label = label[:-1]
                    if "lxde" in path:
                        label = "LXDE - " + label
                    if "X-Ubuntu" in full:
                        label = "GNOME - " + label
                    if name:
                        if name[0] == "one":
                            name[0] = label
                        else:
                            name.append(label)
                    break
        if name:
            return name
        elif check:
            return path
        else:
            return label


#----------------------SYSTEM LAUNCHER
    def system_launcher(self, tb, bt):
        obt = bt
        obt.disabled_set(True)

        vbox = elm.Box(self.win)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        gl = self.sysgl = elm.Genlist(self.win)
        self.add_files(gl, SYSTEM)
        gl.size_hint_weight_set(1.0, 1.0)
        gl.size_hint_align_set(-1.0, -1.0)
        gl.callback_clicked_double_add(self.dubclick)
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
        tb.item_append("", "Close", self.iw_close, iw, obt)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

    def sys_cb(self, tb=False, tbi=False):
        item = self.sysgl.selected_item_get()
        if item:
            path = item.data["fullpath"]
            name = item.data["name"]
            newpath = "%s%s.directory" %(LOCAL, name)
            if not os.path.exists(newpath):
                ecore.Exe("cp '%s' '%s'" %(path, LOCAL))
                ecore.Timer(0.5, self.add_files, self.maingl, newpath)


#----------------------EDITOR/CREATOR LAUNCHER
    def editor(self, tb, tbi, vbox):
        item = self.maingl.selected_item_get()
        if item:
            self.editor_core(vbox, item)

    def creator(self, tb, tbi, vbox):
        self.editor_core(vbox)

    def editor_core(self, vbox, item=False, notify=False, check=False):
        def new():
            dest = LOCAL + "default"
            copy = dest[:]
            for x in NUM:
                dest.strip('-0123456789')
                dest = dest + "-" + x
                newpath = dest + ".directory"
                if not os.path.exists(newpath):
                    ecore.Exe("echo '[Desktop Entry]' > %s" %newpath)
                    sleep(5)
                    ecore.Exe("echo 'Name=Default' >> %s" %newpath)
                    sleep(5)
                    break
                else:
                    dest = copy
            return newpath

        if notify:
            notify.delete()

        if item:
            self.item = item
            if type(item) is unicode or type(item) is str:
                path = self.path = item
                pathname = self.get_name(path, None, item)
                pass
            else:
                path = self.path = item.data['fullpath']
                pathname = item.data['name']
        else:
            n = elm.Notify(self.win)
            n.orient = 1
            n.allow_events_set(False)
            n.show()
            path = new()
            ecore.Timer(1.0, self.editor_core, vbox, path, n, True)
            return

        name = "";icon = "";com = ""

        with open(path) as deskfile:
            for x in deskfile:
                if "Name=" in x:
                    name = x.split("=")[-1]
                    break
        with open(path) as deskfile:
            for x in deskfile:
                if "Icon=" in x:
                    icon = x.split("=")[-1]
                    break
        with open(path) as deskfile:
            for x in deskfile:
                if "Comment=" in x:
                    com  = x.split("=")[-1]
                    break

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
        vbox.padding_set(2, 2)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        fr = elm.Frame(self.win)
        fr.text = "Name:"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.name = elm.Entry(self.win)
        en.size_hint_weight_set(1.0, 1.0)
        en.text = name
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        ib = elm.Box(self.win)
        ib.horizontal_set(True)
        ib.size_hint_weight_set(1.0, 0.0)
        ib.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(ib)
        ib.show()

        fr = elm.Frame(self.win)
        fr.text = "Icon:"
        fr.size_hint_weight_set(1.0, 1.0)
        fr.size_hint_align_set(-1.0, -1.0)
        ib.pack_end(fr)
        fr.show()

        def icon_change(en):
            icon = self.icon.entry_get()
            self.ic.standard_set(icon)

        ic = self.ic = elm.Icon(self.win)
        en = self.icon = elm.Entry(self.win)
        if not check:
            en.text = icon
        else:
            en.text = "none"
        en.callback_activated_add(icon_change)
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        icon = icon[:-1]
        if ic.standard_set(icon):
            pass
        else:
            ic.standard_set("none")
        ic.size_hint_weight_set(1.0, 1.0)
        ic.size_hint_align_set(-1.0, -1.0)
        ib.pack_end(ic)
        ic.show()

        fr = elm.Frame(self.win)
        fr.text = "Comment:"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.com = elm.Entry(self.win)
        en.text = com
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        fr = elm.Frame(self.win)
        fr.text = "File Name(no suffix):"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.dtfp = elm.Entry(self.win)
        en.text = pathname
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        fil = elm.Box(self.win)
        fil.size_hint_weight_set(1.0, 1.0)
        fil.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fil)
        fil.show()

        lbb = elm.Box(self.win)
        lbb.horizontal_set(True)
        lbb.size_hint_weight_set(1.0, 0.0)
        lbb.size_hint_align_set(-1.0, -1.0)
        lbb.show()
        vbox.pack_end(lbb)

        bt = elm.Button(self.win)
        bt.text = "File Path:"
        bt.size_hint_weight_set(0.0, 1.0)
        bt.size_hint_align_set(-1.0, -1.0)
        bt.disabled_set(True)
        lbb.pack_end(bt)
        bt.show()

        en = elm.Entry(self.win)
        en.text = path
        en.editable_set(False)
        en.single_line = True
        en.scrollable_set(True)
        en.size_hint_weight_set(1.0, 1.0)
        en.size_hint_align_set(-1.0, -1.0)
        lbb.pack_end(en)
        en.show()

        btnb = elm.Box(self.win)
        btnb.horizontal_set(True)
        btnb.size_hint_weight_set(1.0, 0.0)
        btnb.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(btnb)
        btnb.show()

        if not check:
            bt = elm.Button(self.win)
            bt.text_set("Save")
            bt.callback_clicked_add(self.editor_save, None, vbox, True)
            btnb.pack_end(bt)
            bt.show()

        if not check:
            bt = elm.Button(self.win)
            bt.text_set("Manual")
            #~ if not check:
                #~ bt.callback_clicked_add(self.manual_win, path, vbox, True)
            #~ else:
            bt.callback_clicked_add(self.manual_win, path, vbox)
            btnb.pack_end(bt)
            bt.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        if not check:
            tb.item_append("", "Done", self.editor_save, vbox)
        else:
            tb.item_append("", "Create", self.creator_create, vbox)
        if not check:
            tb.item_append("", "Cancel", self.editor_close, vbox)
        else:
            tb.item_append("", "Cancel", self.editor_close, vbox, path)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

    def editor_save(self, tb=False, tbi=False, vbox=False, check=False):
        repl = self.line_list()
        search = self.search_list()
        path = self.path
        dest = self.dtfp.entry_get()
        dest = "%s%s.directory" %(LOCAL, dest)

        with open(path) as file:
            data = file.readlines()
        for i, line in enumerate(data):
            data[i] = line.decode('utf-8')
        for x in search:
            y = search.index(x)
            data = self.return_data(data, repl, x, y)
            data = self.return_new(data, repl, x, y)
        for i, line in enumerate(data):
            data[i]= line.encode('utf-8')
        with open(path, 'w') as file:
            file.writelines(data)

        #~ ecore.Exe("update-menus")

        if not dest == path:
            ecore.Exe("mv '%s' '%s'" %(path, dest))
            sleep(5)

        if check:
            n = self.n = elm.Notify(self.win)
            n.orient = 1
            n.allow_events_set(False)
            n.show()
            ecore.Timer(1.0, self.editor_core, vbox, dest, n)
            return
        else:
            vbox.delete()
            self.vipbox()

    def creator_create(self, tb=False, tbi=False, vbox=False):
        new = self.line_list()
        path = self.path
        dest = self.dtfp.entry_get()
        dest = "%s%s.directory" %(LOCAL, dest)

        with open(path) as file:
            data = file.readlines()
        data[1] = new[0]
        del new[0]
        data.extend(new)
        with open(path, 'w') as file:
            file.writelines(data)

        if not dest == path:
            ecore.Exe("mv '%s' '%s'" %(path, dest))
            sleep(5)

        vbox.delete()
        self.vipbox()
        #~ ecore.Exe("update-menus")

    def manual_win(self, bt, path, vbox, check=False):
        if not check:
            with open(path) as file:
                data = file.readlines()
            new = self.line_list()
            data[1] = new[0]
            del new[0]
            data.extend(new)
            with open(path, 'w') as file:
                file.writelines(data)

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
        vbox.padding_set(0 , 5)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        self.separator(vbox)

        self.file_viewer(path, vbox)

    def return_data(self, data, repl, x, y):
        for i, line in enumerate(data):
            if x == "Name=":
                if x in line:
                    data[i] = repl[y]
                    break
            if x in line:
                data[i] = repl[y]
                break
        return data

    def return_new(self, data, repl, x, y):
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

    def editor_close(self, tb=False, tbi=False, vbox=False, dest=False):
        if dest:
            ecore.Exe("rm '%s'" %dest)
            sleep(3)
        vbox.delete()
        self.vipbox()

    def delay(self, tb, tbi, vbox, item):
        tb.disabled_set(True)
        n = elm.Notify(self.win)
        n.orient = 1
        n.allow_events_set(False)
        n.show()

        ecore.Timer(1.5, self.editor_core, vbox, item, n)


#----------------------REMOVAL POPUP
    def rm_popup(self, tb, bt):
        if self.maingl.selected_item_get():
            popup = self.rmp = elm.Popup(self.win)
            popup.size_hint_weight = (1.0, 1.0)
            popup.text = "<b>Confirmation</><br><br>Click <i>Delete</i> if you wish to delete the directory. Otherwise, click <i>Cancel</i>."
            bt = elm.Button(self.win)
            bt.text = "Cancel"
            bt.callback_clicked_add(self.remove_files, True)
            popup.part_content_set("button1", bt)
            bt = elm.Button(self.win)
            bt.text = "Delete"
            bt.callback_clicked_add(self.remove_files, False)
            popup.part_content_set("button2", bt)
            popup.show()

    def remove_files(self, bt, cancel):
        item = self.maingl.selected_item_get()
        path = item.data["fullpath"]
        self.rmp.delete()
        if cancel:
            return
        if os.path.exists(path):
            ecore.Exe("rm '%s'" %path)
        item.delete()


#----------------------FILE CONTENT VIEWER
    def file_viewer(self, path, vbox, iw, check=None):
        if check:
            with open(path) as deskfile:
                for x in deskfile:
                    if "Icon=" in x:
                        icon = x.split("=")[-1]

            ib = elm.Box(self.win)
            ib.size_hint_weight_set(1.0, 0.5)
            ib.size_hint_align_set(-1.0, -1.0)
            vbox.pack_end(ib)
            ib.show()

            icon = icon[:-1]
            ic = elm.Icon(self.win)
            if ic.standard_set(icon):
                pass
            else:
                ic.standard_set("none")
            ic.size_hint_weight_set(1.0, 1.0)
            ic.size_hint_align_set(-1.0, -1.0)
            ib.pack_end(ic)
            ic.show()
        else:
            self.fullpath = path
            with open(path) as file:
                data = file.readlines()
            for i, x in enumerate(data):
                try:
                    x = x.encode('utf-8')
                except:
                    del data[i]
            with open(path, 'w') as file:
                file.writelines(data)

        sc = elm.Scroller(self.win)
        sc.size_hint_align_set(-1.0, -1.0)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.policy_set(True, True)
        vbox.pack_end(sc)
        sc.show()

        man = self.man = elm.Entry(self.win)
        man.line_wrap_set(0)
        if check:
            man.autosave_set(False)
        else:
            man.autosave_set(True)
        man.file_set(path, 0)
        man.size_hint_align_set(-1.0, -1.0)
        man.size_hint_weight_set(1.0, 1.0)
        sc.content_set(man)
        if check:
            man.editable_set(False)
        else:
            man.editable_set(True)
        man.scrollable_set(False)
        man.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        if check:
            tb.item_append("", "Close", self.iw_close, iw)
        else:
            tb.item_append("", "Done", self.delay, vbox, self.item)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()


#---------GENERAL
    def separator(self, vbox=False, addto=False):
        sep = elm.Separator(self.win)
        sep.horizontal_set(True)
        sep.show()
        if vbox:
            vbox.pack_end(sep)
        else:
            addto.content_set(sep)

    def iw_close(self, tb, tbi, iw, obt=False):
        iw.delete()
        if obt:
            obt.disabled_set(False)

    def dubclick(self, maingl, item):
        path = item.data['fullpath']

        box = elm.Box(self.win)
        box.padding_set(0 , 5)
        box.size_hint_weight_set(1.0, 1.0)
        box.show()

        iw = elm.InnerWindow(self.win)
        iw.content_set(box)
        iw.show()
        iw.activate()

        self.file_viewer(path, box, iw, True)

