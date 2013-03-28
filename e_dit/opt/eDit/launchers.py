#!/usr/bin/env python
# encoding: utf-8
import os
import elementary as elm
from ecore import Exe, Timer
from time import sleep
from menuitem import MenuItem

"""eDit

A menu-editor GUI built on Python-EFL's.
By: AntCer (bodhidocs@gmail.com)

Started: March 4, 2013
"""

HOME = os.getenv("HOME")
CONFIG = "%s/.config/eDit"%HOME
VIEW = "%s/default.view"%CONFIG
LOCAL = "%s/.local/share/applications/" %HOME
SYSTEM = "/usr/share/applications/"
CATNAME = ['Games', 'Sound & Video', 'Graphics', 'Internet', 'Accessories', 'Office', 'System Tools', 'Programming', 'Education', 'Preferences']
CATTYPE = ['Game;', 'AudioVideo;', 'Graphics;', 'Network;', 'Utility;', 'Office;', 'System;', 'Development;', 'Education;', 'Settings;']


class Launchers(object):
    def __init__(self, tb=False, tbi=False, win=False, vbox=False):
        with open(VIEW) as file:
            self.viewmode = file.readlines()
        viewmode  = self.viewmode[0].split("=")[-1]
        if viewmode == "True":
            self.viewcat = True
        else:
            self.viewcat = False

        if vbox:
            vbox.delete()
        if win:
            self.win = win
        else:
            win = self.win = elm.StandardWindow("eDit", "eDit")
            win.callback_delete_request_add(lambda o: elm.exit())

        self.A = False

        self.vipbox()


#----------------------MAIN WINDOW
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

        tbview = elm.Toolbar(self.win)
        tbview.size_hint_weight_set(1.0, 0.0)
        tbview.size_hint_align_set(-1.0, -1.0)
        tbview.homogeneous_set(True)
        tbview.select_mode_set(2)
        vbox.pack_end(tbview)
        tbview.show()

        self.separator(vbox)
        self.gl(None, None, vbox, self.viewcat)
        self.add_files(self.maingl, LOCAL)
        tbview.item_append("", "Normal View", self.gl, False, False)
        tbview.item_append("", "Category View", self.gl, False, True)
        tbview.item_append("", "Preferences", self.preferences)
        self.separator(vbox)


        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        tb.item_append("", "Add", self.system_launcher)
        tb.item_append("", "Edit", self.editor, vbox)
        tb.item_append("", "Create", self.creator, vbox)
        tb.item_append("", "Remove", self.rm_popup)
        tb.item_append("", "Refresh", self.gl, None, self.viewcat)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
        self.win.show()


#----------------------MAIN LIST
    def gl(self, tb=False, tbi=False, vbox=False, viewcat=False):
        if tb:
            self.maingl.clear()
            if viewcat:
                self.categoryview()
            self.viewcat = viewcat
            self.add_files(self.maingl, LOCAL)
        else:
            gl = self.maingl = elm.Genlist(self.win)
            gl.size_hint_weight_set(1.0, 1.0)
            gl.size_hint_align_set(-1.0, -1.0)
            if viewcat:
                self.categoryview()
            self.viewcat = viewcat
            gl.callback_clicked_double_add(self.dubclick)
            gl.show()
            vbox.pack_end(gl)


#----------------------CATEGORY VIEW
    def categoryview(self):
        catdata = {'name':'Accessories', 'cat':'Utility;', 'icon':'applications-accessories'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.A = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Preferences', 'cat':'Settings;', 'icon':'preferences-desktop'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.B = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Programming', 'cat':'Development;', 'icon':'applications-development'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.C = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Education', 'cat':'Education;', 'icon':'applications-science'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.D = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Games', 'cat':'Game;', 'icon':'applications-games'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.E = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Graphics', 'cat':'Graphics;', 'icon':'applications-graphics'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.F = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Internet', 'cat':'Network;', 'icon':'applications-internet'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.G = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Sound & Video', 'cat':'AudioVideo;', 'icon':'applications-multimedia'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.H = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Office', 'cat':'Office;', 'icon':'applications-office'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.I = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Other', 'cat':';', 'icon':'applications-other'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.J = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'System Tools', 'cat':'System;', 'icon':'applications-system'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.K = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)

        catdata = {'name':'Uncategorized', 'cat':'None;', 'icon':'none'}
        itpc = elm.GenlistItemClass(item_style="default",
                text_get_func=self.cat_return,
                content_get_func=self.icon_return)
        self.L = self.maingl.item_append(itpc, catdata, flags=elm.ELM_GENLIST_ITEM_TREE)


#----------------------FILE ADDER - NAME/CONTENT RETRIEVAL
    def add_files(self, gl, fil):
        copy = fil[:]
        if not os.path.isdir(fil):
            data = {};data['fullpath'] = fil
            fil = os.path.basename(fil)
            fil = os.path.splitext(fil)[0]
            data['name'] = fil

            A = CATNAME[:]
            B = CATTYPE[:]
            cat = "Other"
            with open(copy) as deskfile:
                for x in deskfile:
                    for i, a in enumerate(A):
                        b = B[i]
                        if b in x:
                            cat = a
                            break
                    if "Categories=\n" in x:
                        cat = "None"
                        break
            data['type'] = cat
            self.add_file(gl, data, cat)
            return
        else:
            files = os.listdir(fil)
            for f in files:
                if not f.endswith('.desktop'):
                    files.remove(f)
            for f in files:
                if "wine" in f and not f.endswith('.desktop'):
                    files.remove(f)
            if files == []:
                return
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
                self.add_files(gl, n)

    def add_file(self, gl, data, cat):
        itc = elm.GenlistItemClass(item_style="default",
                            text_get_func=self.name_return,
                            content_get_func=self.icon_return)
        path = data['fullpath']
        split = path.split("/")
        if split[1] == "usr":
            self.sysgl.item_append(itc, data, None)
            return
        if self.viewcat == False:
            self.maingl.item_append(itc, data, None)
            return
        if cat == self.A.data['name']:
            gl.item_append(itc, data, self.A)
            return
        elif cat == self.B.data['name']:
            gl.item_append(itc, data, self.B)
            return
        elif cat == self.C.data['name']:
            gl.item_append(itc, data, self.C)
            return
        elif cat == self.D.data['name']:
            gl.item_append(itc, data, self.D)
            return
        elif cat == self.E.data['name']:
            gl.item_append(itc, data, self.E)
            return
        elif cat == self.F.data['name']:
            gl.item_append(itc, data, self.F)
            return
        elif cat == self.G.data['name']:
            gl.item_append(itc, data, self.G)
            return
        elif cat == self.H.data['name']:
            gl.item_append(itc, data, self.H)
            return
        elif cat == self.I.data['name']:
            gl.item_append(itc, data, self.I)
            return
        elif cat == self.J.data['name']:
            gl.item_append(itc, data, self.J)
            return
        elif cat == self.K.data['name']:
            gl.item_append(itc, data, self.K)
            return
        else:
            gl.item_append(itc, data, self.L)

    def name_return(self, obj, part, data ):
        A = CATNAME[:]
        B = CATTYPE[:]
        path = data["fullpath"]
        label = self.get_name(path)
        if self.viewcat:
            return label
        else:
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

    def cat_return(self, obj, part, data ):
        A = CATNAME[:]
        B = CATTYPE[:]
        C = dict(zip(B,A))
        category = data['cat']
        if category == 'None;':
            cat = "None"
        else:
            cat = "Other"
            for b in B:
                if b == category:
                    cat = C[b]
                    break
        return cat

    def icon_return(self, obj, part, data ):
        if part == "elm.swallow.icon":
            f = elm.Box(self.win)
            f.horizontal_set(True)
            f.show()
            if 'icon' in data:
                icon = data['icon']
            elif 'fullpath' in data:
                path = data['fullpath']
                split = path.split("/")
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
            if 'icon' in data:
                pass
            else:
                if split[1] == "home" and self.viewcat:
                    sep = elm.Separator(self.win)
                    sep.show()
                    f.pack_end(sep)
            return f

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
                    test = " ".join(name)
                    if label in test:
                        label = label + "-1"
                    if "-1" in label:
                        label = label.rstrip("-1") + "-2"
                    if name[0] == "one":
                        name[0] = label
                    else:
                        name.append(label)
                break
        if name:
            return name
        else:
            return label


#----------------------PREFERENCES
    def preferences(self, tb, bt):
        def defaultview(rg):
            val = self.rdg.value_get()
            if val ==2:
                self.viewcat = True
                self.viewmode[0] = "catview=True"
            else:
                self.viewcat = False
                self.viewmode[0] = "catview=False"
            self.gl(tb, bt, None, self.viewcat)
            with open(VIEW, 'w') as file:
                file.writelines(self.viewmode)
        obt = bt
        obt.disabled_set(True)

        vbox = elm.Box(self.win)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        fr = elm.Frame(self.win)
        fr.text = "Start-Up/Refresh View (requires application restart)"
        fr.size_hint_weight_set(1.0, 0.0)
        fr.size_hint_align_set(-1.0, -1.0)
        vbox.pack_end(fr)
        fr.show()

        rdb = elm.Box(self.win)
        rdb.horizontal_set(True)
        fr.content_set(rdb)
        rdb.show()

        rd = self.r1 = elm.Radio(self.win)
        rd.callback_changed_add(defaultview)
        rd.state_value_set(1)
        rd.text_set("Normal")
        rdb.pack_end(rd)
        rdg = self.rdg = rd
        rd.show()

        rd = self.r2 = elm.Radio(self.win)
        rd.callback_changed_add(defaultview)
        rd.state_value_set(2)
        rd.group_add(rdg)
        rd.text_set("Category")
        rdb.pack_end(rd)
        rd.show()

        viewmode = self.viewmode[0].split("=")[-1]
        if viewmode == "True":
            self.rdg.value_set(2)
        else:
            self.rdg.value_set(1)

        fil = elm.Box(self.win)
        fil.size_hint_weight_set(1.0, 1.0)
        vbox.pack_end(fil)
        fil.show()

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
        tb.item_append("", "Close", self.iw_close, iw, obt)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

    def sys_cb(self, tb, tbi):
        item = self.sysgl.selected_item_get()
        if item:
            path = item.data["fullpath"]
            name = item.data["name"]
            newpath = "%s%s.desktop" %(LOCAL, name)
            if not os.path.exists(newpath):
                Exe("cp '%s' '%s'" %(path, LOCAL))
                sleep(5)
                self.add_files(self.maingl, newpath)


#----------------------EDITOR/CREATOR LAUNCHER
    def editor(self, tb, tbi, vbox):
        item = self.maingl.selected_item_get()
        if item:
            if 'fullpath' in item.data:
                self.editor_core(vbox, item)

    def creator(self, tb, tbi, vbox):
        self.editor_core(vbox)

    def editor_core(self, vbox, item=False, notify=False):
        def new():
            num = '0123456789'
            dest = "%sdefault" %LOCAL
            copy = dest[:]
            for x in num:
                dest.strip('-0123456789')
                dest = dest + "-" + x
                newpath = "%s.desktop" %dest
                if not os.path.exists(newpath):
                    Exe("echo '[Desktop Entry]' > %s" %newpath)
                    Exe("echo 'Name=Default' >> %s" %newpath)
                    break
                else:
                    dest = copy
            return newpath

        if notify:
            notify.delete()

        if item:
            self.item = item
            if not type(item) is str:
                path = item.data['fullpath']
            else:
                path = item
        else:
            path = dest = new()
            sleep(10)
            pathname = os.path.basename(path)
            pathname = os.path.splitext(pathname)[0]

        name  = "";gen   = "";exe   = "";icon  = "";mime  = "";cat   = "";com   = "";hide  = "";nodis = "";start = "";term  = ""
        h = self.h = "false";n = self.n = "false";s = self.s = "false";t = self.t = "false"

        with open(path) as file:
            deskfile = file.readlines()

        for x in deskfile:
            if "Name=" in x and not "GenericName=" in x:
                name = x.split("=")[-1]
                break
        for x in deskfile:
            if "Exec=" in x:
                exe  = x.split("=")[-1]
                break
        for x in deskfile:
            if "GenericName=" in x:
                gen  = x.split("=")[-1]
                break
        for x in deskfile:
            if "Comment=" in x:
                com  = x.split("=")[-1]
                break
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

        del(deskfile)

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
        if not ic.standard_set(icon):
            ic.standard_set("none")
        ic.size_hint_weight_set(1.0, 1.0)
        ic.size_hint_align_set(-1.0, -1.0)
        ib.pack_end(ic)
        ic.show()

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
        self.a = hs.item_add('Accessories'); self.d = hs.item_add('Preferences'); self.e = hs.item_add('Programming'); self.f = hs.item_add('Education'); self.g = hs.item_add('Games'); self.b = hs.item_add('Graphics'); self.c = hs.item_add('Internet'); self.h = hs.item_add('Sound & Video'); self.i = hs.item_add('Office'); self.j = hs.item_add('System Tools');
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

        if not item:
            fil = elm.Box(self.win)
            fil.size_hint_weight_set(1.0, 1.0)
            fil.size_hint_align_set(-1.0, -1.0)
            vbox.pack_end(fil)
            fil.show()

        lbb = elm.Box(self.win)
        lbb.horizontal_set(True)
        lbb.size_hint_weight_set(1.0, 1.0)
        lbb.size_hint_align_set(-1.0, -1.0)
        lbb.show()
        vbox.pack_end(lbb)

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
            en.text = pathname
            en.editable_set(True)
        en.single_line = True
        en.scrollable_set(True)
        en.size_hint_weight_set(1.0, 1.0)
        en.size_hint_align_set(-1.0, -1.0)
        lbb.pack_end(en)
        en.show()

        chks = elm.Box(self.win)
        chks.horizontal_set(True)
        chks.size_hint_weight_set(1.0, 1.0)
        chks.size_hint_align_set(-1.0, -1.0)
        chks.show()
        vbox.pack_end(chks)

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
            bt.callback_clicked_add(self.manual_win, path, vbox, item)
            btnb.pack_end(bt)
            bt.show()

        tb = elm.Toolbar(self.win)
        tb.size_hint_weight_set(1.0, 0.0)
        tb.size_hint_align_set(-1.0, -1.0)
        if item:
            tb.item_append("", "Done", self.editor_save, vbox)
            tb.item_append("", "Cancel", self.editor_close, vbox)
        else:
            tb.item_append("", "Create", self.creator_create, vbox, dest)
            tb.item_append("", "Cancel", self.editor_close, vbox, dest)
        tb.homogeneous_set(True)
        tb.select_mode_set(2)
        vbox.pack_end(tb)
        tb.show()

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

        vbox.delete()

        vbox = elm.Box(self.win)
        self.win.resize_object_add(vbox)
        self.win.resize(410, 503)
        vbox.padding_set(0 , 5)
        vbox.size_hint_weight_set(1.0, 1.0)
        vbox.show()

        self.separator(vbox)

        self.file_viewer(path, vbox)

    def editor_save(self, tb, tbi, vbox=False):
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
                data = self.return_new(data, repl, x, y)
        for i, line in enumerate(data):
            data[i]= line.encode('utf-8')
        with open(path, 'w') as file:
            file.writelines(data)

        #~ Exe("update-desktop-database")

        if vbox:
            vbox.delete()
            self.vipbox()

    def creator_create(self, tb, tbi, vbox, path):
        new = self.line_list()
        dest = self.dtfp.entry_get()
        dest = "%s%s.desktop"%(LOCAL, dest)

        with open(path) as file:
            data = file.readlines()
        data[1] = new[0]
        del new[0]
        data.extend(new)

        with open(path, 'w') as file:
            file.writelines(data)

        if not dest == path:
            Exe("mv '%s' '%s'" %(path, dest))
            sleep(5)

        vbox.delete()
        self.vipbox()
        #~ Exe("update-desktop-database -q")

    def editor_close(self, tb, tbi, vbox, dest=False):
        if dest:
            Exe("rm '%s'" %dest)
            sleep(3)
        vbox.delete()
        self.vipbox()

    def delay(self, tb, tbi, vbox):
        tb.disabled_set(True)
        n = elm.Notify(self.win)
        n.orient = 1
        n.allow_events_set(False)
        n.show()

        Timer(1.5, self.editor_core, vbox, self.item, n)


#----------------------EDITOR/CREATOR INFO RETRIEVAL
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


#----------------------REMOVAL POPUP
    def rm_popup(self, tb, tbi):
        item = self.maingl.selected_item_get()
        if not item:
            return
        elif 'fullpath' in item.data:
            popup = self.rmp = elm.Popup(self.win)
            popup.size_hint_weight = (1.0, 1.0)
            popup.text = "<b>Confirmation</><br><br>Click <i>Delete</i> if you wish to delete the launcher. Otherwise, click <i>Cancel</i>."
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
    def file_viewer(self, path, vbox, iw=False):
        if iw:
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
            ic = self.ic = elm.Icon(self.win)
            if not ic.standard_set(icon):
                ic.standard_set("none")
            ic.size_hint_weight_set(1.0, 1.0)
            ic.size_hint_align_set(-1.0, -1.0)
            ic.show()
            ib.pack_end(ic)
        else:
            self.fullpath = path
            with open(path) as file:
                data = file.readlines()
            for i, x in enumerate(data):
                try:
                    x = x.encode('utf-8')
                except:
                    del data[i]
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

        if iw:
            man.autosave_set(False)
            man.editable_set(False)
            tb.item_append("", "Close", self.iw_close, iw)
        else:
            man.autosave_set(True)
            man.editable_set(True)
            tb.item_append("", "Done", self.delay, vbox)

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
        if 'fullpath' in item.data:
            path = item.data['fullpath']

            box = elm.Box(self.win)
            box.padding_set(0 , 5)
            box.size_hint_weight_set(1.0, 1.0)
            box.show()

            iw = elm.InnerWindow(self.win)
            iw.content_set(box)
            iw.show()
            iw.activate()

            self.file_viewer(path, box, iw)
