#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
import evas
import edje
import ecore
from menuitem import MenuItem

"""eDit

An lxde/e17 menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""

HOME = os.getenv("HOME")
local = "%s/.local/share/applications/" %HOME
system = "/usr/share/applications/"


class Launchers(object):
    def __init__(self, tb=False, tbentry=False, win=False, vbox=False):

#----Main Window
        if vbox:
            vbox.delete()

        if win:
            self.win = win
        else:
            win = self.win = elm.StandardWindow("eDit", "eDit")
            win.callback_delete_request_add(lambda o: elm.exit())

        self.vipbox()

    def vipbox(self):
        vbox = self.vbox = elm.Box(self.win)
        vbox.padding_set(5, 0)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Launcher View")
        tb.item_append("", "Menu View", MenuItem, self.win, vbox)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.separator(vbox)
        self.gl(None, None, vbox)
        self.add_files(self.maingl, None, local)
        self.separator(vbox)

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
                    if not f.endswith('.desktop'):
                        files.remove(f)
                for f in files:
                    if "wine" in f and not f.endswith('.desktop'):
                        files.remove(f)
                name = ['one']
                for f in files:
                    location = "%s%s"%(fil, f)
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
                    n = "%s%s" %(fil, l)
                    self.add_files(gl, False, n)

    def add_file(self, gl, data ):
        itc = elm.GenlistItemClass(item_style="default", text_get_func=self.name_return, content_get_func=self.icon_return)
        gl.item_append(itc, data, None)

    def get_name(self, path, name=False):
        with open(path) as file:
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
            if "Name=" in x and not "GenericName=" in x:
                label = x.split("=")[-1]
                label = label[:-1]
                if name:
                    if name[0] == "one":
                        name[0] = label
                    else:
                        name.append(label)
                break
        if name:
            return name
        else:
            return label

    def name_return(self, obj, part, data ):
        A = ['Games', 'Sound & Video', 'Graphics', 'Internet', 'Accessories', 'Office', 'System Tools', 'Programming', 'Education', 'Preferences']
        B = ['Game;', 'AudioVideo;', 'Graphics;', 'Network;', 'Utility;', 'Office;', 'System;', 'Development;', 'Education;', 'Settings;']
        path = data["fullpath"]
        label = self.get_name(path)
        cat = "Other"
        with open(path) as deskfile:
            for x in deskfile:
                for i, a in enumerate(A):
                    b = B[i]
                    if b in x:
                        cat = a
                        break
                if "Categories=\n" in x:
                    cat = "None"
                    break

        total = label+" - "+cat
        return total

    def icon_return(self, obj, part, data ):
        if part == "elm.swallow.icon":
            path = data['fullpath']
            f = elm.Box(self.win)
            f.horizontal_set(True)
            f.show()
            sep = elm.Separator(self.win)
            sep.show()

            icon = "none"
            with open(path) as file:
                data = file.readlines()
            for x in data:
                if "Icon=" in x:
                    icon = x.split("=")[-1]
                    if not icon == "\n":
                        icon = icon[:-1]
                    else:
                        icon = "none"
                    break

            ic = elm.Icon(self.win)
            if ic.standard_set(icon):
                pass
            else:
                ic.standard_set("none")
            ic.size_hint_weight_set(1.0, 1.0)
            ic.size_hint_align_set(-1.0, -1.0)
            ic.show()
            f.pack_end(ic)
            f.pack_end(sep)

            return f

    def sys_cb(self, tb=False, tbi=False):
        item = self.sysgl.selected_item_get()
        if item:
            path = item.data["fullpath"]
            name = item.data["name"]
            newpath = "%s%s.desktop" %(local, name)
            if not os.path.exists(newpath):
                ecore.Exe("cp '%s' '%s'" %(path, local))
                ecore.Timer(0.3, self.add_files, self.maingl, None, newpath)

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

        iw = elm.InnerWindow(self.win)
        iw.content = vbox
        iw.show()
        iw.activate()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Add", self.sys_cb)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Close", self.iwin_close, obt, iw)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.add_files(gl, None, system)

    def editor_core(self, tb, tbi, vbox, item=None, n=False):
        if n:
            self.n.delete()
        if item:
            if not type(item) is str:
                path = item.data['fullpath']
            else:
                path = item
        else:
            dest = "%sblank.desktop" %local
            ecore.Exe("echo '[Desktop Entry]' > %s" %dest)
            ecore.Exe("echo 'Name=Default' >> %s" %dest)
            path = "%sblank.desktop" %local

        name  = "";gen   = "";exe   = "";icon  = "";mime  = "";cat   = "";com   = "";hide  = "";nodis = "";start = "";term  = ""
        h = self.h = "false";n = self.n = "false";s = self.s = "false";t = self.t = "false"

        with open(path) as deskfile:
            for x in deskfile:
                if "Name=" in x and not "GenericName=" in x:
                    name = x.split("=")[-1]
                    break
        with open(path) as deskfile:
            for x in deskfile:
                if "Exec=" in x:
                    exe  = x.split("=")[-1]
                    break
        with open(path) as deskfile:
            for x in deskfile:
                if "GenericName=" in x:
                    gen  = x.split("=")[-1]
                    break
        with open(path) as deskfile:
            for x in deskfile:
                if "Comment=" in x:
                    com  = x.split("=")[-1]
                    break
        with open(path) as deskfile:
            for x in deskfile:
                if "Icon=" in x:
                    icon = x.split("=")[-1]
                if "MimeType=" in x:
                    mime = x.split("=")[-1]
                if "Categories=" in x:
                    cat  = x.split("=")[-1]
                if "Hidden=" in x:
                    if "true" in x:
                        hide = True
                        h = "true"
                if "NoDisplay=" in x:
                    if "true" in x:
                        nodis = True
                        n = "true"
                if "StartupNotify=" in x:
                    if "true" in x:
                        start = True
                        s = "true"
                if "Terminal=" in x:
                    if "true" in x:
                        term = True
                        t = "true"

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 460)
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

        fr = elm.Frame(self.win)
        fr.text = "Generic Name:"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.gen = elm.Entry(self.win)
        en.size_hint_weight_set(1.0, 1.0)
        en.text = gen
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        fr = elm.Frame(self.win)
        fr.text = "Exec:"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.exe = elm.Entry(self.win)
        en.text = exe
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
        if item:
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
        ic.show()
        ib.pack_end(ic)

        fr = elm.Frame(self.win)
        fr.text = "MimeTypes:"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        en = self.mime = elm.Entry(self.win)
        en.text = mime
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

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

        cb = elm.Box(self.win)
        cb.horizontal_set(True)
        cb.size_hint_weight_set(1.0, 0.0)
        cb.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(cb)
        cb.show()

        def ch(hs, e):
            if self.a == e :
                self.cat.entry_set("Utility;") ; return
            if self.b == e:
                self.cat.entry_set("Graphics;") ; return
            if self.c == e:
                self.cat.entry_set("Network;") ; return
            if self.d == e:
                self.cat.entry_set("Settings;") ; return
            if self.e == e:
                self.cat.entry_set("Development;") ; return
            if self.f == e:
                self.cat.entry_set("Education;") ; return
            if self.g == e:
                self.cat.entry_set("Game;") ; return
            if self.h == e:
                self.cat.entry_set("AudioVideo;") ; return
            if self.i == e:
                self.cat.entry_set("Office;") ; return
            if self.j == e:
                self.cat.entry_set("System;") ; return

        hs = self.hs = elm.Hoversel(self.win)
        hs.hover_parent_set(self.win)
        hs.text_set("Category:")
        self.a = hs.item_add('Accessories', 'applications-accessories'); self.b = hs.item_add('Graphics', "applications-graphics"); self.c = hs.item_add('Internet', "applications-internet"); self.d = hs.item_add('Preferences', "preferences-desktop"); self.e = hs.item_add('Programming', "applications-development"); self.f = hs.item_add('Education', "applications-science"); self.g = hs.item_add('Games', "applications-games"); self.h = hs.item_add('Sound & Video', "applications-multimedia"); self.i = hs.item_add('Office', "applications-office"); self.j = hs.item_add('System Tools', "applications-system");
        hs.callback_selected_add(ch)
        hs.size_hint_weight_set(0.5, 0.0)
        hs.size_hint_align_set(-1.0, -1.0)
        cb.pack_end(hs)
        hs.show()

        en = self.cat = elm.Entry(self.win)
        en.text = cat
        en.scrollable_set(True)
        en.single_line = True
        en.size_hint_weight_set(1.0, 1.0)
        en.size_hint_align_set(-1.0, -1.0)
        cb.pack_end(en)
        en.show()

        pl = elm.Panel(self.win)
        pl.hidden_set(False)
        pl.orient_set(elm.ELM_PANEL_ORIENT_LEFT)
        pl.size_hint_weight_set(1.0, 1.0)
        pl.size_hint_align_set(-1.0, -1.0)

        lbb = elm.Box(self.win)
        lbb.horizontal_set(True)
        lbb.size_hint_weight_set(1.0, 1.0)
        lbb.size_hint_align_set(-1.0, -1.0)
        pl.content_set(lbb)
        lbb.show()
        vbox.pack_end(pl)
        pl.show()

        bt = elm.Button(self.win)
        if item:
            bt.text = "File Path:"
        else:
            bt.text = "File Name(no suffix):"
        bt.size_hint_weight_set(0.0, 1.0)
        bt.size_hint_align_set(-1.0, -1.0)
        bt.disabled_set(True)
        lbb.pack_end(bt)
        bt.show()

        en = self.dtfp = elm.Entry(self.win)
        if item:
            en.text = path
            en.editable_set(False)
        else:
            en.text = "Default"
            en.editable_set(True)
        en.single_line = True
        en.scrollable_set(True)
        en.size_hint_weight_set(1.0, 1.0)
        en.size_hint_align_set(-1.0, -1.0)
        lbb.pack_end(en)
        en.show()

        self.separator(lbb)

        pl = elm.Panel(self.win)
        pl.hidden_set(False)
        pl.orient_set(elm.ELM_PANEL_ORIENT_LEFT)
        pl.size_hint_weight_set(1.0, 1.0)
        pl.size_hint_align_set(-1.0, -1.0)

        chks = elm.Box(self.win)
        chks.horizontal_set(True)
        chks.size_hint_weight_set(1.0, 1.0)
        chks.size_hint_align_set(-1.0, -1.0)
        pl.content_set(chks)
        chks.show()
        vbox.pack_end(pl)
        pl.show()

        ck = self.hide = elm.Check(self.win)
        ck.text_set("Hidden")
        if hide:
            ck.state_set(True)
        chks.pack_end(ck)
        ck.show()

        ck = self.nodis = elm.Check(self.win)
        ck.text_set("Show in Menus")
        if nodis:
            ck.state_set(False)
        else:
            ck.state_set(True)
        chks.pack_end(ck)
        ck.show()

        ck = self.start = elm.Check(self.win)
        ck.text_set("Startup Notify")
        if start:
            ck.state_set(True)
        chks.pack_end(ck)
        ck.show()

        ck = self.term = elm.Check(self.win)
        ck.text_set("Run in Terminal")
        if term:
            ck.state_set(True)
        chks.pack_end(ck)
        ck.show()

        self.separator(chks)

        btnb = elm.Box(self.win)
        btnb.horizontal_set(True)
        btnb.size_hint_weight_set(1.0, 1.0)
        vbox.pack_end(btnb)
        btnb.show()

        btnb = elm.Box(self.win)
        btnb.horizontal_set(True)
        btnb.size_hint_weight_set(1.0, 0.0)
        vbox.pack_end(btnb)
        btnb.show()

        if item:
            bt = elm.Button(self.win)
            bt.text_set("Save")
            bt.callback_clicked_add(self.editor_save, None)
            btnb.pack_end(bt)
            bt.show()

        bt = elm.Button(self.win)
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

    def editor_save(self, tb=False, tbi=False, vbox=False):
        repl = self.line_list()
        search = self.search_list()
        path = self.dtfp.entry_get()

        with open(path) as file:
            data = file.readlines()
        for i, line in enumerate(data):
            data[i]= line.decode('utf-8')
        for x in search:
            if x:
                y = search.index(x)
                data = self.return_data(data, repl, x, y)
        #~ search = self.search_list()
        for x in search:
            if x:
                y = search.index(x)
                data = self.return_new(data, repl, x, y)
        for i, line in enumerate(data):
            data[i]= line.encode('utf-8')
        with open(path, 'w') as file:
            file.writelines(data)

        #~ ecore.Exe("update-desktop-database")

        if vbox:
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

        ecore.Exe("mv '%s' '%s%s.desktop'" %(dest, local, path))
        vbox.delete()
        self.vipbox()

        #~ ecore.Exe("update-desktop-database -q")

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
                if x in line and not "GenericName=" in line:
                    data[i] = repl[y]
                    break
            if x in line:
                data[i] = repl[y]
                break

        return data

    def return_new(self, data=False, repl=False, x=False, y=False):
        for line in data:
            if x == "Name=" and "GenericName=" not in line:
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
        A = ['Hidden=', 'NoDisplay=', 'StartupNotify=', 'Terminal=']
        B = [self.hide.state_get,self.nodis.state_get,self.start.state_get,self.term.state_get]
        C = ['hide', 'nodis', 'start', 'term']
        D = ['true', 'false']
        name = "Name=%s" %self.name.entry_get();L.append(name)
        exe  = "Exec=%s" %self.exe.entry_get();L.append(exe)
        typ  = "Type=Application";L.append(typ)
        gen  = "GenericName=%s" %self.gen.entry_get();L.append(gen)
        com  = "Comment=%s" %self.com.entry_get();L.append(com)
        icon = "Icon=%s" %self.icon.entry_get();L.append(icon)
        mime = "MimeType=%s" %self.mime.entry_get();L.append(mime)
        cat  = "Categories=%s" %self.cat.entry_get();L.append(cat)
        for i, x in enumerate(B):
            z = C[1] ; y = C[i]
            if x():
                s = D[0]
                if z == y:
                    s = D[1]
            else:
                s = D[1]
                if z == y:
                    s = D[0]
            y = A[i]+s
            L.append(y)
        L = [x+"\n" for x in L]
        return L

    def search_list(self):
        S = []
        name = "Name=";S.append(name)
        exe  = "Exec=";S.append(exe)
        typ  = "";S.append(typ)
        gen  = "GenericName=";S.append(gen)
        com  = "Comment=";S.append(com)
        icon = "Icon=";S.append(icon)
        mime = "MimeType=";S.append(mime)
        cat  = "Categories=";S.append(cat)
        hide = "Hidden=";S.append(hide)
        nodis= "NoDisplay=";S.append(nodis)
        start= "StartupNotify=";S.append(start)
        term = "Terminal=";S.append(term)
        return S

    def delay(self, tb, tbi, vbox, item):
        tb.disabled_set(True)
        n = self.n = elm.Notify(self.win)
        n.orient = 1
        n.allow_events_set(False)
        n.show()
        tb = "filler"

        ecore.Timer(1.5, self.editor_core, tb, tbi, vbox, item, n)
