-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Sep 29, 2018 at 07:55 AM
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
-- Table structure for table `tmd_stations`
--

CREATE TABLE IF NOT EXISTS `tmd_stations` (
  `TmdCode` varchar(15) NOT NULL,
  `WmoCode` varchar(10) DEFAULT NULL,
  `StationNameEnglish` varchar(255) DEFAULT NULL,
  `Latitude` float DEFAULT NULL,
  `Longitude` float DEFAULT NULL,
  `HeightAboveMSL` float DEFAULT NULL,
  `HeightofWindWane` float DEFAULT NULL,
  `HeightofBarometer` float DEFAULT NULL,
  `HeightofThermometer` float DEFAULT NULL,
  PRIMARY KEY (`TmdCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tmd_stations`
--

INSERT INTO `tmd_stations` (`TmdCode`, `WmoCode`, `StationNameEnglish`, `Latitude`, `Longitude`, `HeightAboveMSL`, `HeightofWindWane`, `HeightofBarometer`, `HeightofThermometer`) VALUES
('1005001301', '48452', 'BANG KHEN AGROMET.', 13.85, 100.583, 4, -9999, -9999, -9999),
('1033001201', '48455', 'BANGKOK METROPOLIS', 13.7264, 100.56, 3.01, 10, 4.27, 1.25),
('1033001202', '48454', 'BANGKOK PORT (KLONG TOEI)', 13.7069, 100.568, 2.8, 11, 6, 1.25),
('1036001201', '48456', 'DON MUANG AIRPORT', 13.9192, 100.605, 12, 10, 12.3, 17.5),
('1047001301', '48453', 'BANG NA AGROMET.', 13.6664, 100.606, 3, 10, 6.1, 1.25),
('1101001201', '48457', 'PILOT STATION', 13.3939, 100.599, 14, 34, 14.66, 32.4),
('1103001201', '48429', 'SUVARNABHUMI AIRPORT', 13.6864, 100.768, 0.96, -9999, 6.14, -9999),
('1103001301', '48420', 'Samut Prakarn', 13.5167, 100.762, 1.44, 11, 3.9, 1.2),
('1302001301', '48419', 'PATHUMTHANI', 14.1, 100.617, 6, 11, 7, 1.2),
('1601001201', '48426', 'LOP BURI', 14.7997, 100.645, 10, 13, 11.44, 1.2),
('1604001401', '48418', 'BUA CHUM', 15.2667, 101.187, 49.28, 11.17, 51.47, 1.5),
('1804001301', '48402', 'CHAINAT AGROMET.', 15.15, 100.183, 15, 11.5, 16.85, 1.5),
('2001001201', '48459', 'CHON BURI', 13.3667, 100.983, 0.86, 13.6, 2.48, 1.5),
('2004001201', '48461', 'PHATTHAYA', 12.92, 100.869, 58.93, 10, 60.8, 1.2),
('2007001201', '48463', 'LAEM CHABANG', 13.0769, 100.876, 81, 97.3, 81.7, 1.2),
('2008001201', '48460', 'KO SICHANG', 13.1617, 100.802, 24.85, 12.8, 27.38, 1.2),
('2009001201', '48477', 'SATTAHIP', 12.6833, 100.983, 16, 1.5, 18, 1.25),
('2101001201', '48478', 'RAYONG', 12.6322, 101.344, 2.6, 15, 4.54, 1.2),
('2101001301', '48479', 'HUAI PONG AGROMET.', 12.7333, 101.133, 43, 10.2, 45.1, 1.2),
('2201001201', '48480', 'CHANTHA BURI', 12.6167, 102.113, 2.68, 11.5, 3.6, 1.25),
('2202001301', '48481', 'PHLIU  AGROMET.', 12.5086, 102.173, 24, 11.18, 24.1, 1.55),
('2302001201', '48501', 'TRAD', 11.7667, 102.883, 2, 11.1, 4, 1.25),
('2408001301', '48458', 'CHACHOENGSAO', 13.5156, 101.458, 70.17, 11, 70.17, 1.2),
('2501001201', '48430', 'PRACHIN BURI', 14.0584, 101.369, 5.14, 10, 7.14, 1.5),
('2502001401', '48439', 'KABIN BURI', 13.9833, 101.707, 12.74, 11, 12.56, 1.4),
('2701001401', '48440', 'SA KAEW', 13.7889, 102.035, 42.93, 11, 43.16, 1.3),
('2706001201', '48462', 'ARANYA PRATHET', 13.7, 102.583, 47, 14.2, 49, 1.2),
('3001001201', '48431', 'NAKHON RATCHASIMA', 14.9683, 102.086, 186.6, 11.5, 187.02, 1.25),
('3007001401', '48434', 'CHOK CHAI', 14.7189, 102.169, 190.34, 12.5, 193.32, 1.44),
('3021001301', '48435', 'PAKCHONG AGROMET.', 14.6439, 101.332, 386.12, 11.15, 387.92, 1.25),
('3104001401', '48436', 'NANG RONG', 14.5833, 102.8, 179, 11.1, 181.7, 1.5),
('3111001201', '48437', 'BURIRUM', 15.2257, 103.248, 182, 11.3, 184, 2),
('3201001201', '48432', 'SURIN', 14.8833, 103.5, 145.81, 11.5, 147.36, 1.2),
('3201001301', '48433', 'SURIN AGROMET.', 14.8833, 103.45, 142.56, 11, 144.82, 1.25),
('3203001401', '48416', 'THA TUM', 15.3167, 103.683, 127.62, 10.93, 129.3, 1.3),
('3301001301', '48409', 'SI SAKET AGROMET.', 15, 104.05, 122.87, 1, 127.32, 1),
('3401001501', '48407', 'UBON RATCHATHANI', 15.25, 104.867, 122, 11.75, 123.5, 1.5),
('3432001301', '48408', 'UBON RATCHATHANI AGROMET.', 15.2391, 105.023, 129.76, 10.7, 130.56, 1.25),
('3601001201', '48403', 'CHAIYAPHUM', 15.8, 102.033, 182.15, 12.15, 184.39, 1.2),
('4001001201', '48381', 'KHON KAEN', 16.4611, 102.79, 186.97, 18.75, 193.66, 1.25),
('4001001202', '-9999', 'Khon Kaen Airport', -9999, -9999, -9999, -9999, -9999, -9999),
('4001001301', '48384', 'THA PHRA AGROMET.', 16.3333, 102.817, 166, 11, 166.7, 1.25),
('4101001201', '48354', 'UDON THANI', 17.3833, 102.8, 177, 12, 178.1, 1.5),
('4201001201', '48353', 'LOEI', 17.45, 101.733, 252.51, 10.8, 254.25, 1.25),
('4201001301', '48350', 'LOEI AGROMET.', 17.4, 101.733, 260.3, 12, 263.6, 1.3),
('4301001201', '48352', 'NONG KHAI', 17.8672, 102.733, 173.21, 12.5, 174.02, 1.25),
('4403001401', '48382', 'MAHASARAKHAM', 16.2472, 103.068, 153, 11.8, 154, 1.2),
('4501001201', '48405', 'ROI ET', 16.02, 103.744, 140, 11.33, 142.41, 1.2),
('4501001301', '48404', 'ROI ET AGROMET.', 16.0732, 103.608, 153, 11, 155.81, 1.25),
('4603001401', '48390', 'KALASIN', 16.3325, 103.588, 138.75, 11.7, 140.86, 1.3),
('4701001201', '48356', 'SAKON NAKHON', 17.15, 104.133, 171, 10.65, 172, 1.2),
('4701001301', '48355', 'SAKON NAKHON AGROMET.', 17.125, 104.061, 192, 10, 192.03, 1.25),
('4801001201', '48357', 'NAKHON PHANOM', 17.4108, 104.783, 140, 11.2, 147.56, 1.2),
('4801001301', '48358', 'NAKHON PHANOM AGROMET.', 17.4431, 104.774, 153.13, 10, 153.46, 1.25),
('4901001201', '48383', 'MUKDAHAN', 16.5414, 104.729, 138, 11.2, 139.5, 1.5),
('5001001501', '48327', 'CHIANG MAI', 18.79, 98.9769, 313.2, 2.5, 314, 1.25),
('5009001201', '48302', 'DOI ANG KANG', 19.9314, 99.0483, 1529, 14, 1530, 1.5),
('5014001301', '48326', 'MAE JO AGROMET.', 18.7833, 98.9833, 316.53, 11.2, 318.37, 1.25),
('5101001201', '48329', 'LAMPHUN', 18.5672, 99.0339, 296.42, 12, 298.3, 1.5),
('5201001201', '48328', 'LAMPANG', 18.2833, 99.5167, 242, 11.7, 243.83, 1.2),
('5208001201', '48324', 'THOEN', 17.6366, 99.2448, 190.89, 11, 192.03, 1.55),
('5212001301', '48334', 'LAMPANG AGROMET.', 18.3167, 99.2833, 315, 11, 319.02, 1.45),
('5301001201', '48351', 'UTTARADIT', 17.6167, 100.1, 63, 14, 64, 1),
('5401001201', '48330', 'PHRAE', 18.1667, 100.167, 161.79, 12.5, 162.8, 1.2),
('5501001201', '48331', 'NAN', 18.7797, 100.778, 200, 12.07, 201.6, 1.2),
('5501001301', '48333', 'NAN AGROMET.', 18.8667, 100.75, 264, 11, 263.88, 1.25),
('5506001401', '48315', 'THA WANGPHA', 19.1106, 100.802, 234.7, 11.25, 236.52, 1.25),
('5508001401', '48307', 'THUNG CHANG', 19.4119, 100.884, 333.39, 11.94, 334.94, 1.25),
('5601001201', '48310', 'PHAYAO', 19.1333, 99.9, 396.89, 12, 398.94, 1.5),
('5701001201', '48303', 'CHIANG RAI', 19.9614, 99.8814, 390, 10.5, 393, 1.25),
('5701001301', '48304', 'CHAING RAI AGROMET.', 19.8708, 99.7828, 397, 11, 401.05, 5),
('5801001201', '48300', 'MAE HONG SON', 19.299, 97.9758, 267.74, 19.98, 278.48, 1.2),
('5804001201', '48325', 'MAE SARIANG', 18.1667, 97.9333, 211, 11.77, 213, 1.2),
('6001001201', '48400', 'NAKHON SAWAN', 15.6718, 100.132, 33.91, 14, 35.28, 1.2),
('6012001301', '48401', 'TAKFA AGROMET.', 15.3494, 100.53, 86.67, 11, 86.94, 1.25),
('6201001201', '48380', 'KAMPHAENG PHET', 16.4868, 99.527, 80, 12.4, 81.8, 1.5),
('6301001201', '48376', 'TAK', 16.8783, 99.1433, 125.62, 12, 126.62, 1.5),
('6301001301', '48387', 'DOI MU SOE AGROMET.', 16.75, 98.9333, 863, 10.5, 867.8, 1.25),
('6303001201', '48377', 'BHUMIBOL DAM', 17.2439, 99.0025, 143.73, 15, 144.38, 1.25),
('6306001201', '48375', 'MAE SOT', 16.6592, 98.5508, 196, 11.56, 197.46, 1.5),
('6308001401', '48385', 'UMPHANG', 16.0247, 98.8644, 454, 12, 460, 1.25),
('6406001201', '48372', 'SUKHOTHAI*', 17.1061, 99.8, 48.29, 11, 50.2, 1.25),
('6406001301', '48373', 'SI SAMRONG AGROMET.', 17.1614, 99.8617, 54, 10.2, 54.2, 1.25),
('6501001201', '48378', 'PHITSANULOK', 16.7948, 100.279, 44.02, 1, 45.74, 1.25),
('6601001301', '48386', 'PICHIT AGROMET.', 16.4381, 100.293, 35.95, 11, 37.95, 1.2),
('6701001201', '48379', 'PHETCHABUN', 16.4333, 101.15, 114, 10, 116.07, 1.25),
('6703001401', '48374', 'LOM SAK', 16.7736, 101.249, 142.81, 10.75, 144.86, 1.25),
('6705001401', '48413', 'WICHIAN BURI', 15.657, 101.108, 68, 10, 69.7, 1.2),
('6711001301', '-9999', 'Khao Kho Agromet', -9999, -9999, -9999, -9999, -9999, -9999),
('7001001301', '48464', 'RATCHA BURI', 13.4893, 99.7924, 5, 10.7, 0, 1.5),
('7100001201', '48450', 'KANCHANA BURI', 14.0225, 99.5358, 27.53, 14.8, 28.78, 1.25),
('7107001401', '48421', 'THONG PHAPHUM', 14.7422, 98.6364, 97.36, 12.47, 99.29, 1.25),
('7201001201', '48425', 'SUPHAN BURI', 14.4744, 100.139, 7.23, 11.5, 8.83, 1.2),
('7209001301', '48427', 'U THONG AGROMET.', 14.3036, 99.8647, 6, 10.8, 6.68, 1.5),
('7302001301', '48451', 'NAKHONPATHOM', 14.0117, 99.97, 7.46, 11, 9.65, 1.2),
('7601001201', '48465', 'PHETCHA BURI', 12.9994, 100.061, 2.01, 10.5, 3.77, 1.4),
('7701001201', '48500', 'PRACHUAP KHIRIKHAN', 11.8333, 99.8333, 4, 11.7, 5.9, 1.2),
('7707001201', '48475', 'HUA HIN', 12.5861, 99.9625, 4.73, 14, 6.23, 1.5),
('7707001301', '48474', 'NONG PHLUB AGROMET.', 12.5833, 99.7333, 106, 10.5, 107.75, 1.2),
('8001001201', '48552', 'NAKHONSI THAMMARAT', 8.53778, 99.9639, 3.14, 14.5, 5.54, 1.25),
('8004001401', '48557', 'CHAWANG', 8.43194, 99.5119, 28.12, 12, 30.37, 1.25),
('8015001201', '48553', 'KHANOM', 9.24306, 99.8575, 5, 1, 1, 1),
('8015001301', '48554', 'NAKHONSI THAMMARAT AGROMET.', 8.35931, 100, 1.81, 10.8, 3.02, 0.9),
('8101001201', '48563', 'KRABI', 8.10361, 98.9753, 8, -9999, -9999, -9999),
('8103001201', '48566', 'KO LANTA', 7.53333, 99.05, 2, 1, 5.5, 1.8),
('8205001201', '48561', 'TAKUA PA', 8.68417, 98.2522, 5.93, 11, 7.72, 1.2),
('8301001201', '48564', 'PHUKET', 7.88333, 98.4, 1.83, 10, 3.8, 1.2),
('8303001501', '48565', 'PHUKET AIRPORT', 8.145, 98.3144, 5.86, 10.15, 8.66, 1.2),
('8401001201', '-9999', 'SURAT THANI AIRPORT', 9.13556, 99.1519, 5, -9999, -9999, -9999),
('8402001301', '48555', 'SURAT THANI AGROMET.', 9.1, 99.6333, 36.8, 11.5, 36.8, 1.25),
('8404001201', '48550', 'KO SAMUI', 9.46667, 100.05, 4, 12.25, 5, 1.25),
('8416001401', '48556', 'PHRA SANG', 8.57022, 99.2582, 12.08, 12, 14.05, 1.5),
('8417001201', '48551', 'SURAT THANI', 9.13556, 99.1519, 5, 10, 6.95, 1.25),
('8501001201', '48532', 'RANONG', 9.98333, 98.6167, 7, 10.5, 7.99, 1.25),
('8601001201', '48517', 'CHUMPHON', 10.4987, 99.1885, 4.4, 11.9, 5.95, 1.2),
('8607001301', '48520', 'SAWI AGROMET.', 10.3333, 99.1, 13, 10, 13.33, 1.25),
('9001001501', '48568', 'SONGKHLA', 7.18211, 100.608, 4.57, 18, 6.56, 1.3),
('9010001401', '48574', 'SA DAO', 6.79806, 100.391, 24.7, 10, 25.5, 1.25),
('9011001202', '48569', 'HAT YAI AIRPORT', 6.91667, 100.433, 27.4, 10, 34.93, 1.25),
('9011001301', '48571', 'KHO HONG AGROMET.', 7, 100.5, 6.96, 10.8, 9.73, 1.25),
('9101001201', '48570', 'SATUN', 6.65, 100.083, 4.06, 11.2, 5.96, 1.2),
('9201001201', '48567', 'TRANG AIRPORT', 7.51667, 99.6167, 14.32, 12, 15.83, 1.28),
('9301001301', '48560', 'PHATTHALUNG AGROMET.', 7.58333, 100.167, 2, 11, 4.15, 1.25),
('9403001201', '48580', 'PATTANI AIRPORT', 6.78333, 101.15, 4.05, 10.8, 6.01, 1.2),
('9501001301', '48581', 'YALA AGROMET.', 6.51667, 101.283, 30, 11, 36.04, 1.25),
('9601001201', '48583', 'NARATHIWAT', 6.41667, 101.817, 3.57, 12.25, 5.13, 1.2);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;