create database im117;
use im117;
drop database im117;

create table usuarios (
	id int auto_increment primary key,
    usuario varchar(50) not null,
    rol varchar(40) not null,
    password varchar(10) not null
);

drop table usuarios;

insert into usuarios(usuario, rol, password) values
	('Elmer Homero', 'almacen', '12345'),
    ('Esteban Quito', 'mantenimiento', '12345'),
    ('Elsa Pato', 'ventas', '12345'),
    ('Lola Mento', 'proveedores', '12345'),
    ('Zoyla Vaca', 'envios', '12345');
    
select * from usuarios;

create table mantenimiento(
     id int auto_increment primary key,
     nombreA varchar(20) not null,
     tipoServicio enum('Mantenimiento', 'Reparación') not null,
     descripcionFalla text not null,
	 fecha date not null
);

drop table mantenimiento;

insert into mantenimiento(nombreA, tipoServicio, descripcionFalla, fecha) values
     ('AK-47', 'Mantenimiento', 'Revisión general del sistema de disparo', '2024-11-22'),
     ('M16', 'Reparación', 'Cambio de resorte en el mecanismo de disparo', '2024-11-20'),
     ('Glock 19', 'Mantenimiento', 'Limpieza y engrase completo', '2024-11-18');

select * from mantenimiento;

create table pedidos(
     id int auto_increment primary key,
     equipo varchar(50) not null,
     cantidad int not null,
     proveedor varchar(30) not null,
	 fecha date not null,
     comentarios text
);

insert into pedidos(equipo, cantidad, proveedor, fecha, comentarios) values
     ('Pistola Glock 17', 10, 'Proveedor A', '2024-11-01', 'Se requiere entrega antes del 15 de noviembre'),
     ('Rifle AR-15', 5, 'Proveedor B', '2024-11-02', 'Pedido urgente'),
     ('Municiones 9mm', 500, 'Proveedor D', '2024-11-05', 'Incluye embalaje adicional');
     
select * from pedidos;
drop table pedidos;

create table envios(
     id int auto_increment primary key,
     nombre_cliente varchar(30) not null,
     cantidad_arma text not null,
     direccion varchar(50) not null,
	 fecha date not null,
     estado enum('Pendiente', 'Enviado', 'Entregado')
);

drop table envios;

create table armas(
      nombre_arma varchar(20) not null,
      modelo varchar(20) not null,
	  calibre varchar(12) not null,
      numSerie varchar(10) not null primary key,
      sistemaDisparo enum('Tiro a tiro', 'Semiautomático', 'Automático'),
      materiales varchar(50) not null,
      peso varchar(10) not null, 
      costo float not null,
      estado enum('activo', 'sin existencia') default 'activo'
);

insert into armas (nombre_arma, modelo, calibre, numSerie, sistemaDisparo, materiales, peso, costo) values
      ('Beretta M9', 'M9', '9mm', 'A12345678', 'Semiautomático', 'Acero, polímero', '0.9 kg', 5236.00),
      ('AK-47', 'AK-47', '7.62x39mm', 'B98765432', 'Semiautomático', 'Acero', '3.5 kg', 9214.00),
      ('Desert Eagle', 'Mark XIX', '.50 AE', 'D87654321', 'Semiautomático', 'Acero, polímero', '1.9 kg', 6990.00),
      ('Uzi Mini', 'Mini', '9mm', 'F12345678', 'Automático', 'Polímero, acero', '1.2 kg', 5537.00),
      ('MP5K', 'MP5K', '9mm', 'G98765432', 'Automático', 'Polímero, acero', '2.5 kg', 5621.00);

select * from armas;
drop table armas;

create table ventas (
    id_venta int auto_increment primary key,
    fecha date not null,
    numSerie varchar(10) not null,
    cantidad int not null,
    precio_unitario decimal(10, 2) not null,
    total decimal(10, 2) as (cantidad * precio_unitario) stored,
    metodo_pago varchar(50) not null,
    foreign key (numSerie) references armas (numSerie)
);

-- Ventas en 2022, 2023, 2024
insert into ventas (fecha, numSerie, cantidad, precio_unitario, metodo_pago) values
('2022-01-15', 'A12345678', 2, 5236.00, 'Efectivo'),
('2022-02-05', 'B98765432', 3, 9214.00, 'Tarjeta de crédito'),
('2022-03-10', 'D87654321', 1, 6990.00, 'Transferencia bancaria'),
('2022-04-25', 'F12345678', 4, 5537.00, 'Efectivo'),
('2022-05-17', 'G98765432', 2, 5621.00, 'Tarjeta de crédito'),
('2022-06-03', 'A12345678', 5, 5236.00, 'Efectivo'),
('2022-07-20', 'B98765432', 3, 9214.00, 'Efectivo'),
('2022-08-11', 'D87654321', 2, 6990.00, 'Transferencia bancaria'),
('2022-09-02', 'F12345678', 1, 5537.00, 'Tarjeta de crédito'),
('2022-10-14', 'G98765432', 4, 5621.00, 'Efectivo'),
('2022-11-01', 'A12345678', 3, 5236.00, 'Efectivo'),
('2022-12-05', 'B98765432', 2, 9214.00, 'Transferencia bancaria'),
('2022-12-15', 'D87654321', 1, 6990.00, 'Efectivo'),
('2022-12-20', 'F12345678', 5, 5537.00, 'Tarjeta de crédito'),
('2022-12-28', 'G98765432', 3, 5621.00, 'Efectivo'),
('2023-01-10', 'A12345678', 4, 5236.00, 'Efectivo'),
('2023-02-05', 'B98765432', 2, 9214.00, 'Tarjeta de crédito'),
('2023-03-15', 'D87654321', 3, 6990.00, 'Transferencia bancaria'),
('2023-04-20', 'F12345678', 1, 5537.00, 'Efectivo'),
('2023-05-05', 'G98765432', 2, 5621.00, 'Tarjeta de crédito'),
('2023-06-12', 'A12345678', 5, 5236.00, 'Efectivo'),
('2023-07-10', 'B98765432', 3, 9214.00, 'Efectivo'),
('2023-08-01', 'D87654321', 4, 6990.00, 'Transferencia bancaria'),
('2023-09-14', 'F12345678', 2, 5537.00, 'Tarjeta de crédito'),
('2023-10-23', 'G98765432', 5, 5621.00, 'Efectivo'),
('2023-11-03', 'A12345678', 3, 5236.00, 'Efectivo'),
('2023-12-07', 'B98765432', 2, 9214.00, 'Transferencia bancaria'),
('2023-12-11', 'D87654321', 1, 6990.00, 'Efectivo'),
('2023-12-15', 'F12345678', 4, 5537.00, 'Tarjeta de crédito'),
('2023-12-19', 'G98765432', 3, 5621.00, 'Efectivo'),
('2023-12-22', 'A12345678', 2, 5236.00, 'Efectivo'),
('2023-12-25', 'B98765432', 5, 9214.00, 'Tarjeta de crédito'),
('2023-12-29', 'D87654321', 3, 6990.00, 'Transferencia bancaria'),
('2024-01-04', 'F12345678', 4, 5537.00, 'Efectivo'),
('2024-02-11', 'G98765432', 3, 5621.00, 'Tarjeta de crédito'),
('2024-03-01', 'A12345678', 2, 5236.00, 'Efectivo'),
('2024-04-09', 'B98765432', 1, 9214.00, 'Efectivo'),
('2024-05-15', 'D87654321', 5, 6990.00, 'Transferencia bancaria'),
('2024-06-10', 'F12345678', 3, 5537.00, 'Tarjeta de crédito'),
('2024-07-03', 'G98765432', 2, 5621.00, 'Efectivo'),
('2024-08-05', 'A12345678', 4, 5236.00, 'Efectivo'),
('2024-09-10', 'B98765432', 3, 9214.00, 'Tarjeta de crédito'),
('2024-10-01', 'D87654321', 1, 6990.00, 'Efectivo'),
('2024-10-15', 'F12345678', 5, 5537.00, 'Transferencia bancaria'),
('2024-10-18', 'G98765432', 2, 5621.00, 'Tarjeta de crédito'),
('2024-10-22', 'A12345678', 3, 5236.00, 'Efectivo'),
('2024-10-28', 'B98765432', 2, 9214.00, 'Efectivo'),
('2024-11-01', 'D87654321', 4, 6990.00, 'Transferencia bancaria'),
('2024-11-10', 'F12345678', 3, 5537.00, 'Tarjeta de crédito'),
('2024-11-15', 'G98765432', 2, 5621.00, 'Criptomoneda'),
('2024-11-18', 'A12345678', 1, 5236.00, 'Efectivo'),
('2024-11-22', 'B98765432', 5, 9214.00, 'Transferencia bancaria'),
('2024-11-25', 'D87654321', 2, 6990.00, 'Efectivo'),
('2024-11-26', 'F12345678', 4, 5537.00, 'Tarjeta de crédito');

select * from ventas;
drop table ventas;



