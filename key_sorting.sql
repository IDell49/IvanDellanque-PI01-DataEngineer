
-- Assign all primary keys to each table:

ALTER TABLE `sucursal` ADD PRIMARY KEY(`sucursalId`);
ALTER TABLE `sucursaltipo` ADD PRIMARY KEY(`sucursalTipoId`);
ALTER TABLE `provincialocalidad`  ADD PRIMARY KEY(`provinciaLocalidadId`);
ALTER TABLE `provincia` ADD PRIMARY KEY(`provinciaId`);
ALTER TABLE `comercio_bandera` ADD PRIMARY KEY(`comercioBanderaId`);
ALTER TABLE `marca` ADD PRIMARY KEY(`marcaId`);
ALTER TABLE `producto` ADD PRIMARY KEY(`productoId`);

-- Assign foreign keys to each table:

ALTER TABLE `sucursal` ADD CONSTRAINT `sucursal_fk_comercioBanderaId` FOREIGN KEY (comercioBanderaId) REFERENCES comercio_bandera (comercioBanderaId) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `sucursal` ADD CONSTRAINT `sucursal_fk_sucursalTipoId` FOREIGN KEY (sucursalTipoId) REFERENCES sucursaltipo (sucursalTipoId) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `sucursal` ADD CONSTRAINT `sucursal_fk_provinciaLocalidadId` FOREIGN KEY (provinciaLocalidadId) REFERENCES provincialocalidad (provinciaLocalidadId) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `producto` ADD CONSTRAINT `producto_fk_marcaId` FOREIGN KEY (marcaId) REFERENCES marca (marcaId) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `provincialocalidad` ADD CONSTRAINT `provincialocalidad_fk_provinciaId` FOREIGN KEY (provinciaId) REFERENCES provincia (provinciaId) ON DELETE RESTRICT ON UPDATE RESTRICT;