#!/usr/bin/env python
# encoding: utf-8
import os
import dexml
import elementary as elm
from ecore import Exe, Timer
from time import sleep
from dexml import fields


"""eDit

A menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""

HOME = os.getenv("HOME")
LOCAL = "%s/.config/menus/" %HOME
SYSTEM = "/etc/xdg/menus/"
NUM = '0123456789'



class MenuLayout(object):
    def __init__(self, tb, tbi, win, vbox=False):
        if vbox:
            vbox.delete()

        self.win = win

        self.vipbox()

#----------------------MAIN WINDOW
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
                if not f.endswith('.menu'):
                    files.remove(f)
            if files == []:
                return
            files.sort()
            for f in files:
                if fil == SYSTEM:
                    f = SYSTEM + f
                else:
                    f = LOCAL + f
                self.add_files(gl, f)

    def add_file(self, gl, data ):
        itc = elm.GenlistItemClass(item_style="default", text_get_func=self.name_return, content_get_func=self.icon_return)
        gl.item_append(itc, data, None)

    def name_return(self, obj, part, data):
        path = data["fullpath"]
        label = self.get_name(path)
        return label

    def icon_return(self, obj, part, data):
        if part == "elm.swallow.icon":
            f = elm.Box(self.win)
            f.show()

            ic = elm.Icon(self.win)
            ic.standard_set("text-xml")
            ic.size_hint_weight_set(1.0, 1.0)
            ic.size_hint_align_set(-1.0, -1.0)
            f.pack_end(ic)
            ic.show()

            return f

    def get_name(self, path, check=False):
        path = os.path.basename(path)
        path = os.path.splitext(path)[0]
        if not check:
            if "-" in path:
                name = path.replace("-", " ")
            else:
                name = path
            name = name.title()
        else:
            name = path
        return name


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

    def sys_cb(self, tb, tbi):
        item = self.sysgl.selected_item_get()
        if item:
            path = item.data["fullpath"]
            name = item.data["name"]
            copy = name[:]
            for x in NUM:
                name.strip('-0123456789')
                name = name + "-" + x
                newpath = "%s%s.menu" %(LOCAL, name)
                if not os.path.exists(newpath):
                    Exe("cp '%s' '%s'" %(path, newpath))
                    Timer(0.5, self.add_files, self.maingl, newpath)
                    break
                else:
                    name = copy


#----------------------EDITOR/CREATOR LAUNCHER
    def editor(self, tb, tbi, vbox):
        item = self.maingl.selected_item_get()
        if item:
            self.editor_core(vbox, item)

    def creator(self, tb, tbi, vbox):
        self.editor_core(vbox)

    def editor_core(self, vbox, item=None, notify=None, check=None):
        def new():
            dest = LOCAL + "new"
            copy = dest[:]
            for x in NUM:
                dest.strip('-0123456789')
                dest = dest + "-" + x
                newpath = dest + ".menu"
                if not os.path.exists(newpath):
                    Exe("cp '/opt/eDit/new.menu' '%s'" %newpath)
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
                pathname = self.get_name(path, item)
                pass
            else:
                path = self.path = item.data['fullpath']
                pathname = item.data['name']
        else:
            n = elm.Notify(self.win)
            n.allow_events_set(False)
            n.orient = 1
            n.show()
            path = new()
            Timer(1.0, self.editor_core, vbox, path, n, True)
            return

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
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
        man.scrollable_set(False)
        man.show()

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
        vbox.pack_end(btnb)
        btnb.show()

        if not check:
            bt = elm.Button(self.win)
            bt.size_hint_weight_set(1.0, 1.0)
            bt.text_set("Save")
            bt.callback_clicked_add(self.editor_save, None, vbox, True)
            btnb.pack_end(bt)
            bt.show()

            bt = elm.Button(self.win)
            bt.size_hint_weight_set(1.0, 1.0)
            bt.text_set("Manual")
            bt.callback_clicked_add(self.manual_win, path, vbox)
            btnb.pack_end(bt)
            bt.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        if not check:
            tb.item_append("", "Done", self.editor_save, vbox)
            tb.item_append("", "Cancel", self.editor_close, vbox)
        else:
            tb.item_append("", "Create", self.editor_save, vbox)
            tb.item_append("", "Cancel", self.editor_close, vbox, path)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

    def editor_save(self, tb, tbi, vbox, check=False):
        self.man.file_save()
        dest = self.dtfp.entry_get()
        dest = LOCAL + dest + ".menu"
        path = self.path

        if not path == dest:
            Exe("mv '%s' '%s'" %(path, dest))
            sleep(5)

        #~ Exe("update-menus")

        if check:
            self.editor_core(vbox, dest)
            return
        else:
            vbox.delete()
            self.vipbox()

    def manual_win(self, bt, path, vbox):
        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
        vbox.padding_set(0 , 5)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        self.separator(vbox)

        self.file_viewer(path, vbox)

    def editor_close(self, tb, tbi, vbox, dest=False):
        if dest:
            Exe("rm '%s'" %dest)
            sleep(3)
        vbox.delete()
        self.vipbox()

    def delay(self, tb, tbi, vbox, item):
        tb.disabled_set(True)
        n = elm.Notify(self.win)
        n.orient = 1
        n.allow_events_set(False)
        n.show()

        Timer(1.5, self.editor_core, vbox, item, n)


#----------------------REMOVAL POPUP
    def rm_popup(self, tb, bt):
        if self.maingl.selected_item_get():
            popup = self.rmp = elm.Popup(self.win)
            popup.size_hint_weight = (1.0, 1.0)
            popup.text = "<b>Confirmation</><br><br>Click <i>Delete</i> if you wish to delete the menu. Otherwise, click <i>Cancel</i>."
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
        elif os.path.exists(path):
            Exe("rm '%s'" %path)
        item.delete()


#----------------------FILE CONTENT VIEWER
    def file_viewer(self, path, vbox, iw, check=None):
        sc = elm.Scroller(self.win)
        sc.size_hint_align_set(-1.0, -1.0)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.policy_set(True, True)
        vbox.pack_end(sc)
        sc.show()

        man = elm.Entry(self.win)
        man.line_wrap_set(0)
        man.file_set(path, 0)
        man.size_hint_align_set(-1.0, -1.0)
        man.size_hint_weight_set(1.0, 1.0)
        sc.content_set(man)
        man.scrollable_set(False)

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.select_mode_set(2)
        vbox.pack_end(tb)

        if check:
            man.autosave_set(False)
            man.editable_set(False)
            tb.item_append("", "Close", self.iw_close, iw)
        else:
            man.autosave_set(True)
            man.editable_set(True)
            tb.item_append("", "Done", self.delay, vbox, self.item)

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

#~
#~ class Menu(dexml.Model):
    #~ menus = fields.List(Menu)
