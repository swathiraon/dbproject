

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

















DROP TABLE IF EXISTS `orddetails`;
CREATE TABLE IF NOT EXISTS `orddetails`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`ord_id` int(11) NOT NULL,
`product_id` int(11) NOT NULL,
`qty` int(2),
`cost` decimal(10,4),
FOREIGN KEY (`product_id`) REFERENCES `uniform` (`id`),
FOREIGN KEY (`ord_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
PRIMARY KEY (`id`,`product_id`) )ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;



UPDATE orddetails INNER JOIN uniform ON orddetails.product_id = uniform.id SET orddetails.cost=uniform.cost