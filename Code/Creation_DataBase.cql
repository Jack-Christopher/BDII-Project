CREATE KEYSPACE bd WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = 'true';

USE bd

CREATE TABLE producto (
	id int PRIMARY KEY, 
	nombre text, 
	precio float, 
	stock int, 
	descripcion text
);

CREATE TABLE reserva (
	id int PRIMARY KEY, 
	cantidad float, 
	adelanto float, 
	tipo_venta text
);

CREATE TABLE cliente (
	DNI int PRIMARY KEY, 
	nombre text, 
	apellidos text, 
	tarjeta_credito int, 
	RUC int
);

CREATE TABLE factura (
	id int PRIMARY KEY, 
	costo float, 
	medio_de_pago text
);

CREATE TABLE cajero (
	id int PRIMARY KEY, 
	tipo text
);

CREATE TABLE corte_turno (
	id int PRIMARY KEY, 
	hora_entrada text, 
	hora_salida text, 
	saldo_inicial float, 
	entrada text, 
	devoluciones float, 
	saldo_final float
);

CREATE TABLE empleado (
	id int PRIMARY KEY, 
	nombre text, 
	apellidos text, 
	permisos text
);

CREATE TABLE vale (
	id int PRIMARY KEY, 
	porcentaje float
);

CREATE TABLE gasto (
	id int PRIMARY KEY, 
	cantidad int
);
