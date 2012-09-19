#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2007 Francisco José Rodríguez Bogado                          #
#                    (pacoqueen@users.sourceforge.net)                        #
#                                                                             #
# This file is part of Dent-Inn.                                              #
#                                                                             #
# Dent-Inn is free software; you can redistribute it and/or modify            #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# Dent-Inn is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with Dent-Inn; if not, write to the Free Software                     #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

version = '3.0.2 RC (gran_plaza)'
version_info = tuple(
    [int(num) for num in version.split()[0].split('.')] + 
    [txt.replace("(", "").replace(")", "") for txt in version.split()[1:]]
    )

import pygtk
pygtk.require('2.0')
import sys, os
from ventana import Ventana
import utils
import gtk, gtk.glade, time, mx, mx.DateTime
try:
    import pclases
    from seeker import VentanaGenerica 
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
    from seeker import VentanaGenerica 
from utils import _float as float

SHOW_DENTIGRAMA = pclases.DEBUG #XXX BUGFIX: El dentigrama da problemas.

class Pacientes(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.Paciente
        self.dic_campos = {#"codigo": "e_codigo", 
                           "nombre": "e_nombre", 
                           "domicilio": "e_domicilio", 
                           "telefono": "e_telefono",
                           "cp": "e_codigo_postal", 
                           "poblacion": "e_poblacion", 
                           "provincia": "e_provincia", 
                           "alergias": "e_alergias", 
                           "padecimientos": "e_padecimientos", 
                           "observaciones": "txt_observaciones", 
                           "protesis": "txt_protesis", 
                           "dni": "e_dni", 
                           "motivoConsulta": "txt_motivo", 
                           "pAlergias": "txt_alergias", 
                           "patologiasOtroNivel": "txt_patologias", 
                           "medicacion": "txt_medicacion", 
                           "cirugias": "txt_cirugias", 
                           "primeraVez": "txt_primera_vez", 
                           "seguidoAlgunTratamiento": "txt_algun_tratamiento", 
                           "cualYDuranteCuantoTiempo": "txt_cual_y_durante", 
                           "actividadLaboral": "txt_actividad", 
                           "deportes": "txt_deportes", 
                           "coloracion": "e_coloracion", 
                           "temperatura": "e_temperatura", 
                           "edema": "e_edema", 
                           "ampollas": "e_ampollas", 
                           "queratopatias": "e_queratopatias", 
                           "infecciones": "e_infecciones", 
                           "anhidrosis": "e_anhidrosis", 
                           "hiperhidrosis": "e_hiperhidrosis", 
                           "bromhidrosis": "e_bromhidrosis", 
                           "onicodistrofias": "e_onicodistrofias", 
                           "onicogrifosis": "e_onicogrifosis", 
                           "oniquia": "e_oniquia", 
                           "paroniquia": "e_paroniquia", 
                           "modificacionColor": "e_modificacion_color", 
                           "desprendimiento": "e_desprendimiento", 
                           "tumoresUngueales": "e_tumores", 
                           "estriacionesTransversal": "e_transversal", 
                           "estriacionesLongitudinal": "e_longitudinal", 
                           "hiperqueratosis": "e_hiperqueratosis", 
                           "helomas": "e_helomas", 
                           "alteraciones": "e_alteraciones", 
                           "horizontal": "e_horizontal", 
                           "frontal": "e_vertical", 
                           "valoracionArticular": "e_valoracion", 
                           "enCarga": "e_en_carga", 
                           "movilizacion": "e_movilizacion", 
                           "primerRadio": "e_primer_radio", 
                           "exploracionMarcha": "txt_exploracion", 
                           "diagnostico": "txt_diagnostico", 
                           "tratamiento": "txt_tratamiento",
                          }
        Ventana.__init__(self, 'dentinn.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar, 
                       'b_fecha_nacimiento/clicked': self.set_fechaNac, 
                       'b_anterior/clicked': self.anterior, 
                       'b_siguiente/clicked': self.siguiente, 
                       'b_primero/clicked': self.primero, 
                       'b_ultimo/clicked': self.ultimo,
                       'b_ir_a/clicked': self.ir_a_pos, 
                       'b_add_tratamiento/clicked': self.add_cita, 
                       'b_drop_tratamiento/clicked': self.drop_cita,
                       'b_add_presupuesto/clicked': self.add_presupuesto, 
                       'b_drop_presupuesto/clicked': self.drop_presupuesto, 
                       'b_add_foto/clicked': self.add_foto, 
                       'b_drop_foto/clicked': self.drop_foto, 
                       'b_print_foto/clicked': self.print_foto, 
                       'b_abrir_autorizacion/clicked': self.abrir_documento, 
                       'b_abrir_correspondencia/clicked': self.abrir_documento, 
                       'b_abrir_otros/clicked': self.abrir_documento, 
                       'b_borrar_autorizacion/clicked': self.drop_documento, 
                       'b_borrar_correspondencia/clicked': self.drop_documento, 
                       'b_borrar_otros/clicked': self.drop_documento, 
                       'b_ortodoncia/clicked': self.new_doc, 
                       'b_radicular/clicked': self.new_doc, 
                       'b_anestesia/clicked': self.new_doc, 
                       'b_cirugia/clicked': self.new_doc,
                       'b_plantilla/clicked': self.new_doc, 
                       'b_blanco/clicked': self.new_doc, 
                       'b_presupuesto/clicked': self.new_doc, 
                       'b_factura/clicked': self.new_doc, 
                       'b_imprimir_datos/clicked': self.print_datos, 
                       'b_imprimir_tratamientos/clicked': self.print_tratamientos, 
                       'b_podo/clicked': self.imprimir_podologia 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def print_datos(self, boton):
        txt = ('Código             : ' + `self.objeto.codigo`, 
               'Nombre             : ' + self.objeto.nombre, 
               'Teléfono           : ' + self.objeto.telefono, 
               'Domicilio          : ' + self.objeto.domicilio, 
               'Población          : ' + self.objeto.poblacion, 
               'Provincia          : ' + self.objeto.provincia, 
               'Profesión          : ' + self.objeto.profesion, 
               'Fecha de nacimiento: ' + utils.str_fecha(self.objeto.fechaNac), 
               'Padecimientos      : ' + self.objeto.padecimientos, 
               'Código postal      : ' + self.objeto.cp, 
               'Alergias           : ' + self.objeto.alergias, 
               'Observaciones      : ' + self.objeto.observaciones, 
               'Prótesis           : ' + self.objeto.protesis)
        txt = "\n".join(txt)
        import geninformes
        from informes import abrir_pdf
        abrir_pdf(geninformes.texto_libre(txt, "Datos del paciente"))

    def print_tratamientos(self, boton):
        self.wids['tv_tratamientos'].grab_focus()
        self.wids['notebook'].set_current_page(2)
        coldiente = self.wids['tv_tratamientos'].get_column(0)
        coldiente.set_min_width(coldiente.get_width() + 50)
        while gtk.events_pending(): gtk.main_iteration(False)
        from informes import abrir_pdf
        from treeview2pdf import treeview2pdf
        pdf = treeview2pdf(self.wids['tv_tratamientos'], 
                           "Tratamientos", 
                           self.objeto.nombre, 
                           apaisado = False, 
                           marco = False, 
                           logo = False)
        #pdf = treeview2pdf(self.wids['tv_tratamientos'], "Tratamientos", mx.DateTime.localtime(), apaisado = False)
        if pdf != None:
            abrir_pdf(pdf)
        self.wids['notebook'].set_current_page(5)
        boton.grab_focus()

    def abrir_documento(self, boton):
        if "autorizacion" in boton.name:
            tv = self.wids['tv_autorizaciones']
        elif "correspondencia" in boton.name:
            tv = self.wids['tv_correspondencia']
        elif "otros" in boton.name:
            tv = self.wids['tv_otros']
        else:
            return
        model, paths = tv.get_selection().get_selected_rows()
        if (paths != None and paths != []): 
            for path in paths:
                id = model[path][-1]
                documento = pclases.Documento.get(id)
                import mod_informes
                mod_informes.abrir_documento(documento.get_ruta_completa())

    def drop_documento(self, boton):
        if "autorizacion" in boton.name:
            tv = self.wids['tv_autorizaciones']
        elif "correspondencia" in boton.name:
            tv = self.wids['tv_correspondencia']
        elif "otros" in boton.name:
            tv = self.wids['tv_otros']
        else:
            return
        model, paths = tv.get_selection().get_selected_rows()
        if (paths != None and paths != [] and
            utils.dialogo(titulo = "BORRAR DOCUMENTOS", 
                          texto = "Se eliminarán los documentos seleccionados.\n¿Está seguro?", 
                          padre = self.wids['ventana'])):
            for path in paths:
                id = model[path][-1]
                documento = pclases.Documento.get(id)
                mover_a_papelera(documento)
                documento.destroySelf()
            self.rellenar_documentos()

    def new_doc(self, boton):
        if "ortodoncia" in boton.name:
            plantilla = "ortodoncia"
        elif "radicular" in boton.name:
            plantilla = "canal"
        elif "anestesia" in boton.name:
            plantilla = "anestesia"
        elif "cirugia" in boton.name:
            plantilla = "cirugia"
        elif "plantilla" in boton.name:
            plantilla = "correspondencia"
        elif "blanco" in boton.name:
            plantilla = "blanco"
        elif "presupuesto" in boton.name:
            plantilla = "presupuesto"
        elif "factura" in boton.name:
            plantilla = "factura"
        else:
            return
        if self.objeto:
            nombre = utils.dialogo_entrada(titulo = "NOMBRE", 
                                           texto = "Introduza un nombre para almacenar el documento:", 
                                           padre = self.wids['ventana'], 
                                           valor_por_defecto = "%s_%s" % (plantilla, mx.DateTime.localtime().strftime("%Y%m%d")))
            if nombre != None and nombre.strip() != "":
                nombre = nombre.strip()
                if nombre in [d.ruta[-4] == "." and d.ruta[:-4] or d.ruta for d in self.objeto.documentos]:
                    utils.dialogo_info(titulo = "DUPLICADO", 
                                       texto = "El documento %s ya existe. Use otro nombre." % nombre, 
                                       padre = self.wids['ventana'])
                else:
                    documento = self.new_doc_plantilla(nombre, plantilla)
                    self.rellenar_documentos()
                    if documento != None:
                        import mod_informes
                        mod_informes.abrir_documento(documento.get_ruta_completa())

    def new_doc_plantilla(self, nombre, plantilla):
        """
        Crea un nuevo documento según la plantilla recibida.
        """
        paciente = self.objeto
        documento = None
        if paciente != None:
            from mod_informes import nuevo_doc, combinar_sxw
            if plantilla in ("ortodoncia", "canal", "anestesia", "cirugia"):
                tipo = 1
            elif plantilla in ("correspondencia"):
                tipo = 2
            else:
                tipo = 3
            documento = nuevo_doc(self.objeto, plantilla = plantilla, nombre = nombre, tipo = tipo)
            func_cambios = getattr(self, "preguntar_cambios_%s" % plantilla)
            cambios = func_cambios()
            if cambios != None:
                error = combinar_sxw(cambios, documento)
                if error < 0:
                    utils.dialogo_info(titulo = "ERROR", 
                                       texto = "El documento no se pudo crear.", 
                                       padre = self.wids['ventana'])
            if cambios == None or error < 0:
                mover_a_papelera(documento)
                documento.destroySelf()
                documento = None
        return documento

    def preguntar_cambios_presupuesto(self):
        cambios = {'[NOMBRE]': ("", "", self.objeto.nombre),
                   '[CODIGO]': ("", "", str(self.objeto.codigo)), 
                   '[LINEAS]': ("", "", "".join(["""%s: %s \xe2\x82\xac</text:p><text:p text:style-name="P7">""" 
                                                 % (p.concepto, utils.float2str(p.importe, 0))
                                                 for p in self.objeto.presupuestos])), 
                   '[TOTAL]': ("", "", "%s €" % utils.float2str(sum([p.importe for p in self.objeto.presupuestos]), 0)), 
                   '[FECHA]': ("FECHA", "Fecha:", utils.str_fecha(mx.DateTime.localtime()))}
        return self.aplicar_a_dialogos_entrada(cambios, ())

    def preguntar_cambios_factura(self):
        cambios = {'[NOMBRE]': ("", "", self.objeto.nombre),
                   '[DOMICILIO]': ("", "", self.objeto.domicilio), 
                   '[POBLACION]': ("", "", self.objeto.poblacion), 
                   '[DNI]': ("", "", self.objeto.dni), 
                   '[FECHA]': ("", "", utils.str_fecha(mx.DateTime.localtime()))} 
        return self.aplicar_a_dialogos_entrada(cambios, ())

    def preguntar_cambios_canal(self):
        cambios = {'[NOMBRE]': ("NOMBRE", "Introduzca nombre del paciente:", self.objeto.nombre),
                   '[FECHA]': ("FECHA", "Fecha:", utils.str_fecha(mx.DateTime.localtime())),
                   '[DIENTE]': ("DIENTE", "Introduzca diente:", "")
                  }
        orden = ("[DIENTE]", )
        return self.aplicar_a_dialogos_entrada(cambios, orden)

    def preguntar_cambios_blanco(self):
        return self.aplicar_a_dialogos_entrada({}, ())

    def preguntar_cambios_correspondencia(self):
        cambios = {'[NOMBRE]': ("NOMBRE", "Introduzca nombre del paciente:", self.objeto.nombre),
                   '[DIRECCION]': ("DOMICILIO", "Domicilio:", self.objeto.domicilio),
                   '[CP]': ("CÓDIGO POSTAL", "Código postal:", self.objeto.cp),
                   '[PROVINCIA]': ("PROVINCIA", "Provincia:", self.objeto.provincia),
                   '[CIUDAD]': ("CIUDAD", "Población:", self.objeto.poblacion)}
        orden = ()
        return self.aplicar_a_dialogos_entrada(cambios, orden)


    def preguntar_cambios_ortodoncia(self):
        cambios = {'[NOMBRE]': ("NOMBRE", "Nombre del paciente:", self.objeto.nombre),
                   '[FECHA]': ("FECHA", "Fecha:", utils.str_fecha(mx.DateTime.localtime())),
                   '[CANTIDAD]': ("CANTIDAD INICIAL", "Introduzca cantidad inicial", ""),
                   '[MENSUALIDAD]': ("MENSUALIDAD", "Cantidad mensual:", 
                                        (lambda p, c, m: (utils._float(p) - utils._float(c)) / utils._float(m), 
                                         ("[PRESUPUESTO]", "[CANTIDAD]", "[MESES]"))),
                   '[MESES]': ("MESES", "Número de meses", ""), 
                   '[PRESUPUESTO]': ("PRESUPUESTO", "Presupuesto total:", ""),
                   '[NOMBREPACIENTE]': ("NOMBRE", "Nombre del paciente en la firma:", self.objeto.nombre),
                   '[FECHAFIRMA]': ("FECHA FIRMA", "Fecha de la firma:", utils.str_fecha(mx.DateTime.localtime()))
                  }
        orden = ("[CANTIDAD]", "[PRESUPUESTO]", "[MESES]", "[MENSUALIDAD]", "[NOMBREPACIENTE]", "[FECHAFIRMA]")
        return self.aplicar_a_dialogos_entrada(cambios, orden)

    def preguntar_cambios_cirugia(self):
        cambios = {'[NOMBRE]': ("NOMBRE", "Nombre del paciente:", self.objeto.nombre),
                   '[DIENTE]': ("DIENTE", "Diente:", ""),
                   '[FECHA]': ("FECHA", "Fecha de la firma:", utils.str_fecha(mx.DateTime.localtime()))}
        #orden = cambios.keys()
        orden = ("[DIENTE]", "[FECHA]", )
        return self.aplicar_a_dialogos_entrada(cambios, orden)

    def preguntar_cambios_anestesia(self):
        """
        Diálogos de entrada para introducir los datos 
        que aparecerán con el documento.
        Devuelve un diccionario con las claves de la 
        plantilla y el texto sustituto.
        Devuelve None si se cancela algún diálogo.
        """
        # Este diccionario irá cambiando los valores por la respuesta del diálogo. Hasta ese momento 
        # tiene una lista con el título de la ventana, texto y valor por defecto. Las preguntas se 
        # harán en el orden definido por la tupla «orden».
        # Si algún valor no debe preguntarse, basta con sacarlo de la tupla «orden» para ignorarlo 
        # y devolverlo tal cual aparezca en el valor por defecto (d[k][2]).
        cambios = {'[NOMBRE]': ("NOMBRE", "Nombre del paciente:", self.objeto.nombre),
                   '[EDAD]': ("EDAD", "Edad en el momento de la autorización:", str(self.objeto.calcular_edad())), 
                   '[CIUDAD]': ("CIUDAD", "Ciudad:", self.objeto.poblacion), 
                   '[DIRECCION]': ("DIRECCIÓN", "Dirección:", self.objeto.domicilio), 
                   '[DNI]': ("DNI", "DNI:", self.objeto.dni),
                   '[OBSERVACIONES]': ("OBSERVACIONES", "Observaciones:", ""), 
                   '[DIA]': ("DÍA", "Día de la fecha:", str(mx.DateTime.localtime().day)), 
                   '[MES]': ("MES", "Mes de la fecha:", utils.corregir_nombres_fecha(mx.DateTime.localtime().strftime("%B"))),
                   '[ANO]': ("AÑO", "Año de la fecha:", str(mx.DateTime.localtime().year))}
        #orden = cambios.keys()
        orden = ("[OBSERVACIONES]", )
        return self.aplicar_a_dialogos_entrada(cambios, orden)

    def aplicar_a_dialogos_entrada(self, cambios, orden):
        """
        cambios es un diccionario donde se almacenan las respuestas.
        orden es una tupla de claves del diccionario con el orden en que 
        deben ir apareciendo los diálogos de entrada. En el momento en que 
        se cancela alguno se devuelve None y se ignoran el resto.
        Ver el formato del diccionario de preguntas en «preguntar_cambios_anestesia».
        Si el tercer elemento de la lista es una lista o una tupla, se 
        considera que el valor por defecto es el resultado de evaluar una
        función. Para ello el primer elemento de esta tupla será la 
        función y el segundo la lista de claves del diccionario que conformarán 
        los parámetros. Es imprescindible que ya hayan sido recogidos 
        por sus diálogos, por lo que su posición en la lista «orden» es 
        importante. El resultado que dé será el que se muestre por defecto.
        """
        for k in [k for k in cambios.keys() if k not in orden]: # Valores que no hay que preguntar
            cambios[k] = cambios[k][2]
        for k in orden:
            v = cambios[k]
            if (isinstance(v[2], tuple) or isinstance(v[2], list)) and isinstance(v[2][0], type(lambda: None)):
                try:
                    valor = v[2][0](*[cambios[i] for i in v[2][1]])
                except Exception, msg:
                    print "pacientes.py::aplicar_a_dialogos_entrada -> No se pudo evaluar expresión. %s" % msg
                    valor = ""
                else:
                    if isinstance(valor, type(1.0)):    # float no es la clase, sino utils._float debido a la forma de importar la función.
                        valor = "%s €" % utils.float2str(valor, autodec = True)
                    elif insintance(valor, int):
                        valor = `valor`
                    else:
                        valor = str(valor)
            else:
                valor = v[2]
            resp = utils.dialogo_entrada(titulo = v[0], 
                                        texto = v[1], 
                                        padre = self.wids['ventana'], 
                                        valor_por_defecto = valor)
            if resp == None:
                cambios = None
                break
            cambios[k] = resp
        return cambios

    def add_foto(self, b):
        """
        Muestra un diálogo de abrir ficheros de tipo imagen.
        La imagen devuelta es almacenada en un servidor de archivos y 
        la ruta a la misma en la base de datos junto con un nombre que 
        se pedirá mediante un diálogo.
        """
        # En realidad en la BD únicamente almacenaremos el nombre de la foto. Se le 
        # antepondrá una ruta relativa "harcoded" para evitar conflictos con los separadores 
        # de directorios de los diferentes sistemas operativos. Si se guardara en formato UNIX 
        # habría después que reinterpretarlo y adaptarlo a la nomenclatura L:\dir\ de Windows.
        # Y viceversa.
        # Es mejor guardar solo el nombre del archivo y acceder con ruta relativa ya que el 
        # directorio de la aplicación se exporta desde un servidor de ficheros a los clientes.
        ruta = browse_for_image()
        if ruta and self.objeto:
            import shutil
            ruta_destino = pclases.Fotografia.ruta_completa(self.objeto, ruta)
            if ruta_destino not in [f.get_ruta_completa() for f in self.objeto.fotografias]:
                shutil.copy(ruta, ruta_destino)
                nuevafoto = pclases.Fotografia(paciente = self.objeto, 
                                               nombre = os.path.split(ruta)[-1], 
                                               ruta = os.path.basename(ruta))
                self.rellenar_fotografias()
                model = self.wids['tv_fotos'].get_model()
                for path in range(len(model)):
                    if model[path][-1] == nuevafoto.id:
                        self.wids['tv_fotos'].set_cursor(path)
            else:
                utils.dialogo_info(titulo = "DUPLICADA", 
                                   texto = "La foto %s ya existe. Renombre el archivo." % ruta_destino, 
                                   padre = self.wids['ventana'])
                # TODO: Podría usar un dialogo sí/no y renombrarla yo mismo, o comparar fechas y machacar.

    def print_foto(self, b):
        """
        Muestra un diálogo de impresión. Necesita pygtk 2.10.
        """
        model, paths = self.wids['tv_fotos'].get_selection().get_selected_rows()
        if (paths != None and paths != []):
            for path in paths:
                idfoto = model[path][-1]
                foto = pclases.Fotografia.get(idfoto)
                self.mostrar_dialogo_imprimir(foto)

    def mostrar_dialogo_imprimir(self, foto):
        settings = None
        def do_print(settings):
            printop = gtk.PrintOperation()
            if settings != None: 
                printop.set_print_settings(settings)
            #printop.connect("begin_print", begin_print)
            #printop.connect("draw_page", draw_page)
            printop.connect("begin_print", lambda *args, **kw: None)
            printop.connect("draw_page", lambda *args, **kw: None)
            res = printop.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, self.wids['ventana'])
            if res == gtk.PRINT_OPERATION_RESULT_APPLY:
                settings = printop.get_print_settings()
        do_print(settings)

    def drop_foto(self, b):
        """
        Elimina las fotos seleccionadas de la BD y almacena 
        la foto del servidor de ficheros en el directorio 
        temporal local de la máquina del usuario.
        """
        model, paths = self.wids['tv_fotos'].get_selection().get_selected_rows()
        if (paths != None and paths != [] and
            utils.dialogo(titulo = "BORRAR IMÁGENES", 
                          texto = "Se eliminarán las fotos seleccionadas.\n¿Está seguro?", 
                          padre = self.wids['ventana'])):
            for path in paths:
                idfoto = model[path][-1]
                foto = pclases.Fotografia.get(idfoto)
                mover_a_papelera(foto)
                foto.destroySelf()
            self.rellenar_fotografias()

    def add_cita(self, boton):
        if self.objeto != None:
            nuevacita = pclases.Cita(paciente = self.objeto)
            self.rellenar_tabla_tratamientos()
            scroll_a_fila_nueva(self.wids['tv_tratamientos'], nuevacita.id)

    def drop_cita(self, boton):
        model, paths = self.wids['tv_tratamientos'].get_selection().get_selected_rows()
        if (paths != None and paths != [] and
            utils.dialogo(titulo = "BORRAR TRATAMIENTOS", 
                          texto = "Se eliminarán las citas seleccionadas.\n¿Está seguro?", 
                          padre = self.wids['ventana'])):
            for path in paths:
                idcita = model[path][-1]
                cita = pclases.Cita.get(idcita)
                cita.destroySelf()
            self.rellenar_tabla_tratamientos()

    def add_presupuesto(self, boton):
        if self.objeto != None:
            nuevopresupuesto = pclases.Presupuesto(paciente = self.objeto)
            self.rellenar_tabla_presupuestos()
            scroll_a_fila_nueva(self.wids['tv_presupuestos'], 
                                nuevopresupuesto.id, 
                                0)

    def drop_presupuesto(self, boton):
        model, paths = self.wids['tv_presupuestos'].get_selection().get_selected_rows()
        if (paths != None and paths != [] and
            utils.dialogo(titulo = "BORRAR PRESUPUESTOS", 
                          texto = "Se eliminarán las líneas seleccionadas.\n¿Está seguro?", 
                          padre = self.wids['ventana'])):
            for path in paths:
                idpresupuesto = model[path][-1]
                presupuesto = pclases.Presupuesto.get(idpresupuesto)
                presupuesto.destroySelf()
            self.rellenar_tabla_presupuestos()

    def ir_a_pos(self, boton):
        """
        Va al paciente que ocupe la posición tecleada 
        por el usuario.
        """
        pos = utils.dialogo_entrada(titulo = "IR A POSICIÓN", 
                                    texto = "Teclee una posición entre 1 y %d" % pclases.Paciente.select().count(), 
                                    padre = self.wids['ventana'])
        if pos != None:
            try:
                pos = int(pos)
            except:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = 'El texto tecleado "%s" no es un número.' % pos, 
                                   padre = self.wids['ventana'])
            else:
                pos = min(pos, pclases.Paciente.select().count())
                pos = max(pos, 1)
                pos -= 1
                self.ir_a(pclases.Paciente.select(orderBy = "id")[pos])

    def anterior(self, boton):
        if self.objeto != None:
            #self.objeto.make_swap()
            pos = buscar_pos_paciente(self.objeto) - 1
            if pos < 0:
                utils.dialogo_info(titulo = "PRIMER PACIENTE", 
                                   texto = "No hay pacientes anteriores al actual.", 
                                   padre = self.wids['ventana'])
            else:
                paciente = pclases.Paciente.select(orderBy = "id")[pos]
                self.objeto = None
                self.ir_a(paciente)
    
    def siguiente(self, boton):
        if self.objeto != None:
            #self.objeto.make_swap()
            pos = buscar_pos_paciente(self.objeto) + 1
            if pos > pclases.Paciente.select().count() - 1:
                utils.dialogo_info(titulo = "ÚLTIMO PACIENTE", 
                                   texto = "No hay pacientes posteriores al actual.", 
                                   padre = self.wids['ventana'])
            else:
                self.objeto = None
                paciente = pclases.Paciente.select(orderBy = "id")[pos]
                self.ir_a(paciente)

    def primero(self, boton):
        if pclases.Paciente.select().count() > 0:
            self.ir_a(pclases.Paciente.select(orderBy = "id")[0])

    def ultimo(self, boton):
        if pclases.Paciente.select().count() > 0:
            self.ir_a(pclases.Paciente.select(orderBy = "-id")[0])

    def set_fechaNac(self, boton):
        """
        Cambia la fecha de nacimiento y actualiza 
        el entry de la edad.
        """
        if self.objeto != None:
            tuplafecha = utils.mostrar_calendario(self.objeto.fechaNac, self.wids['ventana'])
            self.objeto.fechaNac = utils.parse_fecha("/".join([`i` for i in tuplafecha]))
            mostrar_edad(self.objeto, self.wids['e_edad'])
            self.guardar(None)

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        if self.objeto == None:
            igual = True
        else:
            igual = self.objeto != None
            for colname in self.dic_campos:
                col = self.clase.sqlmeta.columnDefinitions[colname]
                try:
                    valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                except (ValueError, mx.DateTime.RangeError, TypeError), msg:
                    igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if isinstance(col, pclases.SODateCol):
                    valor_objeto = utils.abs_mxfecha(valor_objeto)
                igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    break
        return not igual
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # TODO: Hasta que aprenda a usar el PrintOperation. Pista, hay que "dibujar" la foto en Cairo.
        # (http://www.islascruz.org/html/index.php?Blog/SingleView/id/Imprimiendo_usando_GTK)
        self.wids['b_print_foto'].set_property("visible", False)
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        self.init_tratamientos()
        self.init_presupuestos()
        self.init_fotografias()
        self.init_documentos()
        #utils.rellenar_lista(self.wids['cbe_proveedor'], [(p.id, p.nombre) for p in pclases.Proveedor.select(orderBy = "nombre")])
        self.crear_dentigrama()

    def init_documentos(self):
        """
        Crea las opciones por defecto para nuevos documentos, facturas y demás.
        """
        cols = (('Nombre', 'gobject.TYPE_STRING', False, True, True, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_autorizaciones'], cols)
        utils.preparar_listview(self.wids['tv_correspondencia'], cols)
        utils.preparar_listview(self.wids['tv_otros'], cols)

    def init_presupuestos(self):
        """
        Crea el listview de los presupuestos.
        """
        cols = (('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_concepto_presupuesto),
                ('Importe', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_importe_presupuesto),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_presupuestos'], cols)
        self.wids['tv_presupuestos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE) 
        self.wids['tv_presupuestos'].get_column(1).get_cell_renderers()[0].set_property("xalign", 1)

    def init_tratamientos(self):
        """
        Crea el listview de los tratamientos (citas).
        """
        cols = (('Fecha', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_fecha_cita),
                ('Diente', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_diente_cita),
                ('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_concepto_cita),
                ('Debido', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_debido_cita),
                ('Pagado', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_pagado_cita),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_tratamientos'], cols)
        tv = self.wids['tv_tratamientos']
        tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE) 
        tv.get_column(3).get_cell_renderers()[0].set_property("xalign", 1)
        tv.get_column(4).get_cell_renderers()[0].set_property("xalign", 1)
        tv.get_column(1).get_cell_renderers()[0].set_property("xalign", 0.5)
        # CWT:
        c = tv.get_column(2)
        try:
            c.set_properties(sizing=gtk.TREE_VIEW_COLUMN_FIXED,fixed_width=400)
        except:
            c.set_property("sizing", gtk.TREE_VIEW_COLUMN_FIXED)
            c.set_property("fixed_width", 400)
    
    def init_fotografias(self):
        """
        Crea el listview de las imagenes.
        """
        cols = (('Nombre', 'gobject.TYPE_STRING', True, True, True, self.cambiar_nombre_foto),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_fotos'], cols)
        self.wids['tv_fotos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE) 
        self.wids['tv_fotos'].connect("cursor-changed", self.mostrar_foto)

    def mostrar_foto(self, tv):
        """
        Muestra la foto de la fila seleccionada en el treeview.
        """
        model, paths = tv.get_selection().get_selected_rows()
        if len(paths) > 0:
            idfoto = model[paths[-1]][-1]
            foto = pclases.Fotografia.get(idfoto)
            pix = gtk.gdk.pixbuf_new_from_file(foto.get_ruta_completa())
            if pix.get_property("width") > 400 or pix.get_property("height") > 300:
                pix = pix.scale_simple(400, 300, gtk.gdk.INTERP_BILINEAR)
            self.wids['im_foto'].set_from_pixbuf(pix)

    def cambiar_nombre_foto(self, cell, path, txt):
        """
        Cambia el nombre de la foto seleccionada.
        """
        id = self.wids['tv_fotos'].get_model()[path][-1]
        foto = pclases.Fotografia.get(id)
        foto.nombre = txt
        self.rellenar_fotografias()

    def cambiar_fecha_cita(self, cell, path, txt):
        id = self.wids['tv_tratamientos'].get_model()[path][-1]
        cita = pclases.Cita.get(id)
        try:
            fecha = utils.parse_fecha(txt)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto %s no tiene un formato de fecha correcto." % txt, padre = self.wids['ventana'])
        else:
            cita.fecha = fecha
            self.rellenar_tabla_tratamientos()
            scroll_a_fila_nueva(self.wids['tv_tratamientos'], id, 1)
    
    def cambiar_diente_cita(self, cell, path, txt):
        id = self.wids['tv_tratamientos'].get_model()[path][-1]
        cita = pclases.Cita.get(id)
        cita.ndiente = txt
        self.rellenar_tabla_tratamientos()
        scroll_a_fila_nueva(self.wids['tv_tratamientos'], id, 2)
    
    def cambiar_concepto_cita(self, cell, path, txt):
        id = self.wids['tv_tratamientos'].get_model()[path][-1]
        cita = pclases.Cita.get(id)
        cita.concepto = txt
        self.rellenar_tabla_tratamientos()
        scroll_a_fila_nueva(self.wids['tv_tratamientos'], id, 3)

    def cambiar_debido_cita(self, cell, path, txt):
        id = self.wids['tv_tratamientos'].get_model()[path][-1]
        cita = pclases.Cita.get(id)
        try:
            debido = utils._float(txt)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto %s no tiene un formato numérico correcto." % txt, padre = self.wids['ventana'])
        else:
            cita.debido = debido
            self.rellenar_tabla_tratamientos()
            scroll_a_fila_nueva(self.wids['tv_tratamientos'], id, 4)

    def cambiar_pagado_cita(self, cell, path, txt):
        id = self.wids['tv_tratamientos'].get_model()[path][-1]
        cita = pclases.Cita.get(id)
        try:
            pagado = utils._float(txt)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto %s no tiene un formato numérico correcto." % txt, padre = self.wids['ventana'])
        else:
            cita.pagado = pagado
            self.rellenar_tabla_tratamientos()

    def cambiar_concepto_presupuesto(self, cell, path, txt):
        id = self.wids['tv_presupuestos'].get_model()[path][-1]
        presupuesto = pclases.Presupuesto.get(id)
        presupuesto.concepto = txt
        self.rellenar_tabla_presupuestos()
        scroll_a_fila_nueva(self.wids['tv_presupuestos'], id, 1)

    def cambiar_importe_presupuesto(self, cell, path, txt):
        id = self.wids['tv_presupuestos'].get_model()[path][-1]
        presupuesto = pclases.Presupuesto.get(id)
        try:
            importe = utils._float(txt)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto %s no tiene un formato numérico correcto." % txt, padre = self.wids['ventana'])
        else:
            presupuesto.importe = importe
            self.rellenar_tabla_presupuestos()

    def crear_dentigrama(self):
        """
        Crea un dentigrama con botones y los asocia a un callback que 
        actuará en función del color seleccionado en los radiobuttons.
        También colorea el DW al lado de cada radiobutton para identificar 
        el color de cada uno.
        Los colores de cada afección se encuentran "harcoded" en pclases.
        """
        self.colorear_radiobuttons()
        self.crear_botones_dentigrama()

    def crear_botones_dentigrama(self):
        """
        Crea una cuadrícula donde poner los botones del dentigrama y 
        los asocia al callback.
        """
        self.wids['tabla_dientes'] = gtk.Table(rows = 1 + 3 + 1 + 3 + 1, columns = 16*3, homogeneous = True)
        self.wids['hbox_dentigrama'].add(self.wids['tabla_dientes'])
        # Primera fila:
        for i in range(32):
            if i < 16:
                fila = 2
            else:
                fila = 6
            columna = (i*3) % (16*3)
            label = gtk.Label("<small>%d</small>" % (i+1))
            label.set_use_markup(True)
            if fila == 2:
                self.wids['tabla_dientes'].attach(label, columna+1, columna+2, fila-1, fila, xoptions = 0, yoptions = 0)
            else:
                self.wids['tabla_dientes'].attach(label, columna+1, columna+2, fila+3, fila+4, xoptions = 0, yoptions = 0)
            dn = gtk.Button()
            dn.connect("clicked", self.cambiar_color)
            dn.set_name("b_%dn" % i)
            self.wids[dn.get_name()] = dn
            self.wids['tabla_dientes'].attach(dn, columna+1, columna+2, fila, fila+1, yoptions = 0)
            ds = gtk.Button()
            ds.connect("clicked", self.cambiar_color)
            ds.set_name("b_%ds" % i)
            self.wids[ds.get_name()] = ds
            self.wids['tabla_dientes'].attach(ds, columna+1, columna+2, fila+2, fila+3, yoptions = 0)
            de = gtk.Button()
            de.connect("clicked", self.cambiar_color)
            de.set_name("b_%de" % i)
            self.wids[de.get_name()] = de
            self.wids['tabla_dientes'].attach(de, columna+2, columna+3, fila+1, fila+2, yoptions = 0)
            do = gtk.Button()
            do.connect("clicked", self.cambiar_color)
            do.set_name("b_%do" % i)
            self.wids[do.get_name()] = do
            self.wids['tabla_dientes'].attach(do, columna, columna+1, fila+1, fila+2, yoptions = 0)
            dc = gtk.Button()
            dc.connect("clicked", self.cambiar_color)
            dc.set_name("b_%dc" % i)
            self.wids[dc.get_name()] = dc
            self.wids['tabla_dientes'].attach(dc, columna+1, columna+2, fila+1, fila+2, yoptions = 0)
        self.wids['tabla_dientes'].show_all()

    def cambiar_color(self, boton):
        """
        Cambia el color de la porción del diente a la que 
        se ha hecho clic y guarda el nuevo número de afección 
        en el registro.
        """
        dl = boton.get_name().replace("b_", "")
        d = int(dl[:-1])
        l = dl[-1]
        diente = pclases.Diente.select(pclases.AND(
                                pclases.Diente.q.pacienteID == self.objeto.id, 
                                pclases.Diente.q.diente == d))
        try:
            diente = diente[0]
        except IndexError:
            diente = pclases.Diente(paciente = self.objeto, diente = d)
        numafeccion = self.get_numafeccion()
        setattr(diente, l, numafeccion)
        self.rellenar_dentigrama(self.objeto)

    def get_numafeccion(self):
        """
        Devuelve el número de afección marcado en el dentigrama.
        """
        for i in range(len(pclases.AFECCIONES)):
            afeccion = pclases.AFECCIONES[i].keys()[0]
            rb = self.wids['rb_%s' % afeccion]
            if rb.get_active():
                return i

    def colorear_radiobuttons(self):
        """
        Colorea los "drawings area" de los radiobuttons.
        """
        for numafeccion in range(len(pclases.AFECCIONES)):
            afeccion = pclases.AFECCIONES[numafeccion].keys()[0]   # Solo una clave por diccionario
            color = pclases.AFECCIONES[numafeccion][afeccion]
            area = self.wids['dw_%s' % afeccion]
            area.modify_bg(gtk.STATE_NORMAL, area.get_colormap().alloc_color(*color))

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        # ws = tuple(["e_observaciones", "tv_transferencias", "b_borrar"] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        resto_widgets = self.wids.keys()
        # Aquí no debo tocar guardar ni actualizar, ya se activan o desactivan en función del objeto y valores en 
        # ventana desde la función es_diferente y el hilo notificador del objeto respectivamente.
        resto_widgets.remove("b_guardar")
        resto_widgets.remove("b_actualizar")
        ws = tuple([self.dic_campos[k] for k in self.dic_campos.keys()]) + tuple(resto_widgets)
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except:
                print w
        # b_nuevo siempre a True porque aquí no hay control de permisos y siempre se debe poder crear un nuevo paciente.
        self.wids['b_salir'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        self.wids['b_nuevo'].set_sensitive(True)
        parent = self.wids['b_nuevo'].parent
        while parent != None:
            parent.set_sensitive(True)
            parent = parent.parent

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, "%06d" % r.codigo, r.nombre))
        idpaciente = utils.dialogo_resultado(filas_res,
                                           titulo = 'SELECCIONE PACIENTE',
                                           cabeceras = ('ID', 'Código', 'Nombre'), 
                                           padre = self.wids['ventana'])
        if idpaciente < 0:
            return None
        else:
            return idpaciente

    def rellenar_widgets(self):
        """
        Introduce la información de el paciente actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        paciente = self.objeto
        if paciente != None:
            self.objeto.make_swap()
            self.wids['e_codigo'].set_text("%06d" % paciente.codigo)
            for nombre_col in self.dic_campos:
                self.escribir_valor(paciente.sqlmeta.columnDefinitions[nombre_col], 
                                    getattr(paciente, nombre_col), 
                                    self.dic_campos[nombre_col])
            pos = buscar_pos_paciente(self.objeto) + 1
            self.wids['ventana'].set_title("%d/%d - %s" % (pos, pclases.Paciente.select().count(), paciente.nombre))
            self.rellenar_tabla_tratamientos()
            self.rellenar_tabla_presupuestos()
            self.rellenar_fotografias()
            self.rellenar_documentos()
            mostrar_edad(paciente, self.wids['e_edad'])
            self.rellenar_dentigrama(paciente)
    
    def rellenar_documentos(self):
        """
        Introduce los documentos del paciente en los treeview.
        """
        ma = self.wids['tv_autorizaciones'].get_model()
        mc = self.wids['tv_correspondencia'].get_model()
        mo = self.wids['tv_otros'].get_model()
        mcorr = self.wids['tv_correspondencia'].get_model()
        for model, tipo in (zip((ma, mc, mo, mcorr), range(1, 4))):
            model.clear()
            if self.objeto:
                docus = list(self.objeto.documentos)
                docus.sort(key = lambda d: d.id)
                for docu in docus:
                    if docu.tipo == tipo:
                        model.append((docu.ruta, docu.id))

    def rellenar_dentigrama(self, paciente):
        """
        Colorea los botones según los registros diente del paciente.
        """
        if SHOW_DENTIGRAMA:
            for d in range(32):
                for l in ("n", "s", "e", "o", "c"):
                    w = self.wids['b_%d%s' % (d, l)]
                    w.modify_bg(gtk.STATE_NORMAL, None)
            for diente in paciente.dientes:
                n = diente.diente
                self.poner_color(self.wids['b_%dn' % n], diente.n)
                self.poner_color(self.wids['b_%ds' % n], diente.s)
                self.poner_color(self.wids['b_%de' % n], diente.e)
                self.poner_color(self.wids['b_%do' % n], diente.o)
                self.poner_color(self.wids['b_%dc' % n], diente.c)

    def poner_color(self, w, numafeccion):
        afeccion = pclases.AFECCIONES[numafeccion].keys()[0]   # Solo una clave por diccionario
        color = pclases.AFECCIONES[numafeccion][afeccion]
        w.modify_bg(gtk.STATE_NORMAL, w.get_colormap().alloc_color(*color))
        w.set_property("tooltip-text", afeccion)

    def rellenar_tabla_tratamientos(self):
        model = self.wids['tv_tratamientos'].get_model()
        model.clear()
        totalp = totald = 0.0
        citas = list(self.objeto.citas)
        citas.sort(key = lambda c: c.id)
        for c in citas:
            totalp += c.pagado
            totald += c.debido
            model.append((utils.str_fecha(c.fecha), 
                          c.ndiente, 
                          c.concepto, 
                          utils.float2str(c.debido, 0), 
                          utils.float2str(c.pagado, 0), 
                          c.id))
        self.wids['e_total_debido_tratamiento'].set_text(utils.float2str(totald, 0))
        self.wids['e_total_pagado_tratamiento'].set_text(utils.float2str(totalp, 0))
    
    def rellenar_fotografias(self):
        model = self.wids['tv_fotos'].get_model()
        model.clear()
        self.wids['im_foto'].set_from_file(None)
        if self.objeto != None:
            fotos = list(self.objeto.fotografias)
            fotos.sort(key = lambda f: f.id)
            for foto in fotos:
                model.append((foto.nombre, 
                              foto.id))
    
    def rellenar_tabla_presupuestos(self):
        model = self.wids['tv_presupuestos'].get_model()
        model.clear()
        total = 0.0
        press = self.objeto.presupuestos[:]
        press.sort(lambda x, y: int(x.id - y.id))
        for p in press:
            total += p.importe
            model.append((p.concepto,
                          utils.float2str(p.importe, 0), 
                          p.id))
        self.wids['e_total_presupuesto'].set_text(utils.float2str(total, 0))
            
            
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        paciente_anterior = self.objeto
        if paciente_anterior != None:
            paciente_anterior.notificador.desactivar()
        paciente = pclases.Paciente()
        utils.dialogo_info('NUEVO PACIENTE', 
                           'Se ha creado un paciente nuevo.\nA continuación complete la información del mismo y guarde los cambios.', 
                           padre = self.wids['ventana'])
        paciente.notificador.activar(self.aviso_actualizacion)
        self.objeto = paciente
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = paciente_anterior)
        self.wids['e_nombre'].grab_focus()

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        paciente = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PACIENTE", 
                                         texto = "Introduzca nombre o código:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                int_buscar = int(a_buscar)
            except ValueError:
                int_buscar = -1
            criterio = pclases.OR(pclases.Paciente.q.nombre.contains(a_buscar),
                                  pclases.Paciente.q.codigo == int_buscar,
                                  pclases.Paciente.q.id == int_buscar)
            resultados = pclases.Paciente.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                idpaciente = self.refinar_resultados_busqueda(resultados)
                if idpaciente == None:
                    return
                resultados = [pclases.Paciente.get(idpaciente)]
                # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.',
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if paciente != None:
                paciente.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                paciente = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            paciente.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = paciente
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        for colname in self.dic_campos:
            col = self.clase.sqlmeta.columnDefinitions[colname]
            try:
                valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                setattr(self.objeto, colname, valor_ventana)
            except (ValueError, mx.DateTime.RangeError, TypeError):
                pass    # TODO: Avisar al usuario o algo. El problema es que no hay una forma "limpia" de obtener el valor que ha fallado.
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        self.objeto.syncUpdate()
        self.objeto.sync()
        # Vuelvo a activar el notificador
        self.objeto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar(self, widget):
        """
        Elimina el paciente de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        paciente = self.objeto
        if paciente != None:
            if utils.dialogo('¿Eliminar el paciente?', 'BORRAR', padre = self.wids['ventana']):
                paciente.notificador.desactivar()
                try:
                    #paciente.destroySelf()
                    paciente.destroy_en_cascada()
                except Exception, e:
                    self.logger.error("pacientes::borrar -> Paciente ID %d no se pudo eliminar. Excepción: %s." % (paciente.id, e))
                    utils.dialogo_info(titulo = "PACIENTE NO ELIMINADO", 
                                       texto = "El paciente no se pudo eliminar.\n\nSe generó un informe de error en el «log» de la aplicación.",
                                       padre = self.wids['ventana'])
                    self.actualizar_ventana()
                else:
                    self.objeto = None
                    self.ir_a_primero()

    def imprimir_podologia(self, boton):
        import geninformes
        from informes import abrir_pdf
        filtrar = utils.dialogo(titulo = "FILTRAR CAMPOS VACÍOS", 
                                texto = "¿Desea ignorar los campos vacíos?", 
                                padre = self.wids['ventana'])
        abrir_pdf(geninformes.podologia(self.objeto, filtrar))
        

def mostrar_edad(paciente, entry):
    try:
        edad = paciente.calcular_edad()
        text = "%d años (%s)" % (edad, utils.str_fecha(paciente.fechaNac))
    except AttributeError:
        text = "N/A"
    entry.set_text(text)

def buscar_pos_paciente(paciente):
    """
    Devuelve el índice que ocupa el paciente en la lista de 
    registros de pacientes de la BD empezando por 0.
    """
    # Lento, lo sé, pero no se me ocurre ninguna otra forma.
    #pos = list(pclases.Paciente.select(orderBy = "id")).index(paciente)
    # Siempre que necesites optimización, sáltate una capa de abstracción.
    ids = pclases.Paciente._connection.queryAll("SELECT id FROM paciente ORDER BY id;")
    ids = [i[0] for i in ids]
    pos = ids.index(paciente.id)
    return pos

def mover_a_papelera(foto_o_documento):
    """
    Mueve el archivo indicado por la ruta al directorio temporal 
    de la máquina local del usuario.
    """
    from tempfile import gettempdir
    import shutil
    try:
        shutil.move(foto_o_documento.get_ruta_completa(), gettempdir())
    except IOError:
        print "pacientes.py::mover_a_papelera -> Fichero %s no existe." % (foto_o_documento.get_ruta_completa())

def browse_for_image():
    """This function is used to browse for an image.
    The path to the image will be returned if the user
    selects one, however a blank string will be returned
    if they cancel or do not select one."""

    file_open = gtk.FileChooserDialog(title="Seleccione imagen"
                , action=gtk.FILE_CHOOSER_ACTION_OPEN
                , buttons=(gtk.STOCK_CANCEL
                            , gtk.RESPONSE_CANCEL
                            , gtk.STOCK_OPEN
                            , gtk.RESPONSE_OK))
    """Create and add the Images filter"""
    filter = gtk.FileFilter()
    filter.set_name("Imágenes")
    filter.add_mime_type("image/png")
    filter.add_mime_type("image/jpeg")
    filter.add_mime_type("image/gif")
    filter.add_pattern("*.png")
    filter.add_pattern("*.jpg")
    filter.add_pattern("*.gif")
    file_open.add_filter(filter)
    """Create and add the 'all files' filter"""
    filter = gtk.FileFilter()
    filter.set_name("Todos los ficheros")
    filter.add_pattern("*")
    file_open.add_filter(filter)

    """Init the return value"""
    result = ""
    if file_open.run() == gtk.RESPONSE_OK:
        result = file_open.get_filename()
    file_open.destroy()

    return result

def scroll_a_fila_nueva(tv, id, ncol = 1):
    """
    Mueve el scroll del TreeView al id recibido.
    """
    model = tv.get_model()
    for path in range(len(model)):
        if model[model.get_iter(path)][-1] == id: 
            tv.scroll_to_cell(path,               
                              use_align = True)
            column = tv.get_column(ncol)
            cell = column.get_cell_renderers()[0]
            tv.set_cursor_on_cell(path,
                                  column,
                                  cell,
                                  start_editing = True)

            break

if __name__ == "__main__":
    p = Pacientes()

