0.- NECESITA postgresq >= 8.1 (En 7.4 falla al crear el lenguaje -subsanable- y al crear la función -error de sintaxix al usar $ para 7.4-).
1.- Crear usuario BD:
su
su postgres
createuser -d -P udentinn2 -s -R
(meter contraseña. -s para que sea superuser y pueda crear lenguajes en la BD.)
1.5.- Editar /etc/postgres/x.x/main/pg_hba.conf y permitir acceso udentinn2 con contraseña, tanto en local (para el init_db) como por red:
host dbdentinn2 udentinn2 0.0.0.0 0.0.0.0 password
local all udentinn2 password
y /etc/init.d/postgresql* restart
2.- Crear base de datos:
exit
exit
cd db
createdb dbdentinn2 -O udentinn2 --encoding UNICODE
psql -U udentinn2 dbdentinn2 < tablas.sql
(o init_db dbdentinn udentinn2 dentinn)
2.5.- Si es postgre 7.4, crear la BD a mano (sin init_db), hacer su postgres y createlang plpgsql dbdentin2; y finalmente  volcar el tablas. Antes hay que editarlo para quitar el CREATE LANGUAGE.
TODO: Sigue fallando al crear la función, no admite el $cod_paciente$.
3.- Crear ginn.conf en framework con los datos correspondientes.
4.- Modificar plantillas ../compartido/plantillas/*.sxw para poner el anagrama y logotipo de la empresa.
5.- Crear o editar ../imgs/logo_empresa.png
