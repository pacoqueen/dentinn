--##############################################################################
-- Copyright (C) 2005, 2006 Francisco José Rodríguez Bogado,                   #
--                          (pacoqueen@users.sourceforge.net)                  #
--                                                                             #
-- This file is part of Dent-Inn.                                              #
--                                                                             #
-- Dent-Inn is free software; you can redistribute it and/or modify            #
-- it under the terms of the GNU General Public License as published by        #
-- the Free Software Foundation; either version 2 of the License, or           #
-- (at your option) any later version.                                         #
--                                                                             #
-- Dent-Inn is distributed in the hope that it will be useful,                 #
-- but WITHOUT ANY WARRANTY; without even the implied warranty of              #
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
-- GNU General Public License for more details.                                #
--                                                                             #
-- You should have received a copy of the GNU General Public License           #
-- along with Dent-Inn; if not, write to the Free Software                     #
-- Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
--##############################################################################

-------------------------------------------------------------
-- Script de creación de tablas para la aplicación Dent-INN
-------------------------------------------------------------
-- Uso:
-- createdb dentinndb
-- psql -U dentinn -W -h localhost dentinndb < tablas.sql 2>&1 | grep ERROR
-- Con el usuario dentinn ya creado, por supuesto.
------------------------------------------------------------------------------------

------------------------
-- Datos del paciente --
------------------------
CREATE TABLE paciente(
    id SERIAL PRIMARY KEY,
    codigo INT UNIQUE,  -- Si no SQLObject no sabrá cómo crearlo y no dejará al TRIGGER poner el valor correcto.
    nombre TEXT DEFAULT '', 
    domicilio TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    poblacion TEXT DEFAULT '',
    provincia TEXT DEFAULT '',
    profesion TEXT DEFAULT '',
    fecha_nac DATE DEFAULT CURRENT_DATE, 
    alergias TEXT DEFAULT '',
    padecimientos TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    protesis TEXT DEFAULT '',
    dni TEXT DEFAULT '', 
    --------------------------------------
    -- Historia clínica quiropodológica --
    --------------------------------------
    -- 1 --
    motivo_consulta TEXT DEFAULT '', 
    -- 2.- Antecedentes medicoquirúrgicos 
    p_alergias TEXT DEFAULT '', 
    patologias_otro_nivel TEXT DEFAULT '', 
    medicacion TEXT DEFAULT '', 
    cirugias TEXT DEFAULT '', 
    -- 3.- Antecedentes podológicos
    primera_vez TEXT DEFAULT '', 
    seguido_algun_tratamiento TEXT DEFAULT '', 
    cual_y_durante_cuanto_tiempo TEXT DEFAULT '', 
    -- 4.- Antecedentes personales 
    actividad_laboral TEXT DEFAULT '', 
    deportes TEXT DEFAULT '', 
    -- 5.- Exploración de la piel 
    coloracion TEXT DEFAULT '', 
    temperatura TEXT DEFAULT '', 
    edema TEXT DEFAULT '', 
    ampollas TEXT DEFAULT '', 
    queratopatias TEXT DEFAULT '', 
    infecciones TEXT DEFAULT '', 
    anhidrosis TEXT DEFAULT '', 
    hiperhidrosis TEXT DEFAULT '', 
    bromhidrosis TEXT DEFAULT '', 
    -- 6.- Uñas onicocriptosis 
    onicodistrofias TEXT DEFAULT '', 
    onicogrifosis TEXT DEFAULT '', 
    oniquia TEXT DEFAULT '', 
    paroniquia TEXT DEFAULT '', 
    modificacion_color TEXT DEFAULT '', 
    desprendimiento TEXT DEFAULT '', 
    tumores_ungueales TEXT DEFAULT '', 
    estriaciones_transversal TEXT DEFAULT '', 
    estriaciones_longitudinal TEXT DEFAULT '', 
    -- 7.- Exploración física 
    hiperqueratosis TEXT DEFAULT '', 
    helomas TEXT DEFAULT '', 
    alteraciones TEXT DEFAULT '', 
    horizontal TEXT DEFAULT '', 
    frontal TEXT DEFAULT '', 
    valoracion_articular TEXT DEFAULT '', 
    en_carga TEXT DEFAULT '', 
    movilizacion TEXT DEFAULT '', 
    primer_radio TEXT DEFAULT '', 
    exploracion_marcha TEXT DEFAULT '', 
    diagnostico TEXT DEFAULT '', 
    tratamiento TEXT DEFAULT '' 
);


-------------------
-- Tabla Dientes --
-------------------
-- codigo es clave externa de datos, para la relación uno a muchos
-- diente es el número de diente
-- afección indica un tipo de afección (de 0 a 11)
-- TO-DO: afecciones y tipo de afecciones deberían ir en otra tabla para estar en 3ª forma normal. 
--  También podría usar un tipo ARRAY...
-- No puede asociarse un paciente con un mismo número de diente
-- más de una vez (UNIQUE).
-- Cada paciente tendrá 32 dientes únicos y como máximo. 
-----------------

CREATE TABLE diente (
  id SERIAL PRIMARY KEY,
  paciente_id INT NOT NULL REFERENCES paciente,
  diente INT,
  N  INT DEFAULT 0,
  S  INT DEFAULT 0,
  E  INT DEFAULT 0,
  O  INT DEFAULT 0,  
  -- C  INT DEFAULT 0
  -- SQLite3 soporta UNIQUE, pero SQLObject con SQLite3 como backend no 
  -- entiende la cláusula y casca al cargar las tablas de la BD.
  C  INT DEFAULT 0,  
  UNIQUE (paciente_id, diente)
);


-----------------
-- Tabla Citas --
-----------------

CREATE TABLE cita (
  id SERIAL PRIMARY KEY,
  paciente_id INT NOT NULL REFERENCES paciente,
  fecha DATE DEFAULT CURRENT_DATE,
  ndiente TEXT DEFAULT '',
  concepto TEXT DEFAULT '',
  debido FLOAT DEFAULT 0.0,
  pagado FLOAT DEFAULT 0.0
);

------------------------
-- Tabla presupuestos --
------------------------

CREATE TABLE presupuesto (
  id SERIAL PRIMARY KEY, 
  paciente_id INT NOT NULL REFERENCES paciente,
  concepto TEXT DEFAULT '',
  importe FLOAT DEFAULT 0.0
);

-----------------------
-- Tabla fotografías --
-----------------------

CREATE TABLE fotografia (
  id  SERIAL PRIMARY KEY,
  paciente_id INT NOT NULL REFERENCES paciente,
  nombre TEXT DEFAULT '', 
  ruta TEXT     -- Nombre del archivo. Usaré rutas relativas al directorio ui
                -- "../compartido" para evitar separadores de directorios heterogéneos.
);

----------------------
-- Tabla documentos --
----------------------
-- tipo es 1,2 ó 3, dependiendo del tipo 
-- de documento que sea (autorización, 
-- correspondencia, otro).

CREATE TABLE documento (
    id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL REFERENCES paciente,
    tipo INT,
    ruta TEXT
);

--------------------------------------
-- Historia clínica quiropodológica --
--------------------------------------
--CREATE TABLE podologia (
--    id SERIAL PRIMARY KEY, 
--    paciente_id INT NOT NULL REFERENCES paciente, 
--    -- 1 --
--    motivo_consulta TEXT DEFAULT '', 
--    -- 2.- Antecedentes medicoquirúrgicos 
--    alergias TEXT DEFAULT '', 
--    patologias_otro_nivel TEXT DEFAULT '', 
--    medicacion TEXT DEFAULT '', 
--    cirugias TEXT DEFAULT '', 
--    -- 3.- Antecedentes podológicos
--    primera_vez TEXT DEFAULT '', 
--    seguido_algun_tratamiento TEXT DEFAULT '', 
--    cual_y_durante_cuanto_tiempo TEXT DEFAULT '', 
--    -- 4.- Antecedentes personales 
--    actividad_laboral TEXT DEFAULT '', 
--    deportes TEXT DEFAULT '', 
--    -- 5.- Exploración de la piel 
--    coloracion TEXT DEFAULT '', 
--    temperatura TEXT DEFAULT '', 
--    edema TEXT DEFAULT '', 
--    ampollas TEXT DEFAULT '', 
--    queratopatias TEXT DEFAULT '', 
--    infecciones TEXT DEFAULT '', 
--    anhidrosis TEXT DEFAULT '', 
--    hiperhidrosis TEXT DEFAULT '', 
--    bromhidrosis TEXT DEFAULT '', 
--    -- 6.- Uñas onicocriptosis 
--    onicodistrofias TEXT DEFAULT '', 
--    onicogrifosis TEXT DEFAULT '', 
--    oniquia TEXT DEFAULT '', 
--    paroniquia TEXT DEFAULT '', 
--    modificacion_color TEXT DEFAULT '', 
--    desprendimiento TEXT DEFAULT '', 
--    tumores_ungueales TEXT DEFAULT '', 
--    estriaciones_transversal TEXT DEFAULT '', 
--    estriaciones_longitudinal TEXT DEFAULT '', 
--    -- 7.- Exploración física 
--    hiperqueratosis TEXT DEFAULT '', 
--    helomas TEXT DEFAULT '', 
--    alteraciones TEXT DEFAULT '', 
--    horizontal TEXT DEFAULT '', 
--    frontal TEXT DEFAULT '', 
--    valoracion_articular TEXT DEFAULT '', 
--    en_carga TEXT DEFAULT '', 
--    movilizacion TEXT DEFAULT '', 
--    primer_radio TEXT DEFAULT '', 
--    exploracion_marcha TEXT DEFAULT '', 
--    diagnostico TEXT DEFAULT '', 
--    tratamiento TEXT DEFAULT '' 
--);

CREATE FUNCTION ultimo_paciente_mas_uno()
    RETURNS INT
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(codigo), 0) + 1 FROM paciente;';

CREATE LANGUAGE plpgsql;

CREATE FUNCTION set_nuevo_codigo_paciente() RETURNS trigger AS $cod_paciente$
    BEGIN
        NEW.codigo := ultimo_paciente_mas_uno();
        RETURN NEW;
    END;
$cod_paciente$ LANGUAGE plpgsql;

CREATE TRIGGER cod_paciente BEFORE INSERT ON paciente
    FOR EACH ROW EXECUTE PROCEDURE set_nuevo_codigo_paciente();

