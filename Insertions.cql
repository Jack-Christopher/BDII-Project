INSERT INTO BD.sucursal (id, nombre) 
   VALUES (1, 'Sucursal  Lima') 
IF NOT EXISTS; 
INSERT INTO BD.sucursal (id, nombre) 
   VALUES (2, 'Sucursal  Arequipa') 
IF NOT EXISTS; 
INSERT INTO BD.sucursal (id, nombre) 
   VALUES (3, 'Sucursal  Tacna') 
IF NOT EXISTS; 


INSERT INTO BD.empleado (DNI, id_sucursal, nombre, apellidos, username, password) 
   VALUES (21376843, 2,'Jack', 'Huaihua', 'JC', '12345') 
IF NOT EXISTS; 


INSERT INTO BD.cliente (DNI, id_sucursal, nombre, apellidos) 
   VALUES (21376843, 2,'Rommel', 'Ccorahua') 
IF NOT EXISTS; 

INSERT INTO BD.producto (id, id_sucursal, nombre, precio, stock, descripcion) 
   VALUES (5465, 2, 'Secadora', 200, 0, 'De buena calidad') 
IF NOT EXISTS; 

INSERT INTO BD.producto (id, id_sucursal, nombre, precio, stock, descripcion) 
   VALUES (2143, 2, 'Refrigeradora', 1000, 19, 'Es una buena refrigeradora') 
IF NOT EXISTS; 
INSERT INTO BD.producto (id, id_sucursal, nombre, precio, stock, descripcion) 
   VALUES (4637, 2, 'Horno microondas', 450, 32, 'Es un buen horno M.') 
IF NOT EXISTS; 
INSERT INTO BD.producto (id, id_sucursal, nombre, precio, stock, descripcion) 
   VALUES (1212, 2, 'Licuadora', 250, 50, 'Licuadora de buena calidad') 
IF NOT EXISTS; 


INSERT INTO BD.factura (id, id_sucursal, fecha, costo, id_producto) 
   VALUES (1, 2, '2017-05-05',  4200, {1212 : 2, 2143 : 3} )
IF NOT EXISTS; 



INSERT INTO BD.corte_turno (id, hora_entrada, hora_salida, saldo_inicial, id_sucursal,  saldo_final) 
   VALUES (1, '13:00', '18:00', 30000, 2, 35000)
IF NOT EXISTS; 
INSERT INTO BD.corte_turno (id, hora_entrada, hora_salida, saldo_inicial, id_sucursal,  saldo_final) 
   VALUES (2, '18:00', '22:00', 35000, 2, 45000)
IF NOT EXISTS; 



INSERT INTO BD.vale (id, id_sucursal, dni_empleado, porcentaje) 
   VALUES (1, 2, 21376843, 20 )
IF NOT EXISTS; 
INSERT INTO BD.vale (id, id_sucursal, dni_empleado, porcentaje) 
   VALUES (2, 1, 123465566, 15 )
IF NOT EXISTS; 


INSERT INTO BD.gasto (id, id_sucursal, cantidad, concepto) 
   VALUES (1, 2, 800, 'Limpieza diaria' )
IF NOT EXISTS; 
INSERT INTO BD.gasto (id, id_sucursal, cantidad, concepto) 
   VALUES (2, 2, 20000, 'Pago de empleados' )
IF NOT EXISTS; 


INSERT INTO BD.reserva (id, id_producto, id_sucursal, cantidad, adelanto) 
   VALUES (1, 1212, 2, 2, 100 )
IF NOT EXISTS; 
INSERT INTO BD.reserva (id, id_producto, id_sucursal, cantidad, adelanto) 
   VALUES (2, 2134 , 2, 2, 100 )
IF NOT EXISTS; 