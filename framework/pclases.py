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
# Cambios de SQLObject 0.9.1 respecto al [fork de] SQLObject 0.6.1 de ginn:
# _SO_columnDict ha sido sustituido por sqlmeta.columnDefinitions
# _fromDatabase = True ha sido sustituido por class sqlmeta: fromDatabase = True
# claveAjenaID = ForeignKey... se queda solo en claveAjena = ForeignKey...

"""
    Catálogo de clases persistentes.
"""


DEBUG = False
#DEBUG = True   # Se puede activar desde ipython después de importar con 
                # pclases.DEBUG = True
VERBOSE = True  # Activar para mostrar por pantalla progreso al cargar clases.
VERBOSE = False

if DEBUG or VERBOSE:
    print "IMPORTANDO PCLASES"

import sys, os
from sqlobject import __doc__ as strsqlobject_version
from sqlobject import *

import re
sqlobject_version = [int(i) for i in re.findall("\d+", strsqlobject_version)]
sqlobject_autodeclareids = lambda: sqlobject_version >= [0, 12, 4]

sys.path.append(os.path.join('..', 'ui'))
try:
    import utils
except ImportError, msg:
    print "WARNING: No se pudo importar utils. Excepción.\n%s" % (msg)

try:
    import notificacion
except:
    sys.path.append(os.path.join('..', 'ui'))
    try:
        import notificacion
    except:
        sys.path.append('.')
        import notificacion
  
import threading#, psycopg
from select import select

from configuracion import ConfigConexion

#import mx, mx.DateTime
import datetime

# GET FUN !

config = ConfigConexion()

#conn = '%s://%s:%s@%s/%s' % (config.get_tipobd(), 
#                             config.get_user(), 
#                             config.get_pass(), 
#                             config.get_host(), 
#                             config.get_dbname())

# HACK: No reconoce el puerto en el URI y lo toma como parte del host. Lo 
# añado detrás y colará en el dsn cuando lo parsee. 
if config.get_tipobd() == "sqlite":
    # OJO: No soportado completamente por el momento.
    ruta_bdsqlite = os.path.join("..", "db", config.get_dbname())
    ruta_bdsqlite = os.path.abspath(ruta_bdsqlite)
    conn = "%s://%s" % (config.get_tipobd(), 
                       ruta_bdsqlite)
else:
    conn = '%s://%s:%s@%s/%s port=%s' % (config.get_tipobd(), 
                                         config.get_user(), 
                                         config.get_pass(), 
                                         config.get_host(), 
                                         config.get_dbname(), 
                                         config.get_puerto()) 
if DEBUG:
    conndebug = connectionForURI(conn)
    #conndebug.autoCommit = False
    conndebug.debug = True

# HACK:
# Hago todas las consultas case-insensitive machacando la función de 
# sqlbuilder:
_CONTAINSSTRING = sqlbuilder.CONTAINSSTRING
def CONTAINSSTRING(expr, pattern):
    try:
        try:
            nombre_clase = SQLObject.sqlmeta.style.dbTableToPythonClass(
                            expr.tableName)
        except Exception, msg:
            nombre_clase = styles.defaultStyle.dbTableToPythonClass(
                            expr.tableName)
        clase = globals()[nombre_clase]
        columna = clase.sqlmeta.columns[expr.fieldName]
    except (AttributeError, KeyError):
        return _CONTAINSSTRING(expr, pattern)
    if isinstance(columna, (SOStringCol, SOUnicodeCol)):
        op = sqlbuilder.SQLOp("ILIKE", expr, 
                                '%' + sqlbuilder._LikeQuoted(pattern) + '%')
    elif isinstance(columna, (SOFloatCol, SOIntCol, SODecimalCol, 
                              SOMediumIntCol, SOSmallIntCol, SOTinyIntCol)):
        try:
            pattern = str(_float(pattern))
        except ValueError:
            pattern = None
        if not pattern:
            op = sqlbuilder.SQLOp("IS NOT", expr, None)
        else:
            op = sqlbuilder.SQLOp("=", expr, 
                                    sqlbuilder._LikeQuoted(pattern))
    else:
        op = sqlbuilder.SQLOp("LIKE", expr, 
                                '%' + sqlbuilder._LikeQuoted(pattern) + '%')
    return op
sqlbuilder.CONTAINSSTRING = CONTAINSSTRING

class SQLtuple(tuple):
    """
    Básicamemte una tupla, pero con la función .count() para hacerla 
    "compatible" con los SelectResults de SQLObject.
    """
    def __init__(self, *args, **kw):
        self.elbicho = tuple(*args, **kw)
        tuple.__init__(*args, **kw)
    #def __new__(self, *args, **kw):
    #    self.elbicho = tuple(*args, **kw)
    #    tuple.__new__(*args, **kw)
    def count(self):
        return len(self)
    def sumFloat(self, campo):
        res = 0.0
        for item in self.elbicho:
            res += getattr(item, campo)
        return res
    def sum(self, campo):
        return self.sumFloat(campo)

class SQLlist(list):
    """
    Básicamemte una lista, pero con la función .count() para hacerla 
    "compatible" con los SelectResults de SQLObject.
    """
    def __init__(self, *args, **kw):
        self.rocio = list(*args, **kw)
        list.__init__(self, *args, **kw)
    def count(self):
        return len(self.rocio)
    # DISCLAIMER: Paso de otra clase base para solo 2 funciones que se repiten.
    def sumFloat(self, campo):
        res = 0.0
        for item in self.rocio:
            res += getattr(item, campo)
        return res
    def sum(self, campo):
        return self.sumFloat(campo)
    def append(self, *args, **kw):
        raise TypeError, "No se pueden añadir elementos a un SelectResults"
    def extend(self, *args, **kw):
        raise TypeError, "No se puede extender un SelectResults."
    def insert(self, *args, **kw):
        raise TypeError, "No se pueden insertar elementos en un SelectResults."
    def pop(self, *args, **kw):
        raise TypeError, "No se pueden eliminar elementos de un SelectResults."
    def remove(self, *args, **kw):
        raise TypeError, "No se pueden eliminar elementos de un SelectResults."

class SQLObjectChanged(Exception):
    """ User-defined exception para ampliar la funcionalidad
    de SQLObject y que soporte objetos persistentes."""
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

class PRPCTOO:
    """ 
    Clase base para heredar y no repetir código.
    Únicamente implementa los métodos para iniciar un hilo de 
    sincronización y para detenerlo cuando ya no sea necesario.
    Ningún objeto de esta clase tiene utilidad "per se".
    """
    # El nombre viene de todo lo que NO hace pero para lo que es útil:
    # PersistentRemoteProcessComunicatorThreadingObservadorObservado. TOOOOOMA.
    def __init__(self, nombre_clase_derivada = ''):
        """
        El nombre de la clase derivada pasado al 
        constructor es para la metainformación 
        del hilo.
        """
        self.__oderivado = nombre_clase_derivada
        self.swap = {}

    def abrir_conexion(self):
        """
        Abre una conexión con la BD y la asigna al 
        atributo conexión de la clase.
        No sale del método hasta que consigue la
        conexión.
        """
        while 1:
            try:
                self.conexion = self._connection.getConnection()
                if DEBUG: print " --> Conexión abierta."
                return
            except:
                print "ERROR estableciendo conexión secundaria para IPC. Vuelvo a intentar"
    
    def abrir_cursor(self):
        self.cursor = self.conexion.cursor()
        if DEBUG: print [self.cursor!=None and self.cursor or "El cursor devuelto es None."][0], self.conexion, len(self.conexion.cursors)

    def make_swap(self):
        # Antes del sync voy a copiar los datos a un swap temporal, para poder comparar:
        for campo in self.sqlmeta.columns:
            self.swap[campo]=eval('self.%s' % campo)
        
    def comparar_swap(self):
        # Y ahora sincronizo:
        #self.sync()    # Da SERIOS problemas de rendimiento. Dunno why.
        # y comparo:
        for campo in self.sqlmeta.columnDefinitions:
            #~print self.swap[campo], getattr(self, campo) 
            if self.swap[campo] != getattr(self, campo): 
                if DEBUG:
                    print "comparar_swap: ", campo, self.swap[campo], getattr(self, campo)
                raise SQLObjectChanged(self)

    def cerrar_cursor(self):
        self.cursor.close()

    def cerrar_conexion(self):
        self.conexion.close()
        if DEBUG: print " <-- Conexión cerrada."

    ## Código del hilo:
    def esperarNotificacion(self, nomnot, funcion=lambda: None):
        """
        Código del hilo que vigila la notificación.
        self -> Objeto al que pertenece el hilo.
        nomnot es el nombre de la notificación a esperar.
        funcion es una función opcional que será llamada cuando se
        produzca la notificación.
        """
        if DEBUG: print "Inicia ejecución hilo"
        while self != None and self.continuar_hilo:   # XXX
            if DEBUG: print "Entra en la espera bloqueante: %s" % nomnot
            self.abrir_cursor()
            self.cursor.execute("LISTEN %s;" % nomnot)
            self.conexion.commit()
            if select([self.cursor], [], [])!=([], [], []):
                if DEBUG: print "Notificación recibida"
                try:
                    self.comparar_swap()
                except SQLObjectChanged:
                    if DEBUG: print "Objeto cambiado"
                    funcion()
                except SQLObjectNotFound:
                    if DEBUG: print "Registro borrado"
                    funcion()
                # self.cerrar_cursor()
        else:
            if DEBUG: print "Hilo no se ejecuta"
        if DEBUG: print "Termina ejecución hilo"

    def chequear_cambios(self):
        try:
            self.comparar_swap()
            # print "NO CAMBIA"
        except SQLObjectChanged:
            # print "CAMBIA"
            if DEBUG: print "Objeto cambiado"
            # print self.notificador
            self.notificador.run()
        except SQLObjectNotFound:
            if DEBUG: print "Registro borrado"
            self.notificador.run()

    def ejecutar_hilo(self):
        ## ---- Código para los hilos:
        self.abrir_conexion()
        self.continuar_hilo = True
        nombre_clase = self.__oderivado
        self.th_espera = threading.Thread(target=self.esperarNotificacion, args=("IPC_%s" % nombre_clase, self.notificador.run), name="Hilo-%s" % nombre_clase)
        self.th_espera.setDaemon(1)
        self.th_espera.start()

    def parar_hilo(self):
        self.continuar_hilo = False
        if DEBUG: print "Parando hilo..."
        self.cerrar_conexion()

    def destroy_en_cascada(self):
        """
        Destruye recursivamente los objetos que dependientes y 
        finalmente al objeto en sí.
        OJO: Es potencialmente peligroso y no ha sido probado en profundidad.
             Puede llegar a provocar un RuntimeError por alcanzar la profundidad máxima de recursividad
             intentando eliminarse en cascada a sí mismo por haber ciclos en la BD. 
        """
        for join in self.sqlmeta.joins:
            lista = join.joinMethodName
            for dependiente in getattr(self, lista):
            # for dependiente in eval("self.%s" % (lista)):
                if DEBUG:
                    print "Eliminando %s..." % dependiente
                dependiente.destroy_en_cascada()
        self.destroySelf()

    def copyto(self, obj, eliminar = False):
        """
        Copia en obj los datos del objeto actual que en obj sean 
        nulos.
        Enlaza también las relaciones uno a muchos para evitar 
        violaciones de claves ajenas, ya que antes de terminar, 
        si "eliminar" es True se borra el registro de la BD.
        PRECONDICIÓN: "obj" debe ser del mismo tipo que "self".
        POSTCONDICIÓN: si "eliminar", self debe quedar eliminado.
        """
        assert type(obj) == type(self) and obj != None, "Los objetos deben pertenecer a la misma clase y no ser nulos."
        for nombre_col in self.sqlmeta.columns:
            valor = getattr(obj, nombre_col)
            if valor == None or (isinstance(valor, str) and valor.strip() == ""):
                if DEBUG:
                    print "Cambiando valor de columna %s en objeto destino." % (nombre_col)
                setattr(obj, nombre_col, getattr(self, nombre_col))
        for col in self._SO_joinList:
            atributo_lista = col.joinMethodName
            lista_muchos = getattr(self, atributo_lista)
            nombre_clave_ajena = repr(self.__class__).replace("'", ".").split(".")[-2] + "ID" # HACK (y de los feos)
            nombre_clave_ajena = nombre_clave_ajena[0].lower() + nombre_clave_ajena[1:]       # HACK (y de los feos)
            for propagado in lista_muchos:
                if DEBUG:
                    print "Cambiando valor de columna %s en objeto destino." % (nombre_clave_ajena)
                    print "   >>> Antes: ", getattr(propagado, nombre_clave_ajena)
                setattr(propagado, nombre_clave_ajena, obj.id)
                if DEBUG:
                    print "   >>> Después: ", getattr(propagado, nombre_clave_ajena)
        if eliminar:
            try:
                self.destroySelf()
            except:     # No debería. Pero aún así, me aseguro de que quede eliminado (POSTCONDICIÓN).
                self.destroy_en_cascada()

    def clone(self, *args, **kw):
        """
        Crea y devuelve un objeto idéntico al actual.
        Si se pasa algún parámetro adicional se intentará enviar 
        tal cual al constructor de la clase ignorando los 
        valores del objeto actual para esos parámetros.
        """
        parametros = {}
        for campo in self.sqlmeta.columns:
            valor = getattr(self, campo)
            parametros[campo] = valor
        for campo in kw:
            valor = kw[campo]
            parametros[campo] = valor
        nuevo = self.__class__(**parametros)
        return nuevo

    def get_info(self):
        """
        Devuelve información básica (str) acerca del objeto. Por ejemplo, 
        si es un pedido de venta, devolverá el número de pedido, fecha y 
        cliente.
        Este método se hereda por todas las clases y debería ser redefinido.
        """
        return "%s ID %d" % (self.sqlmeta.table, self.id)


def starter(objeto, *args, **kw):
    """
    Método que se ejecutará en el constructor de todas las 
    clases persistentes.
    Inicializa el hilo y la conexión secundaria para IPC, 
    así como llama al constructor de la clase padre SQLObject.
    """
    objeto.continuar_hilo = False
    objeto.notificador = notificacion.Notificacion(objeto)
    SQLObject._init(objeto, *args, **kw)
    PRPCTOO.__init__(objeto, objeto.sqlmeta.table)
    objeto.make_swap()    # Al crear el objeto hago la primera caché de datos, por si acaso la ventana 
                          # se demora mucho e intenta compararla antes de crearla.

    #objeto._cacheValues = False    # FIXME: Sospecho que tarde o temprano tendré que desactivar las cachés locales de SQLObject. 
                                    # Tengo que probarlo antes de poner en producción porque no sé si va a resultar peor el remedio 
                                    # (por ineficiente) que la enfermedad (que solo da problemas de vez en cuando y se resuelven 
                                    # con un Shift+F5).
                                    # Mala idea. ¡Si desactivo el caché de SQLObject tengo que hacer sync() después de cada operación!

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

"""
Constante AFECCIONES:
    Una lista donde el índice de cada ítem es el número que corresponde a la afección.
    Cada ítem es un diccionario que tiene como clave el sufijo del widget (rb_/dw_) y 
    como valor el color GTK en RBG que se aplicará.
"""
AFECCIONES = [{"sano": (65535, 65535, 65535)}, 
              {"cariado": (0, 0, 0)}, 
              {"obtur": (65535, 65535, 0)}, 
              {"nocaries": (65535, 0, 65535)}, 
              {"absnoca": (65535, 0, 0)}, 
              {"sellado": (0, 65535, 65535)}, 
              {"corona": (0, 65535, 0)}, 
              {"no_erup": (0, 0, 65535)}, 
              {"prot_remov": (32767, 32767, 32767)}, 
              {"prot_fija": (32767, 0, 65535)}, 
              {"pilar_p_fija": (0, 32767, 65535)}, 
              {"aus_mobili": (65535, 32767, 0)} ]

class Paciente(SQLObject, PRPCTOO):
    _connection = conn
    class sqlmeta:
        fromDatabase = True
    dientes = MultipleJoin('Diente')
    citas = MultipleJoin('Cita')
    presupuestos = MultipleJoin('Presupuesto')
    fotografias = MultipleJoin('Fotografia')
    documentos = MultipleJoin('Documento')
    # podologias = MultipleJoin('Podologia')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    #def calcular_edad(self, fecha = mx.DateTime.localtime()):
    def calcular_edad(self, fecha = datetime.date.today()):
        """
        Calcula la edad del paciente en la fecha recibida (fecha 
        actual por defecto).
        """
        edad = fecha.year - self.fechaNac.year - 1
        if fecha.day >= self.fechaNac.day and fecha.month >= self.fechaNac.month:
            edad += 1
        return edad

class Diente(SQLObject, PRPCTOO):
    _connection = conn
    class sqlmeta:
        fromDatabase = True
    if not sqlobject_autodeclareids():
        paciente = ForeignKey('Paciente')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


class Cita(SQLObject, PRPCTOO):
    _connection = conn
    class sqlmeta:
        fromDatabase = True
    if not sqlobject_autodeclareids():
        paciente = ForeignKey('Paciente')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


class Presupuesto(SQLObject, PRPCTOO):
    _connection = conn
    class sqlmeta:
        fromDatabase = True
    if not sqlobject_autodeclareids():
        paciente = ForeignKey('Paciente')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


class Fotografia(SQLObject, PRPCTOO):
    _connection = conn
    class sqlmeta:
        fromDatabase = True
    if not sqlobject_autodeclareids():
        paciente = ForeignKey('Paciente')

    pre_ruta = os.path.join("..", "compartido")
    pre_ruta = staticmethod(pre_ruta)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_ruta_completa(self):
        """
        Devuelve la ruta completa relativa a la imagen.
        """
        return os.path.join(self.pre_ruta, `self.paciente.codigo`, self.ruta)

    def make_ruta_completa(classfoto, paciente, ruta):
        """
        Devuelve la ruta completa que correspondería al fichero
        cuya ruta se ha recibido y en función del paciente.
        Se asegura de que la ruta de directorios existe.
        """
        ruta = os.path.join(classfoto.pre_ruta, `paciente.codigo`, os.path.split(ruta)[-1])
        try:
            assert os.path.exists(os.path.split(ruta)[0])
        except AssertionError:
            os.mkdir(os.path.split(ruta)[0])
        return ruta

    ruta_completa = classmethod(make_ruta_completa)

class Documento(SQLObject, PRPCTOO):
    _connection = conn
    class sqlmeta:
        fromDatabase = True
    if not sqlobject_autodeclareids():
        paciente = ForeignKey('Paciente')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)
    
    pre_ruta = os.path.join("..", "compartido")
    pre_ruta = staticmethod(pre_ruta)

    # TODO: OJO: Si se cambia el código del paciente hay que cambiar la ruta a
    # sus documentos. Lo suyo sería hacer un wrapper sobre el método heredado 
    # de SQLObject para cambiar el código y que renombrar el directorio antes 
    # de hacerlo y después de haber comprobado que el código sigue cumpliendo 
    # la restricción UNIQUE y que por tanto no hay otro directorio llamado 
    # igual.
    def get_ruta_completa(self):
        """
        Devuelve la ruta completa relativa a la imagen.
        """
        return os.path.join(self.pre_ruta, `self.paciente.codigo`, self.ruta)


#class Podologia(SQLObject, PRPCTOO):
#    _connection = conn
#    class sqlmeta:
#        fromDatabase = True
#    paciente = ForeignKey('Paciente')

#    def _init(self, *args, **kw):
#        starter(self, *args, **kw)


## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

if __name__ == '__main__':
    # Pruebas unitarias
    for clase in ('Paciente', 'Diente', 'Cita', 'Presupuesto', 'Fotografia', 'Documento'): #, 'Podologia'):
        try:
            c = eval(clase)
            print "Buscando primer registro de %s... " % (clase),
            reg = c.select(orderBy="id")[0]
            print "[OK]"
        except IndexError:
            print "[KO] - La clase %s no tiene registros" % (clase)


