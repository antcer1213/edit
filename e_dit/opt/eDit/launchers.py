#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
import evas
import edje
import ecore
import mimetypes
from menus import Menus

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
        vbox.padding_set(5, 5)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Launcher View")
        tb.item_append("", "Menu View", Menus, self.win, vbox)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.separator(vbox)

        gl = self.maingl = elm.Genlist(self.win)
        gl.size_hint_weight_set(1.0, 1.0)
        gl.size_hint_align_set(-1.0, -1.0)
        gl.bounce_set(False, True)
        gl.callback_clicked_double_add(self.dubclick)
        gl.multi_select_set(False)
        gl.show()
        vbox.pack_end(gl)

        self.add_files(gl, None, local)
        self.separator(vbox)

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Add", self.system_launcher)
        tb.item_append("", "Edit", self.editor, vbox)
        tb.item_append("", "Create", self.editor_core, vbox)
        tb.item_append("", "Remove", self.rm_popup)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.win.resize_object_add(vbox)
        self.win.resize(380, 425)
        self.win.show()

#-----Crucial
    def add_files(self, gl, bt= None, fil=None ):
        if fil:
            if not os.path.isdir(fil):
                data = {};data['fullpath'] = fil
                split = fil.split("/")
                fil = os.path.basename(fil);fil = os.path.splitext(fil)[0]
                data['name'] = fil
                split.remove(split[len(split)-1])
                if not split[0]:
                    split.remove(split[0])
                path = "/".join(split)
                data['path'] = "/%s/"%path
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
        path = data["fullpath"]
        label = ""
        label = self.get_name(path)
        cat = "None"
        with open(path) as deskfile:
            for x in deskfile:
                y = x.split("=")[-1]
                if "Game;" in x:
                    cat = "Game"
                    break
                if "AudioVideo;" in x:
                    cat = "Sound/Video"
                    break
                if "Graphics;" in x:
                    cat = "Graphics"
                    break
                if "Network;" in x:
                    cat = "Internet"
                    break
                if "Utility;" in x:
                    cat = "Accessories"
                    break
                if "Office;" in x:
                    cat = "Office"
                    break
                if "System;" in x:
                    cat = "System Tools"
                    break
                if "Development;" in x:
                    cat = "Programming"
                    break
                if "Education;" in x:
                    cat = "Education"
                    break
                if "Settings;" in x:
                    cat = "Preferences"
                    break
                if "Game;" in x:
                    cat = "Sound/Video"
                    break
                if "Categories=" in x and y != "" and y != "\n":
                    cat = "Other"
                    break

        total = label+" - "+cat
        return total

    def icon_return(self, obj, part, data ):
        if part == "elm.swallow.icon":
            f = elm.Box(self.win)
            f.horizontal_set(True)
            f.show()

            sep = elm.Separator(self.win)
            sep.show()

            path = data['fullpath']

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
            ic.standard_set(icon)
            ic.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
            ic.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
            ic.show()

            f.pack_end(ic)
            f.pack_end(sep)

            return f

    def sys_cb(self, bt=False):
        item = self.sysgl.selected_item_get()
        if item:
            path = item.data["fullpath"]
            name = item.data["name"]
            newpath = "%s%s.desktop" %(local, name)
            if not os.path.exists(newpath):
                ecore.Exe("cp '%s' '%s'" %(path, local))
                ecore.Timer(0.3, self.add_files, self.maingl, None, newpath)

#-----------INNER WINDOWS
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

        btnb = elm.Box(self.win)
        btnb.horizontal_set(True)
        btnb.size_hint_weight_set(1.0, 0.0)
        vbox.pack_end(btnb)
        btnb.show()

        bt = elm.Button(self.win)
        bt.text_set("Add")
        bt.callback_clicked_add(self.sys_cb)
        bt.size_hint_align_set(-1.0, -1.0)
        bt.size_hint_weight_set(1.0, 0.0)
        btnb.pack_end(bt)
        bt.show()

        iw = elm.InnerWindow(self.win)
        iw.content = vbox
        iw.show()
        iw.activate()

        bt = elm.Button(self.win)
        bt.text_set("Close")
        bt.callback_clicked_add(self.iwin_close, obt, iw)
        bt.size_hint_align_set(-1.0, -1.0)
        bt.size_hint_weight_set(1.0, 0.0)
        btnb.pack_end(bt)
        bt.show()

        self.add_files(gl, None, system)

    def editor(self, tb, bt, vbox):
        item = self.maingl.selected_item_get()
        if item:
            self.editor_core(tb, bt, vbox, item)

    def editor_core(self, tb, bt, vbox, item=None, n=False):
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
        name  = self.oldname = ""
        gen   = self.oldgen  = ""
        exe   = self.oldexe  = ""
        icon  = self.oldicon = ""
        mime  = self.oldmime = ""
        cat   = self.oldcat  = ""
        com   = self.oldcom  = ""
        hide  = self.oldhide = ""
        h = self.h = "false"
        nodis = ""
        n = self.n = "false"
        start = ""
        s = self.s = "false"
        term  = ""
        t = self.t = "false"

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
        self.win.resize(380, 425)
        vbox.padding_set(2, 2)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        fr = elm.Frame(self.win)
        fr.text = "Name:"
        fr.size_hint_weight_set(1.0, 1.0)
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
        fr.size_hint_weight_set(1.0, 1.0)
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
        fr.size_hint_weight_set(1.0, 1.0)
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
        ib.size_hint_weight_set(1.0, 1.0)
        ib.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(ib)
        ib.show()

        ic = self.ic = elm.Icon(self.win)
        ic.size_hint_weight_set(0.0, 1.0)
        ic.size_hint_align_set(-1.0, -1.0)
        if item:
            inic = "%s"%icon
            ic.standard_set(inic)
        else:
            ic.standard_set("none")
        ib.pack_end(ic)
        ic.show()

        self.separator(ib)

        fr = elm.Frame(self.win)
        fr.text = "Icon:"
        fr.size_hint_weight_set(1.0, 1.0)
        fr.size_hint_align_set(-1.0, -1.0)
        ib.pack_end(fr)
        fr.show()

        en = self.icon = elm.Entry(self.win)
        if item:
            en.text = icon
        else:
            en.text = "none"
        en.scrollable_set(True)
        en.single_line = True
        fr.content_set(en)

        fr = elm.Frame(self.win)
        fr.text = "MimeTypes:"
        fr.size_hint_weight_set(1.0, 1.0)
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
        fr.size_hint_weight_set(1.0, 1.0)
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
        cb.size_hint_weight_set(1.0, 1.0)
        cb.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(cb)
        cb.show()

        hs = self.hs = elm.Hoversel(self.win)
        hs.hover_parent_set(self.win)
        hs.text_set("Categories:")
        hs.item_add("Accessories")
        hs.item_add("Graphics")
        hs.item_add("Internet")
        hs.item_add("Preferences")
        hs.item_add("Programming")
        hs.item_add("Education")
        hs.item_add("Games")
        hs.item_add("Sound & Video")
        hs.item_add("Office")
        hs.item_add("System Tools")
        hs.item_add("Other")
        hs.size_hint_weight_set(0.0, 0.0)
        hs.size_hint_align_set(-1.0, 0.0)
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

        self.separator(cb)

        plb = elm.Box(self.win)
        plb.size_hint_weight_set(1.0, 1.0)
        plb.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(plb)
        plb.show()

        pl = elm.Panel(self.win)
        pl.hidden_set(False)
        pl.orient_set(elm.ELM_PANEL_ORIENT_RIGHT)
        pl.size_hint_weight_set(1.0, 1.0)
        pl.size_hint_align_set(-1.0, -1.0)

        lbb = elm.Box(self.win)
        plb.padding_set(0, 5)
        lbb.horizontal_set(True)
        lbb.size_hint_weight_set(1.0, 1.0)
        lbb.size_hint_align_set(-1.0, -1.0)
        pl.content_set(lbb)
        lbb.show()
        plb.pack_end(pl)
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
        plb.padding_set( 0, 5)
        chks.horizontal_set(True)
        chks.size_hint_weight_set(1.0, 1.0)
        chks.size_hint_align_set(-1.0, -1.0)
        pl.content_set(chks)
        chks.show()
        plb.pack_end(pl)
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

        if item:
            bt = elm.Button(self.win)
            bt.text_set("Save")
            bt.callback_clicked_add(self.editor_save)
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

        btnb = elm.Box(self.win)
        btnb.horizontal_set(True)
        btnb.size_hint_weight_set(1.0, 1.0)
        vbox.pack_end(btnb)
        btnb.show()

        bt = elm.Button(self.win)
        if item:
            bt.text_set("Done")
            bt.callback_clicked_add(self.editor_save, vbox)
        else:
            bt.text_set("Create")
            bt.callback_clicked_add(self.creator_create, vbox, dest)
        btnb.pack_end(bt)
        bt.show()

        bt = elm.Button(self.win)
        bt.text_set("Cancel")
        if item:
            bt.callback_clicked_add(self.editor_close, vbox)
        else:
            bt.callback_clicked_add(self.creator_close, vbox, dest)
        btnb.pack_end(bt)
        bt.show()

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
    def separator(self, vbox):
        sep = elm.Separator(self.win)
        sep.horizontal_set(True)
        sep.show()
        vbox.pack_end(sep)

    def iw_close(self, bt=False, obt=False):
        self.iw.delete()
        if obt:
            obt.disabled_set(False)
    def iwin_close(self, bt=False, obt=False, iw=False):
        iw.delete()
        if obt:
            obt.disabled_set(False)

    def editor_save(self, bt=False, vbox=False):
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

        if vbox:
            vbox.delete()
            self.vipbox()
    def creator_create(self, bt=False, vbox=False, dest=False):
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
        self.win.resize(380, 425)
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

        bt = elm.Button(self.win)
        if val:
            bt.text_set("Close")
        else:
            bt.text_set("Done")
        if val:
            bt.callback_clicked_add(self.iw_close)
        else:
            bt.callback_clicked_add(self.delay, vbox, item)
        vbox.pack_end(bt)
        bt.show()


    def editor_full(self, bt=False, vbox=False):
        vbox.delete()
        self.vipbox()
    def creator_full(self, bt=False, vbox=False, dest=False):
        ecore.Exe("rm '%s'" %dest)
        vbox.delete()
        self.vipbox()

    def editor_close(self, bt=False, vbox=False):
        vbox.delete()
        self.vipbox()
    def creator_close(self, bt=False, vbox=False, dest=False):
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

    def delay(self, bt, vbox, item):
        bt.disabled_set(True)
        n = self.n = elm.Notify(self.win)
        n.orient = 1
        n.allow_events_set(False)
        n.show()
        tb = "filler"

        ecore.Timer(1.5, self.editor_core, tb, bt, vbox, item, n)
