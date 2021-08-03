INSERT INTO BD.empleado (DNI, nombre, apellidos, username, password) 
   VALUES (21376843, 'Jack', 'Huaihua', 'JC', '12345') 
IF NOT EXISTS; 


INSERT INTO BD.cliente (DNI, nombre, apellidos) 
   VALUES (21376843, 'Rommel', 'Ccorahua') 
IF NOT EXISTS; 


INSERT INTO BD.producto (id, nombre, precio, stock, descripcion) 
   VALUES (2143, 'Refrigeradora', 1000, 19, 'Es una buena refrigeradora') 
IF NOT EXISTS; 
INSERT INTO BD.producto (id, nombre, precio, stock, descripcion) 
   VALUES (4637, 'Horno microondas', 450, 32, 'Es un buen horno M.') 
IF NOT EXISTS; 
INSERT INTO BD.producto (id, nombre, precio, stock, descripcion) 
   VALUES (1212, 'Licuadora', 250, 50, 'Licuadora de buena calidad') 
IF NOT EXISTS; 


INSERT INTO BD.factura (id, fecha, costo, id_producto) 
   VALUES (1, '2017-05-05',  4200, {1212 : 2, 2143 : 3} )
IF NOT EXISTS; 
