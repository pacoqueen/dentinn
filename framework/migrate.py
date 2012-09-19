#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg

constring = "host=localhost dbname=dbdentinn user=udentinn2 password=passudentinn2"
connection = psycopg.connect(constring)
cursor = connection.cursor()
cursor.execute("SELECT * FROM datos;")
listapacientes = cursor.fetchall()
pacientes = {}
for p in listapacientes:
    (codigo, nombre, telefono, cp, poblacion, provincia, profesion, fecha_nac, 
     observaciones, protesis, dni, domicilio, padecimientos, alergias) = p
    pacientes[codigo] = {'codigo': codigo, 
                         'nombre': nombre, 
                         'telefono': telefono, 
                         'cp': cp, 
                         'poblacion': poblacion, 
                         'provincia': provincia, 
                         'profesion': profesion, 
                         'fecha_nac': fecha_nac, 
                         'observaciones': observaciones, 
                         'protesis': protesis, 
                         'dni': dni, 
                         'domicilio': domicilio, 
                         'padecimientos': padecimientos, 
                         'alergias': alergias, 
                         'citas': [], 
                         'dientes': [], 
                         'documentos': [], 
                         'fotografias': [], 
                         'presupuestos': []
                        }
cursor.execute("SELECT * FROM citas;")
listacitas = cursor.fetchall()
for c in listacitas:
    (cid, codigo, fecha, ndiente, concepto, debido, pagado) = c
    pacientes[codigo]['citas'].append({'fecha': fecha, 
                                       'ndiente': ndiente, 
                                       'concepto': concepto, 
                                       'debido': debido, 
                                       'pagado': pagado
                                      })
cursor.execute("SELECT * FROM dientes;")
listadientes = cursor.fetchall()
for d in listadientes: 
    tid, codigo, diente, n, s, e, o, c = d
    pacientes[codigo]['dientes'].append({'diente': diente, 
                                         'n': n, 
                                         's': s, 
                                         'e': e, 
                                         'o': o, 
                                         'c': c})
cursor.execute("SELECT * FROM documentos;")
listadocumentos = cursor.fetchall()
for d in listadocumentos:
    did, codigo, tipo, ruta = d
    pacientes[codigo]['documentos'].append({'tipo': tipo, 
                                            'ruta': ruta})
cursor.execute("SELECT * FROM fotografias;")
listafotos = cursor.fetchall()
for f in listafotos:
    fid, codugo, ruta = f
    pacientes[codigo]['fotografias'].append({'ruta': ruta})
cursor.execute("SELECT * FROM presupuestos;")
listapresupuestos = cursor.fetchall()
for p in listapresupuestos:
    pid, codigo, concepto, importe = p
    pacientes[codigo]['presupuestos'].append({'concepto': concepto, 
                                              'importe': importe})


import sys, os, pclases
for r in pclases.Paciente.select():
    r.destroy_en_cascada()

for codigo in pacientes:
    p = pacientes[codigo]
    n = pclases.Paciente(codigo = int(codigo), 
                         nombre = p['nombre'], 
                         domicilio = p['domicilio'],
                         telefono = p['telefono'],
                         cp = p['cp'] != None and p['cp'] or "",
                         poblacion = p['poblacion'],
                         provincia = p['provincia'],
                         profesion = p['profesion'],
                         fechaNac = p['fecha_nac'],
                         alergias = p['alergias'],
                         padecimientos = p['padecimientos'],
                         observaciones = p['observaciones'],
                         protesis = p['protesis'],
                         dni = p['dni'] != None and p['dni'] or "",
                         #nombre = p['nombre'].decode('utf8', 'ignore'), 
                         #domicilio = p['domicilio'].decode('utf8', 'ignore'),
                         #telefono = p['telefono'].decode('utf8', 'ignore'),
                         #cp = p['cp'] != None and p['cp'].decode('utf8', 'ignore') or "",
                         #poblacion = p['poblacion'].decode('utf8', 'ignore'),
                         #provincia = p['provincia'].decode('utf8', 'ignore'),
                         #profesion = p['profesion'].decode('utf8', 'ignore'),
                         #fechaNac = p['fecha_nac'],
                         #alergias = p['alergias'].decode('utf8', 'ignore'),
                         #padecimientos = p['padecimientos'].decode('utf8', 'ignore'),
                         #observaciones = p['observaciones'].decode('utf8', 'ignore'),
                         #protesis = p['protesis'].decode('utf8', 'ignore'),
                         #dni = p['dni'] != None and p['dni'].decode('utf8', 'ignore') or "",
                        )
    # El trigger de la BD ha machacado el código. Lo corrijo:
    n.sync()
    n.codigo = int(codigo)
    n.syncUpdate()
    print codigo + "...", 
    for c in p['citas']:
        nc = pclases.Cita(paciente = n, 
                          fecha = c['fecha'], 
                          ndiente = c['ndiente'], 
                          #concepto = c['concepto'].decode('utf8', 'ignore'), 
                          concepto = c['concepto'], 
                          debido = c['debido'], 
                          pagado = c['pagado']
                         )
        print nc
    for d in p['dientes']: 
        nd = pclases.Diente(paciente = n, 
                            diente = int(d['diente']), 
                            n = d['n'], 
                            s = d['s'], 
                            e = d['e'], 
                            o = d['o'], 
                            c = d['c']
                           ) 
        print nd
    for d in p['documentos']: 
        ruta = d['ruta']
        cod, nombre = ruta.split("/")[-2:]
        #ruta = os.path.abspath("..")
        #ruta = os.path.join(ruta, `int(cod)`, nombre)
        ruta = nombre
        nd = pclases.Documento(paciente = n, 
                               tipo = d['tipo'], 
                               ruta = ruta
                              )
        print nd
    for d in p['fotografias']: 
        ruta = d['ruta']
        cod, nombre = ruta.split("/")[-2:]
        #ruta = os.path.abspath("..")
        #ruta = os.path.join(ruta, `int(cod)`, nombre)
        ruta = nombre
        nd = pclases.Fotografia(paciente = n, 
                                nombre = nombre, 
                                ruta = ruta
                               )
        print nd
    for d in p['presupuestos']: 
        nd = pclases.Presupuesto(paciente = n, 
                                 concepto = d['concepto'], 
                                 #concepto = d['concepto'].decode('utf8', 'ignore'), 
                                 importe = d['importe']
                                )
        print nd

