SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE IF NOT EXISTS `ev_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO `ev_admin` VALUES ('admin','admin@');

CREATE TABLE IF NOT EXISTS `ev_register` (
  `name` varchar(20) NOT NULL,
  `address` varchar(40) NOT NULL,
  `mobile` bigint NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `passw` varchar(128) NOT NULL,
  `latitude` varchar(20) DEFAULT '',
  `longitude` varchar(20) DEFAULT '',
  `account` varchar(20) NOT NULL DEFAULT '',
  `card` varchar(20) NOT NULL DEFAULT '',
  `bank` varchar(20) NOT NULL DEFAULT '',
  `amount` double NOT NULL DEFAULT 10000,
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO `ev_register` VALUES ('manu','perambalur',9384432004,'manuvelu@gmail.com','manuvelu','manuvelu@','','','','','',10000),('sachin','trichy',9894442716,'sachin234@gmail.com','sachin','sachin@','','','','','',10000);

CREATE TABLE IF NOT EXISTS `ev_booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) NOT NULL,
  `station` varchar(20) NOT NULL,
  `carno` varchar(20) NOT NULL DEFAULT '',
  `reserve` varchar(20) NOT NULL DEFAULT '',
  `slot` int NOT NULL DEFAULT 0,
  `cimage` varchar(20) NOT NULL DEFAULT '',
  `mins` int NOT NULL DEFAULT 0,
  `plan` int NOT NULL DEFAULT 0,
  `amount` decimal(8,2) NOT NULL DEFAULT 0.00,
  `rtime` varchar(20) NOT NULL DEFAULT '',
  `etime` varchar(20) NOT NULL DEFAULT '',
  `rdate` varchar(15) NOT NULL DEFAULT '',
  `edate` varchar(15) NOT NULL DEFAULT '',
  `otp` varchar(10) NOT NULL DEFAULT '',
  `charge` double NOT NULL DEFAULT 0,
  `chargetime` int NOT NULL DEFAULT 0,
  `chargemin` int NOT NULL DEFAULT 0,
  `chargesec` int NOT NULL DEFAULT 0,
  `chargest` int NOT NULL DEFAULT 0,
  `paymode` varchar(20) NOT NULL DEFAULT '',
  `payst` int NOT NULL DEFAULT 0,
  `status` int NOT NULL DEFAULT 0,
  `btime1` varchar(20) NOT NULL DEFAULT '',
  `btime2` varchar(20) NOT NULL DEFAULT '',
  `alertst` int NOT NULL DEFAULT 0,
  `duration_seconds` int NOT NULL DEFAULT 0,
  `end_time` datetime DEFAULT NULL,
  `smsst` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS=1;
