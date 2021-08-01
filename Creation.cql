CREATE KEYSPACE IF NOT EXISTS bd WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = 'true' ;

USE bd;

CREATE TABLE IF NOT EXISTS producto (
	id int PRIMARY KEY, 
	nombre text, 
	precio float, 
	stock int, 
	descripcion text
);

CREATE TABLE IF NOT EXISTS reserva (
	id int PRIMARY KEY,
	id_producto int,
	cantidad float, 
	adelanto float, 
	tipo_venta text
);

CREATE TABLE IF NOT EXISTS cliente (
	DNI int PRIMARY KEY, 
	nombre text, 
	apellidos text, 
	tarjeta_credito int,
	RUC int
);

CREATE TABLE IF NOT EXISTS factura (
	id int PRIMARY KEY, 
	id_producto int,
	costo float, 
	medio_de_pago text
);

CREATE TABLE IF NOT EXISTS cajero (
	id int PRIMARY KEY, 
	tipo text
);

CREATE TABLE IF NOT EXISTS corte_turno (
	id int PRIMARY KEY, 
	hora_entrada text, 
	hora_salida text, 
	saldo_inicial float, 
	entrada text, 
	devoluciones float, 
	saldo_final float
);

CREATE TABLE IF NOT EXISTS empleado (
	DNI int PRIMARY KEY, 
	nombre text, 
	apellidos text,
	username text,
	password text,
	permisos text
);

CREATE TABLE IF NOT EXISTS vale (
	id int PRIMARY KEY, 
	porcentaje float
);

CREATE TABLE IF NOT EXISTS gasto (
	id int PRIMARY KEY, 
	cantidad int
);
