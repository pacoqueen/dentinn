#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Verificar rutas y demás (que existan, que no estén a "", capturar 
#       excepciones, etc.). 
# TODO: Implementar los diálogos de buscar destino y buscar compartido.

"""
Backup de dentinn_v2.
1.- Hace un backup de la BD.
2.- Comprime el contenido del directorio compartido (documentos, imágenes y 
    plantillas)
3.- Guarda la copia de la BD y el comprimido de compartido en un archivador 
    tar.bz2 en el archivo de destino elegido por el usuario.
"""

import os, sys
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

import pygtk, gtk, gtk.glade
import tempfile

class W:
    def __init__(self, widgets):
        self.w = widgets

    def __getitem__(self, key):
        res = self.w.get_widget(key)
        return res

class VentanaBackup:
    def __init__(self):
        self.__build_widgets()
        self.__conectar_widgets()
        self.wids['ventana'].show()

    def __build_widgets(self):
        """
        Construye la ventana GTK con el entry de las opciones para la copia 
        de la BD, el del directorio compartido y el de fichero de destino.
        También introduce los valores por defecto.
        """
        self.widgets = gtk.glade.XML("backup.glade")
        self.wids = W(self.widgets)
        compartido = os.path.join(".", "compartido")
        self.wids['e_compartido'].set_text(compartido)
        #destino = os.path.join(os.environ["HOME"], "dinn2bak.tar.bz2")
        filedest = "dinn2bak.tar.bz2"
        try:
            homedestino = os.path.join(os.environ["HOME"], filedest)
        except KeyError:
            homedestino = os.path.join(os.environ['HOMEPATH'], "Desktop")
        destino = os.path.join(homedestino, filedest)
        self.wids['e_destino'].set_text(destino)
        self._buscar_valores_defecto_bd()

    def _buscar_valores_defecto_bd(self):
        conf = os.path.join(".", "framework", "ginn.conf")
        user = "udentinn2"
        passwd = "passudentinn2"
        dbname = "dbdentinn2"
        host = "localhost"
        try:
            fconf = open(conf)
        except:
            pass
        else:
            d = {}
            for l in fconf.readlines():
                try:
                    k, v = l.split()[:2]
                except:
                    continue
                d[k] = v
            if "user" in d:
                user = d["user"]
            if "pass" in d:
                passwd = d["pass"]
            if "dbname" in d:
                dbname = d["dbname"]
            if "host" in d:
                host = d["host"]
        self.wids['e_usuario'].set_text(user)
        self.wids['e_password'].set_text(passwd)
        self.wids['e_nombrebd'].set_text(dbname)
        self.wids['e_host'].set_text(host)

    def __conectar_widgets(self):
        self.wids['b_compartido'].connect("clicked", self.buscar_compartido)
        self.wids['b_destino'].connect("clicked", self.buscar_destino)
        self.wids['b_salir'].connect("clicked", self.salir)
        self.wids['b_empezar'].connect("clicked", self.comenzar)
        self.wids['ventana'].connect("destroy", self.salir)

    def buscar_compartido(self, boton):
        pass

    def buscar_destino(self, boton):
        pass

    def salir(self, boton_o_evento):
        gtk.main_quit()

    def comenzar(self, boton):
        self.wids['progreso'].set_fraction(0.0)
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending():
            gtk.main_iteration(False)
        bsql = self.bak_bd()
        while gtk.events_pending():
            gtk.main_iteration(False)
        bdir = self.bak_compartido()
        while gtk.events_pending():
            gtk.main_iteration(False)
        self.tar_bak(bsql, bdir)
        while gtk.events_pending():
            gtk.main_iteration(False)
        self.wids['ventana'].window.set_cursor(None)
        while gtk.events_pending():
            gtk.main_iteration(False)
        self.dialogo_fin()

    def dialogo_fin(self):
        dialog = gtk.Dialog("COPIA DE SEGURIDAD COMPLETADA",
                    self.wids['ventana'],
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(gtk.Label(
        "\n"*3 + " "*8 + "Copia de seguridad completada." + " "*8 + "\n"*3))
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()

    def bak_bd(self):
        u = self.wids['e_usuario'].get_text()
        p = self.wids['e_password'].get_text()
        b = self.wids['e_nombrebd'].get_text()
        h = self.wids['e_host'].get_text()
        dest = os.path.join(tempfile.gettempdir(), "bak.sql")
        #comando = "pg_dump %s -U %s -h %s -W > %s" % (b, u, h, dest)
        #comando = "pg_dump %s > %s" % (b, dest)
        pg_dump = "pg_duip"
        pg_dump = '"C:\\Program Files\\PostgreSQL\\8.2\\bin\\pg_dump.exe"'
        comando = "%s %s -U %s > %s" % (pg_dump, b, u, dest)
        os.system(comando)
        #import subprocess
        #pg_dump = subprocess.Popen(comando, stdin = subprocess.PIPE)
        #pg_dump.comunicate(p)
        #pg_dump.wait()
        self.wids['progreso'].set_fraction(0.33)
        return dest

    def bak_compartido(self):
        dest = os.path.join(tempfile.gettempdir(), "bak.tar")
        origen = self.wids['e_compartido'].get_text()
        import tarfile
        tardest = tarfile.open(dest, 'w')
        tardest.add(origen)
        tardest.close()
        self.wids['progreso'].set_fraction(0.66)
        return dest
    
    def tar_bak(self, baksql, baktar):
        #import bz2
        dest = self.wids['e_destino'].get_text()
        #bzdest = bz2.BZ2File(dest, 'w')
        import tarfile
        bzdest = tarfile.open(dest, 'w:bz2')
        bzdest.add(baksql)
        bzdest.add(baktar)
        bzdest.close()
        self.wids['progreso'].set_fraction(1)


if __name__ == "__main__":
    v = VentanaBackup()
    gtk.main()

