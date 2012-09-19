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

# Módulo para construir, abrir e imprimir informes y escritos

import os
from time import localtime
import zipfile  #Para toquetear los .sxw
from tempfile import gettempdir as tmpdir
import sys
if os.path.join("..", "framework") not in sys.path:
    sys.path.append(os.path.join("..", "framework"))
import pclases

def cambia_en_sxw(archivo, cambios):
    """ Abre el archivo 'archivo', que debe ser un documento de writer de OOo y
    cambia en el content.xml las claves indicadas en cambios por sus valores
    correspondientes.
    Devuelve un valor != 0 para indicar el error."""
    try:
        doc = zipfile.ZipFile(archivo, 'a')
    except:
        return -4
    rutatemp = os.path.join(tmpdir(), "temporaloo.txt")
    txt=open(rutatemp, 'w') #temporal para los cambios.
    texto=doc.read('content.xml')
    for cambio in cambios:
        nuevo = cambios[cambio]
        try:
            texto = texto.replace(cambio, nuevo)
        except:
            print "mod_informes.py: ", cambio, nuevo
            texto = "ERROR PARÁMETRO"
    txt.write(texto)
    txt.close()
    doc.write(rutatemp, 'content.xml')
    # OJO: Creo que duplica el archivo, se almacenan en el ZIP 2 contents.
    # OOo lee el último, así que de momento funciona, pero ojito en 
    # futuras versiones de oowrite. Ver especificaciones de los archivos
    # en la web de OpenOffice.org 
    doc.close()
    return 0

def combinar_sxw(cambios, documento):
    """ A partir del nombre del documento y el paciente, realiza los cambios
    de valores del diccionario en el archivo con 'nombre' de la ruta 'ruta'."""
    return cambia_en_sxw(documento.get_ruta_completa(), cambios)

def nuevo_doc(paciente, ruta_base = os.path.join("..", "compartido"), plantilla = None, nombre = '', tipo = 3):
    """ Crea un nuevo documento para el paciente.
    Si el directorio del paciente no existe -ruta_base+paciente-, lo crea.
    Si se especifica una plantilla, se copia la misma al directorio del 
    paciente y la abre con el procesador de texto de OpenOffice.org.
    La plantilla debe venir sin ruta, indicando únicamente el nombre del 
    archivo (lo que se conoce como extensión en DOS forma parte del nombre
    en UNIX, por lo tanto, también debe venir en el parámetro).
    Si no se especifica, comienza un nuevo documento a partir de una
    plantilla en blanco -o únicamente con el encabezado, ya veré-.
    Si el nombre del documento no se pasa, al nuevo documento se le
    llamará paciente+fecha+número secuencial.
    Tipo es el tipo de documento: 
        1 - Autorizaciones, 2 - Correspondencia, resto de enteros - Otros.
    Devuelve el nombre con que finalmente se crea el archivo.
    """
    # TO DO: Pedir e introducir los datos directamente en el contenido
    # del documento, aprovechando que OOo lo guarda todo en XML comprimido.
    dir_paciente = os.path.join(ruta_base, `paciente.codigo`)
    if not os.path.exists(dir_paciente):
        os.mkdir(dir_paciente)
    if nombre=='':
        # No se ha pasado descripción, buscar el siguiente nombre disponible.
        num = -1
        hoy = '-'.join([`i` for i in localtime()[:3]])
        try:
            while True:
                num+=1
                nomfichero = "%s%s%d.sxw" % (`paciente.codigo`, hoy, num)
                os.stat(os.path.join(dir_paciente, nomfichero))
        except:
            nomfichero = "%s%s%d.sxw" % (`paciente.codigo`, hoy, num)
    else:
        if not nombre.endswith(".sxw"):
            nomfichero = nombre + ".sxw"
        else:
            nomfichero = nombre
    nombre = nombre.replace('/','-').replace('.','_').replace('º','o').replace('ª','a').replace('ñ','n').replace('Ñ','N')
    ruta_doc = os.path.join(dir_paciente, nomfichero)
    # Preparo el documento que servirá como plantilla
    ruta_plantilla = os.path.join("..", "compartido", "plantillas")
    if plantilla == None:
        ruta_plantilla = os.path.join(ruta_plantilla, 'blanco.sxw')
    else:
        if not plantilla.endswith(".sxw"):
            plantilla += ".sxw"
        ruta_plantilla = os.path.join(ruta_plantilla, plantilla)
    import shutil
    shutil.copy(ruta_plantilla, ruta_doc)
    # Estaría bien mirar si devuelve error o algo... otra cosa más al TO DO.
    return pclases.Documento(paciente = paciente, tipo = tipo, ruta = nomfichero)

def abrir_documento(ruta):
    """
    Si la plataforma es MS-Windows abre el archivo con la aplicación 
    predeterminada para los archivos CSV (por desgracia me imagino que 
    MS-Excel). Si no, intenta abrirlo con OpenOffice.org Calc.
    """
    # TODO: Problemón. Al ponerle el ampersand para mandarlo a segundo plano, sh siempre devuelve 0 como salida del comando, 
    # así que no hay manera de saber cuándo se ha ejecutado bien y cuándo no.
    if sys.platform != 'win32':     # Más general que os.name (que da "nt" en los windows 2000 de las oficinas).
        if not ( (not os.system('oowriter2 "%s" || oowriter "%s" &' % (ruta, ruta))) or \
                 (not os.system('oowriter "%s" &' % ruta)) ):
            utils.dialogo_info(titulo = "OOo NO ENCONTRADO", 
                               texto = "No se encontró OpenOffice.org en el sistema.\nNo fue posible mostrar el archivo %s." % (ruta)) 
    else:
        # OJO: Esto no es independiente de la plataforma:
        os.startfile(ruta)
    

