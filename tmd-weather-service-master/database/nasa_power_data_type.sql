-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Sep 29, 2018 at 07:57 AM
-- Server version: 5.6.33-log
-- PHP Version: 5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `thgeomat_maindb`
--

-- --------------------------------------------------------

--
-- Table structure for table `nasa_power_data_type`
--

CREATE TABLE IF NOT EXISTS `nasa_power_data_type` (
  `id` int(2) unsigned NOT NULL AUTO_INCREMENT,
  `id_name` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=7 ;

--
-- Dumping data for table `nasa_power_data_type`
--

INSERT INTO `nasa_power_data_type` (`id`, `id_name`) VALUES
(1, 'T2M_MIN'),
(2, 'T2M_MAX'),
(3, 'PRECTOT'),
(4, 'CLRSKY_SFC_SW_DWN'),
(5, 'RH2M'),
(6, 'SG_DAY_HOUR_AVG');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
