-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: macmail_db_host
-- Tiempo de generación: 18-07-2023 a las 12:44:33
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
-- Estructura de tabla para la tabla reportes_socialtype
--

CREATE TABLE reportes_socialtype (
  id bigint NOT NULL,
  name varchar(32) DEFAULT NULL,
  description varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla reportes_socialtype
--

INSERT INTO reportes_socialtype (id, name, description) VALUES
(1, 'Facebook account', NULL),
(2, 'Telegram account', NULL),
(3, 'VK account', NULL),
(4, 'Skype ID', NULL),
(5, 'Viber contact', NULL),
(6, 'Instagram comments', NULL),
(7, 'Bitrix24.Network account', NULL),
(8, 'Live Chat', NULL),
(9, 'Open Channel account', NULL),
(10, 'ICQ Number', NULL),
(11, 'MSN/Live!', NULL),
(12, 'Jabber', NULL),
(13, 'Other Contact', NULL),
(14, 'Linked user', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla reportes_socialtype
--
ALTER TABLE reportes_socialtype
  ADD PRIMARY KEY (id);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla reportes_socialtype
--
ALTER TABLE reportes_socialtype
  MODIFY id bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
