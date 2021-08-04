CREATE KEYSPACE IF NOT EXISTS bd WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = 'true' ;

USE bd;

CREATE TABLE IF NOT EXISTS producto (
	id int PRIMARY KEY, 
	id_sucursal int,
	nombre text, 
	precio float, 
	stock int, 
	descripcion text
);

CREATE TABLE IF NOT EXISTS sucursal (
	id int PRIMARY KEY, 
	nombre text
);

CREATE TABLE IF NOT EXISTS reserva (
	id int PRIMARY KEY,
	id_producto int,
	id_sucursal int,
	cantidad float, 
	adelanto float
);

CREATE TABLE IF NOT EXISTS cliente (
	DNI int PRIMARY KEY, 
	nombre text, 
	apellidos text, 
	tarjeta_credito int,
	id_sucursal int
);

CREATE TABLE IF NOT EXISTS factura (
	id int PRIMARY KEY,
	fecha date, 
	id_producto map<int,int>,
	id_sucursal int,
	costo float
);

CREATE TABLE IF NOT EXISTS cajero (
	id int PRIMARY KEY, 
	id_sucursal int,
	tipo text
);

CREATE TABLE IF NOT EXISTS corte_turno (
	id int PRIMARY KEY,
	dni_empleado int, 
	hora_entrada text,
	hora_salida text,
	saldo_inicial float,
	id_sucursal int,
	saldo_final float
);

CREATE TABLE IF NOT EXISTS empleado (
	DNI int PRIMARY KEY, 
	nombre text, 
	apellidos text,
	username text,
	password text,
	id_sucursal int
);

CREATE TABLE IF NOT EXISTS vale (
	id int PRIMARY KEY, 
	id_sucursal int,
	dni_empleado int,
	porcentaje float
);

CREATE TABLE IF NOT EXISTS gasto (
	id int PRIMARY KEY, 
	id_sucursal int,
	cantidad int,
	concepto text
);
