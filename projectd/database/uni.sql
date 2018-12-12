-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 01, 2018 at 04:03 AM
-- Server version: 5.7.21
-- PHP Version: 5.6.35



SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

DROP TABLE IF EXISTS`category`;
CREATE TABLE IF NOT EXISTS `category`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(25),
PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;



DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(125) NOT NULL,
  `lastName` varchar(125) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(25) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `confirmCode` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;




INSERT INTO `admin` (`id`, `firstName`, `lastName`, `email`, `mobile`, `address`, `password`, `type`, `confirmCode`) VALUES
(1,'swathi','n rao','abc@gmail.com','9856347512','VVpuram,bangalore','123','manager','0');


DROP TABLE IF EXISTS `school`;
CREATE TABLE IF NOT EXISTS `school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `address` varchar(30) NOT NULL,
  `contact` int(10) NOT NULL,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;







DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sid`int(11),
  `firstName` varchar(125) NOT NULL,
  `lastName` varchar(125) NOT NULL,
  `email` varchar(100) NOT NULL ,
  `mobile` varchar(25) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`sid`) REFERENCES `school` (`id`),
  CONSTRAINT `qqqq` UNIQUE (`email`)
  )ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;






DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders`(
  `id` int(11) NOT NULL AUTO_INCREMENT ,
  `uid` int(11) NOT NULL,
  `sid` int(11),
    `total_cost` decimal(11,4),
  `oplace` text NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `dstatus` varchar(10) NOT NULL DEFAULT 'no',
  `odate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ddate` datetime DEFAULT NULL,
  FOREIGN KEY (`uid`) REFERENCES `users` (`id`),
  PRIMARY KEY (`id`,`uid`),
  FOREIGN KEY (`sid`) REFERENCES `school` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `uniform`;
CREATE TABLE IF NOT EXISTS `uniform`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`img` text,
`type` varchar(20) NOT NULL,
`cate` int(11) NOT NULL,
`color` varchar(20),
`size` varchar(5),
`gender` varchar(10),
`cost` decimal(10,4),
`description` varchar(200),
`stock` varchar(10),
`sid` int(11),
PRIMARY KEY (`id`),
FOREIGN KEY (`sid`) REFERENCES `school` (`id`),
FOREIGN KEY (`cate`) REFERENCES `category` (`id`)
)ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;





DROP TABLE IF EXISTS `accessories`;
CREATE TABLE IF NOT EXISTS `accessories`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`img` varchar(200),
`name` varchar(20),
`size` varchar(5),
`cost` decimal(10,4),
`description` varchar(200),
`stock` varchar(10),
`sid` int(11),
PRIMARY KEY (`id`),
FOREIGN KEY (`sid`) REFERENCES `school` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

DROP TABLE IF EXISTS `cart`;
CREATE TABLE IF NOT EXISTS `cart`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`uid` int(11) NOT NULL, 
`product_id` int(11),
`qty` int(2),
FOREIGN KEY (`product_id`) REFERENCES `uniform` (`id`),
 FOREIGN KEY (`uid`) REFERENCES `users` (`id`),
PRIMARY KEY (`id`,`product_id`)

)ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `orddetails`;
CREATE TABLE IF NOT EXISTS `orddetails`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`ord_id` int(11) NOT NULL,
`product_id` int(11),
`qty` int(2),
`cost` decimal(10,4),
FOREIGN KEY (`product_id`) REFERENCES `uniform` (`id`),
PRIMARY KEY (`id`,`product_id`) );
