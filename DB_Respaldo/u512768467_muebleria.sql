-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 09-04-2021 a las 03:59:55
-- Versión del servidor: 10.4.14-MariaDB-cll-lve
-- Versión de PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `u512768467_muebleria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id`, `nombre`, `descripcion`, `estatus`) VALUES
(1, 'Escritorios padres', 'Escritorios bonitos y chiquitos v2', 'Activo'),
(2, 'Repisas de Madera', 'Repisas Bonitas de Madera <3', 'Inactivo'),
(3, 'Repisas', 'Repisas de cualquier material que trabajamos', 'Inactivo'),
(4, 'Archiveros', 'Tipo cajoneras', 'Activo'),
(5, 'Pruebas', 'Prueba de integracion', 'Inactivo'),
(6, 'Prueba 5', 'Prueba 5 Descripción', 'Inactivo'),
(7, 'vfvf 2', 'fvfvf 2', 'Inactivo'),
(8, 'Prueba 3', 'Prueba 3', 'Inactivo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id` int(11) NOT NULL,
  `idPersona` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id`, `idPersona`) VALUES
(1, 2),
(2, 3),
(3, 5),
(4, 6),
(5, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_orden_compra`
--

CREATE TABLE `detalle_orden_compra` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `subtotal` float NOT NULL,
  `material` int(11) DEFAULT NULL,
  `idOrden` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `detalle_orden_compra`
--

INSERT INTO `detalle_orden_compra` (`id`, `cantidad`, `subtotal`, `material`, `idOrden`) VALUES
(1, 50, 500, 1, 1),
(2, 30, 450, 2, 1),
(3, 50, 500, 1, 2),
(4, 30, 450, 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_producto_material`
--

CREATE TABLE `detalle_producto_material` (
  `id` int(11) NOT NULL,
  `alto` float NOT NULL,
  `ancho` float NOT NULL,
  `cantidad` int(11) NOT NULL,
  `idProducto` int(11) DEFAULT NULL,
  `idMaterial` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `detalle_producto_material`
--

INSERT INTO `detalle_producto_material` (`id`, `alto`, `ancho`, `cantidad`, `idProducto`, `idMaterial`) VALUES
(1, 1, 1, 1, 1, 1),
(2, 1, 1, 1, 1, 2),
(3, 1, 1, 1, 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `subtotal` float NOT NULL,
  `venta` int(11) DEFAULT NULL,
  `producto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id`, `cantidad`, `subtotal`, `venta`, `producto`) VALUES
(1, 1, 120, 1, 2),
(2, 1, 270, 1, 1),
(3, 1, 100, 2, 1),
(4, 1, 100, 2, 1),
(5, 2, 200, 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `domicilio`
--

CREATE TABLE `domicilio` (
  `id` int(11) NOT NULL,
  `calle` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `colonia` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_interior` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_exterior` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `municipio` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cp` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `referencias` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `domicilio`
--

INSERT INTO `domicilio` (`id`, `calle`, `colonia`, `numero_interior`, `numero_exterior`, `estado`, `municipio`, `cp`, `referencias`, `estatus`) VALUES
(1, 'Aldama Hernandez', 'BLVD. Torres Landa', '345', '0', 'Guanajuato', 'León', '38909', 'Entre una calle y otra', '1'),
(2, 'Prueba Dom', 'Prueba Dom', '2', '2', 'Prueba Dom', 'Prueba Dom', '33', 'Prueba Dom', '1'),
(3, 'Del toril', 'Azteca Palmas', '1045', 'B', 'Baja Califonia', 'La Paz', '43809', 'Enfrente de una lavanderia', '1'),
(4, 'Del capote ', 'Azteca de oro', '234', '-', 'Morelos', 'Michoacan', '43009', 'Enfrente de una lavanderia', '1'),
(5, 'Del toril', 'Azteca Palmas', '1045', 'B', 'Baja Califonia', 'La Paz', '43809', 'Enfrente de una lavanderia', 'Activo'),
(6, 'Miguel Hidalgo', 'Centro', '104', '106', 'Guanajuato', 'León', '376300', 'A un costado del ciber', 'Activo'),
(7, 'Manuel Doblado', 'Centro', '104', '106', 'Guanajuato', 'León', '37000', 'Frente a la farmacia', 'Activo'),
(8, 'calle1', 'colonia1', '21', '21', 'estado1', 'municipio1', '349591', 'referencia1', '1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `material`
--

CREATE TABLE `material` (
  `id` int(11) NOT NULL,
  `tipo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad` int(11) NOT NULL,
  `alto` float NOT NULL,
  `ancho` float NOT NULL,
  `grosor` float NOT NULL,
  `color` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `material`
--

INSERT INTO `material` (`id`, `tipo`, `nombre`, `descripcion`, `cantidad`, `alto`, `ancho`, `grosor`, `color`, `estatus`) VALUES
(1, 'update', 'update', 'update', 0, 0, 0, 2, 'update', 'Inutilizable'),
(2, 'prueba2', 'prueba2', 'prueba2', 2, 2, 2, 2, 'prueba2', 'Disponible'),
(3, 'prueba3', 'prueba3', 'prueba3', 3, 3, 3, 3, 'prueba3', 'Disponible');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden_compra`
--

CREATE TABLE `orden_compra` (
  `id` int(11) NOT NULL,
  `fecha_orden` date DEFAULT NULL,
  `total` float NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proveedor` int(11) DEFAULT NULL,
  `user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `orden_compra`
--

INSERT INTO `orden_compra` (`id`, `fecha_orden`, `total`, `estatus`, `proveedor`, `user`) VALUES
(1, '2021-04-07', 950, 'Activa', 1, 1),
(2, '2021-04-07', 950, 'Activa', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

CREATE TABLE `persona` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidoP` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidoM` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_fijo` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `celular` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `domicilio` int(11) DEFAULT NULL,
  `rfc` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`id`, `nombre`, `apellidoP`, `apellidoM`, `numero_fijo`, `celular`, `estatus`, `domicilio`, `rfc`) VALUES
(2, 'Oscar', 'Ramirez', 'Rodriguez', '4777987732', '578383838', 'Activo', 1, 'RARO003848YJ'),
(3, 'Prueba Dom', 'Prueba Dom', 'Prueba Dom', '222222', '222222', 'Inactivo', 2, 'Prueba Dom'),
(4, 'Martin', 'Carmona', 'Santillana', '123456789', '0987654321', 'Activo', 3, 'TRMLO1900987Y'),
(5, 'Alvaro Tomas', 'Lopez', 'Santillana', '123456789', '0987654321', 'Activo', 4, 'TRMLO1900987Y'),
(6, 'Martin', 'Carmona', 'Santillana', '123456789', '0987654321', 'Activo', 5, 'TRMLO1900987Y'),
(7, 'NOMBRE1', 'apellidop1', 'apellidom1', '2473871', '483851', 'Activo', 8, 'rfc1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(11) NOT NULL,
  `modelo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `img` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `peso` float NOT NULL,
  `color` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alto` float NOT NULL,
  `ancho` float NOT NULL,
  `largo` float NOT NULL,
  `cantidad` int(11) NOT NULL,
  `cantidad_minima` int(11) NOT NULL,
  `precio` float NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `idCategoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `modelo`, `descripcion`, `img`, `peso`, `color`, `alto`, `ancho`, `largo`, `cantidad`, `cantidad_minima`, `precio`, `estatus`, `idCategoria`) VALUES
(1, 'prueba', 'prueba', 'prueba', 1, 'prueba', 1, 1, 1, 1, 1, 1, 'Activo', 1),
(2, 'prueba2_', 'prueba2_', 'prueba2_', 3, 'prueba2_', 3, 3, 3, 4, 3, 3, 'Inactivo', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rfc` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_contacto` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `puesto_contacto` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono_contacto` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo_contacto` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `idDomicilio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id`, `nombre`, `rfc`, `nombre_contacto`, `puesto_contacto`, `telefono_contacto`, `correo_contacto`, `estatus`, `idDomicilio`) VALUES
(4, 'Maderas Pinos', 'APHL1458L8i40', 'Kenia Fuentes', 'Asistente de Ventas', '4771006925', 'keniaF@gmail.com', 'Activo', 6),
(5, 'Materiales HYG', 'KPHO1458L8I48', 'Juan Lopez', 'Asesor de Ventas', '4771457863', 'juan23@gmail.com', 'Activo', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `role`
--

INSERT INTO `role` (`id`, `name`, `description`) VALUES
(1, 'admin', 'Administrador'),
(2, 'vendedor', 'Vendedor'),
(3, 'almacenista', 'Almacenista');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sobrante_material`
--

CREATE TABLE `sobrante_material` (
  `id` int(11) NOT NULL,
  `alto` float NOT NULL,
  `ancho` float NOT NULL,
  `comentario` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estatus` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `material` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `sobrante_material`
--

INSERT INTO `sobrante_material` (`id`, `alto`, `ancho`, `comentario`, `estatus`, `material`) VALUES
(1, 1, 1, 'prueba', 'Inutilizable', 2),
(2, 4, 4, 'ninguno', 'Inutilizable', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `numero_empleado` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nivel_escolar` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profesion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `observaciones` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `idPersona` int(11) DEFAULT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  `confirmed_at` date DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `numero_empleado`, `correo`, `password`, `nivel_escolar`, `profesion`, `observaciones`, `idPersona`, `estatus`, `confirmed_at`) VALUES
(1, '1', 'jhl@gmail.com', 'xxxx', 'Bachillerato', 'Tecnico', 'S/C', 4, 1, '2021-04-07');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_roles`
--

CREATE TABLE `users_roles` (
  `userId` int(11) DEFAULT NULL,
  `roleId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `id` int(11) NOT NULL,
  `fecha_venta` date DEFAULT NULL,
  `total` float NOT NULL,
  `cliente` int(11) DEFAULT NULL,
  `user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`id`, `fecha_venta`, `total`, `cliente`, `user`) VALUES
(1, '2021-04-08', 390, 2, 1),
(2, '2021-04-08', 400, 2, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idPersona` (`idPersona`);

--
-- Indices de la tabla `detalle_orden_compra`
--
ALTER TABLE `detalle_orden_compra`
  ADD PRIMARY KEY (`id`),
  ADD KEY `material` (`material`),
  ADD KEY `idOrden` (`idOrden`);

--
-- Indices de la tabla `detalle_producto_material`
--
ALTER TABLE `detalle_producto_material`
  ADD PRIMARY KEY (`id`),
  ADD KEY `detalle_producto_material_ibfk_1` (`idProducto`),
  ADD KEY `detalle_producto_material_ibfk_2` (`idMaterial`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `venta` (`venta`),
  ADD KEY `producto` (`producto`);

--
-- Indices de la tabla `domicilio`
--
ALTER TABLE `domicilio`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `orden_compra`
--
ALTER TABLE `orden_compra`
  ADD PRIMARY KEY (`id`),
  ADD KEY `proveedor` (`proveedor`),
  ADD KEY `user` (`user`);

--
-- Indices de la tabla `persona`
--
ALTER TABLE `persona`
  ADD PRIMARY KEY (`id`),
  ADD KEY `domicilio` (`domicilio`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_ibfk_1` (`idCategoria`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_idx` (`idDomicilio`);

--
-- Indices de la tabla `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sobrante_material`
--
ALTER TABLE `sobrante_material`
  ADD PRIMARY KEY (`id`),
  ADD KEY `material` (`material`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `idPersona` (`idPersona`);

--
-- Indices de la tabla `users_roles`
--
ALTER TABLE `users_roles`
  ADD KEY `userId` (`userId`),
  ADD KEY `roleId` (`roleId`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente` (`cliente`),
  ADD KEY `user` (`user`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_orden_compra`
--
ALTER TABLE `detalle_orden_compra`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `detalle_producto_material`
--
ALTER TABLE `detalle_producto_material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `domicilio`
--
ALTER TABLE `domicilio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `material`
--
ALTER TABLE `material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `orden_compra`
--
ALTER TABLE `orden_compra`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `persona`
--
ALTER TABLE `persona`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `role`
--
ALTER TABLE `role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `sobrante_material`
--
ALTER TABLE `sobrante_material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`idPersona`) REFERENCES `persona` (`id`);

--
-- Filtros para la tabla `detalle_orden_compra`
--
ALTER TABLE `detalle_orden_compra`
  ADD CONSTRAINT `detalle_orden_compra_ibfk_1` FOREIGN KEY (`material`) REFERENCES `material` (`id`),
  ADD CONSTRAINT `detalle_orden_compra_ibfk_2` FOREIGN KEY (`idOrden`) REFERENCES `orden_compra` (`id`);

--
-- Filtros para la tabla `detalle_producto_material`
--
ALTER TABLE `detalle_producto_material`
  ADD CONSTRAINT `detalle_producto_material_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`),
  ADD CONSTRAINT `detalle_producto_material_ibfk_2` FOREIGN KEY (`idMaterial`) REFERENCES `material` (`id`);

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`venta`) REFERENCES `venta` (`id`),
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `orden_compra`
--
ALTER TABLE `orden_compra`
  ADD CONSTRAINT `orden_compra_ibfk_1` FOREIGN KEY (`proveedor`) REFERENCES `proveedor` (`id`),
  ADD CONSTRAINT `orden_compra_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`);

--
-- Filtros para la tabla `persona`
--
ALTER TABLE `persona`
  ADD CONSTRAINT `persona_ibfk_1` FOREIGN KEY (`domicilio`) REFERENCES `domicilio` (`id`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`id`);

--
-- Filtros para la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD CONSTRAINT `id` FOREIGN KEY (`idDomicilio`) REFERENCES `domicilio` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `sobrante_material`
--
ALTER TABLE `sobrante_material`
  ADD CONSTRAINT `sobrante_material_ibfk_1` FOREIGN KEY (`material`) REFERENCES `material` (`id`);

--
-- Filtros para la tabla `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`idPersona`) REFERENCES `persona` (`id`);

--
-- Filtros para la tabla `users_roles`
--
ALTER TABLE `users_roles`
  ADD CONSTRAINT `users_roles_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `users_roles_ibfk_2` FOREIGN KEY (`roleId`) REFERENCES `role` (`id`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`cliente`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
