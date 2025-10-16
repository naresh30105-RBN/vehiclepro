-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 05, 2023 at 10:33 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `2numperplatecomdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `complainttb`
--

CREATE TABLE `complainttb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `VehicleNo` varchar(250) NOT NULL,
  `Complaint` varchar(250) NOT NULL,
  `Date` date NOT NULL,
  `Status` varchar(20) NOT NULL,
  `VehicleType` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `complainttb`
--

INSERT INTO `complainttb` (`id`, `UserName`, `Mobile`, `VehicleNo`, `Complaint`, `Date`, `Status`, `VehicleType`) VALUES
(1, 'jai', '9486365535', '21BH2345AA', 'missing', '2023-03-05', 'Find', 'TWO WHEELER');

-- --------------------------------------------------------

--
-- Table structure for table `entrytb`
--

CREATE TABLE `entrytb` (
  `id` bigint(20) NOT NULL auto_increment,
  `VehicleNo` varchar(250) NOT NULL,
  `Date` varchar(250) NOT NULL,
  `Time` varchar(250) NOT NULL,
  `FineAmount` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `entrytb`
--

INSERT INTO `entrytb` (`id`, `VehicleNo`, `Date`, `Time`, `FineAmount`, `Status`) VALUES
(1, '21BH2345AA', '2023-03-05', '16:00:05', '500', 'NotPaid');

-- --------------------------------------------------------

--
-- Table structure for table `insuratb`
--

CREATE TABLE `insuratb` (
  `id` bigint(10) NOT NULL auto_increment,
  `VehicleNo` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `PolicyNo` varchar(250) NOT NULL,
  `ExpiryDate` date NOT NULL,
  `PolicyAmount` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `insuratb`
--

INSERT INTO `insuratb` (`id`, `VehicleNo`, `Mobile`, `PolicyNo`, `ExpiryDate`, `PolicyAmount`) VALUES
(1, '21BH2345AA', '9486365535', '2135237345874', '2023-03-04', '600');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `VehicleNo` varchar(50) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `VehicleType` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Mobile`, `Email`, `VehicleNo`, `UserName`, `Password`, `VehicleType`) VALUES
(2, 'jai', '9486365535', 'sangeeth5535@gmail.com', '21BH2345AA', 'jai', 'jai', 'TWO WHEELER');
