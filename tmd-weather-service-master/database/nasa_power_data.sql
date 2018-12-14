-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Sep 29, 2018 at 07:58 AM
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
-- Table structure for table `nasa_power_data`
--

CREATE TABLE IF NOT EXISTS `nasa_power_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `wmo_id` varchar(8) COLLATE utf8_bin DEFAULT NULL,
  `data_year` int(4) DEFAULT NULL,
  `data_month` int(2) DEFAULT NULL,
  `data_day` int(2) DEFAULT NULL,
  `data_doy` int(3) DEFAULT NULL,
  `data_type` varchar(32) COLLATE utf8_bin DEFAULT NULL,
  `data_value` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=7562041 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
