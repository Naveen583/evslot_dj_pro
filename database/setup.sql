-- ============================================================
-- EV CHARGE HUB - Database Setup Script
-- Run this file to set up the project database on a new system
-- Command: mysql -u root -p < database/setup.sql
-- ============================================================

-- Step 1: Create and select database
CREATE DATABASE IF NOT EXISTS ev_charging;
USE ev_charging;

-- ============================================================
-- Table: ev_admin
-- ============================================================
CREATE TABLE IF NOT EXISTS `ev_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO `ev_admin` (`username`, `password`) VALUES
('admin', 'admin@');

-- ============================================================
-- Table: ev_register (Users)
-- ============================================================
CREATE TABLE IF NOT EXISTS `ev_register` (
  `name`      varchar(20)  NOT NULL,
  `address`   varchar(40)  NOT NULL,
  `mobile`    bigint       NOT NULL,
  `email`     varchar(40)  NOT NULL,
  `uname`     varchar(20)  NOT NULL,
  `passw`     varchar(128) NOT NULL,
  `latitude`  varchar(20)  DEFAULT '',
  `longitude` varchar(20)  DEFAULT '',
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO `ev_register` (`name`, `address`, `mobile`, `email`, `uname`, `passw`, `latitude`, `longitude`) VALUES
('manu',           'perambalur', 9384432004, 'manuvelu@gmail.com',  'manuvelu', 'manuvelu@', '', ''),
('sachin',         'trichy',     9894442716, 'sachin234@gmail.com', 'sachin',   'sachin@',   '', ''),
('Mohammed safaq', 'vellore',    9894442716, 'Safaq94273@gmail.com','safaq',    'safaq@',    '', '');

-- ============================================================
-- Table: ev_station (Charging Stations)
-- ============================================================
CREATE TABLE IF NOT EXISTS `ev_station` (
  `name`        varchar(20)  NOT NULL,
  `stype`       varchar(20)  NOT NULL DEFAULT 'Private',
  `numcharger`  int          NOT NULL DEFAULT 0,
  `area`        varchar(30)  NOT NULL,
  `city`        varchar(30)  NOT NULL,
  `lat`         varchar(20)  NOT NULL DEFAULT '',
  `lon`         varchar(20)  NOT NULL DEFAULT '',
  `uname`       varchar(20)  NOT NULL,
  `passw`       varchar(20)  NOT NULL,
  `status`      int          NOT NULL DEFAULT 0,
  `landmark`    varchar(30)  NOT NULL DEFAULT '',
  `mobile`      bigint       NOT NULL,
  `email`       varchar(40)  NOT NULL DEFAULT '',
  `distance`    double       NOT NULL DEFAULT 0,
  `is_active`   tinyint(1)   NOT NULL DEFAULT 0,
  `last_seen`   datetime     DEFAULT NULL,
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO `ev_station` (`name`, `stype`, `numcharger`, `area`, `city`, `lat`, `lon`, `uname`, `passw`, `status`, `landmark`, `mobile`, `email`, `distance`, `is_active`, `last_seen`) VALUES
('Auto_LPG', 'Private', 6, 'NH 38',          'Perambalur', '11.201109', '78.878258', 'Auto_LPG_ST', 'Auto_LPG@', 1, 'near Sri Ramakrishna College',    6398765432, 'autolpgstation@gmail.com', 0, 0, NULL),
('Zeon',     'Private', 8, 'NH 38',          'Perambalur', '11.206906', '78.881544', 'Zeon_ST',     'Zeon@',     1, 'Near Aswins Veg Restaurant',      9876543210, 'zeonstation@gmail.com',    0, 0, NULL),
('HPCL',     'Private', 7, 'NH 38, Irungalur','TRICHY',    '10.95453',  '78.75907',  'HPCL_ST',     'HPCL@',     1, 'Chennai to Trichy HW',            9608754321, 'hpclhpcl3452@gmail.com',   0, 0, NULL);

-- ============================================================
-- Table: ev_booking
-- ============================================================
CREATE TABLE IF NOT EXISTS `ev_booking` (
  `id`               int          NOT NULL AUTO_INCREMENT,
  `uname`            varchar(20)  NOT NULL,
  `station`          varchar(20)  NOT NULL,
  `carno`            varchar(20)  NOT NULL,
  `reserve`          varchar(20)  NOT NULL DEFAULT '',
  `slot`             int          NOT NULL,
  `cimage`           varchar(20)  NOT NULL DEFAULT '',
  `mins`             int          NOT NULL DEFAULT 0,
  `plan`             int          NOT NULL DEFAULT 0,
  `amount`           decimal(8,2) NOT NULL DEFAULT 0,
  `rtime`            varchar(20)  NOT NULL DEFAULT '',
  `etime`            varchar(20)  NOT NULL DEFAULT '',
  `rdate`            varchar(15)  NOT NULL DEFAULT '',
  `edate`            varchar(15)  NOT NULL DEFAULT '',
  `otp`              varchar(10)  NOT NULL DEFAULT '',
  `charge`           double       NOT NULL DEFAULT 0,
  `chargetime`       int          NOT NULL DEFAULT 0,
  `chargemin`        int          NOT NULL DEFAULT 0,
  `chargesec`        int          NOT NULL DEFAULT 0,
  `chargest`         int          NOT NULL DEFAULT 0,
  `paymode`          varchar(20)  NOT NULL DEFAULT '',
  `payst`            int          NOT NULL DEFAULT 0,
  `status`           int          NOT NULL DEFAULT 0,
  `btime1`           varchar(20)  NOT NULL DEFAULT '',
  `btime2`           varchar(20)  NOT NULL DEFAULT '',
  `alertst`          int          NOT NULL DEFAULT 0,
  `duration_seconds` int          NOT NULL DEFAULT 0,
  `end_time`         datetime     DEFAULT NULL,
  `smsst`            int          NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_booking_user`    FOREIGN KEY (`uname`)   REFERENCES `ev_register`(`uname`) ON DELETE CASCADE,
  CONSTRAINT `fk_booking_station` FOREIGN KEY (`station`) REFERENCES `ev_station`(`uname`)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO `ev_booking` (`id`, `uname`, `station`, `carno`, `reserve`, `slot`, `cimage`, `mins`, `plan`, `amount`, `rtime`, `etime`, `rdate`, `edate`, `otp`, `charge`, `status`, `btime1`, `btime2`, `chargetime`, `chargemin`, `chargesec`, `chargest`, `paymode`, `payst`, `alertst`, `duration_seconds`, `end_time`, `smsst`) VALUES
(1, 'manuvelu', 'Zeon_ST',     'TN 45 ZS 0418', '1', 3, 'evch.jpg', 5, 3, 300.00, '16:05', '16:10', '2026-01-22', '2026-01-22', '', 0, 3, '16:05', '16:10', 0, 5, 0, 3, 'Cash', 1, 0, 300, '2026-01-22 10:38:30', 0),
(2, 'sachin',   'Auto_LPG_ST', 'TN 65 AX 9978', '1', 2, 'evch.jpg', 5, 3, 300.00, '18:10', '18:15', '2026-01-21', '2026-01-21', '', 0, 1, '18:10', '18:15', 0, 5, 0, 1, '',     0, 0, 0,   NULL,                  0);

-- ============================================================
-- Django migrations table
-- ============================================================
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id`      bigint       NOT NULL AUTO_INCREMENT,
  `app`     varchar(255) NOT NULL,
  `name`    varchar(255) NOT NULL,
  `applied` datetime(6)  NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- SETUP COMPLETE!
-- Next steps in terminal:
--
-- 1. python -m pip install django mysqlclient requests
-- 2. mysql -u root -p < database/setup.sql
-- 3. python manage.py migrate --fake
-- 4. python manage.py createsuperuser
-- 5. python manage.py runserver
-- ============================================================
