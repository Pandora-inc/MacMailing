-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: macmail_db_host
-- Tiempo de generación: 18-07-2023 a las 11:49:12
-- Versión del servidor: 8.0.33
-- Versión de PHP: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: macmail_db
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla reportes_contacttype
--

CREATE TABLE reportes_contacttype (
  id bigint NOT NULL,
  name varchar(32) DEFAULT NULL,
  description varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla reportes_contacttype
--

INSERT INTO reportes_contacttype (id, name, description) VALUES
(1, 'Work Phone', NULL),
(2, 'Mobile', NULL),
(3, 'Fax', NULL),
(4, 'Home Phone', NULL),
(5, 'Pager Number', NULL),
(6, 'SMS marketing phone', NULL),
(7, 'Other Phone Number', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla reportes_contacttype
--
ALTER TABLE reportes_contacttype
  ADD PRIMARY KEY (id);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla reportes_contacttype
--
ALTER TABLE reportes_contacttype
  MODIFY id bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
