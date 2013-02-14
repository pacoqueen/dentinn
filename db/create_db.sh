#!/bin/sh

# Crear usuario con la contraseña
echo "(sudo) Añadiendo usuario udentinn2 a PostgreSQL..."
sudo su postgres -c "createuser -d -R -S udentinn2" && echo "ALTER USER udentinn2 WITH PASSWORD 'passudentinn2'\;" | psql template1

# Modificar el pg_hba.conf
if [ -z "$(sudo grep dbdentinn2 /etc/postgresql/*/main/pg_hba.conf | grep udentinn2 | grep password)" ]; then 
    echo "Asegúrate de que el usuario especificado en el fichero de configuración tiene acceso en pg_hba.conf." 
    exit 1
fi

# Crear base de datos
./init_db.sh dbdentinn2 udentinn2 passudentinn2 tablas.sql 

