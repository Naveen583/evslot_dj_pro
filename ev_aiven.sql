
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add ev admin',7,'add_evadmin'),(26,'Can change ev admin',7,'change_evadmin'),(27,'Can delete ev admin',7,'delete_evadmin'),(28,'Can view ev admin',7,'view_evadmin'),(29,'Can add ev booking',8,'add_evbooking'),(30,'Can change ev booking',8,'change_evbooking'),(31,'Can delete ev booking',8,'delete_evbooking'),(32,'Can view ev booking',8,'view_evbooking'),(33,'Can add ev register',9,'add_evregister'),(34,'Can change ev register',9,'change_evregister'),(35,'Can delete ev register',9,'delete_evregister'),(36,'Can view ev register',9,'view_evregister'),(37,'Can add ev station',10,'add_evstation'),(38,'Can change ev station',10,'change_evstation'),(39,'Can delete ev station',10,'delete_evstation'),(40,'Can view ev station',10,'view_evstation');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (1,'pbkdf2_sha256$1200000$HCH79PZTihP8NFflgqASJj$CQlkqIj75kkCSj60Bxeg8qorH/Hpd8YkC/7yQ+0OVvI=','2026-04-08 05:22:09.960418',1,'Naveen_Admin','','','naveen@gmail.com',1,1,'2026-04-05 08:05:58.646006');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES (1,'2026-04-05 09:24:41.999980','yuva','EVRegister object (yuva)',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(7,'charging','evadmin'),(8,'charging','evbooking'),(9,'charging','evregister'),(10,'charging','evstation'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (1,'contenttypes','0001_initial','2026-04-05 07:55:27.601879'),(2,'auth','0001_initial','2026-04-05 07:55:29.117227'),(3,'admin','0001_initial','2026-04-05 07:55:29.454074'),(4,'admin','0002_logentry_remove_auto_add','2026-04-05 07:55:29.469207'),(5,'admin','0003_logentry_add_action_flag_choices','2026-04-05 07:55:29.490537'),(6,'contenttypes','0002_remove_content_type_name','2026-04-05 07:55:29.698695'),(7,'auth','0002_alter_permission_name_max_length','2026-04-05 07:55:29.834589'),(8,'auth','0003_alter_user_email_max_length','2026-04-05 07:55:29.878212'),(9,'auth','0004_alter_user_username_opts','2026-04-05 07:55:29.893923'),(10,'auth','0005_alter_user_last_login_null','2026-04-05 07:55:30.020719'),(11,'auth','0006_require_contenttypes_0002','2026-04-05 07:55:30.031455'),(12,'auth','0007_alter_validators_add_error_messages','2026-04-05 07:55:30.045568'),(13,'auth','0008_alter_user_username_max_length','2026-04-05 07:55:30.193277'),(14,'auth','0009_alter_user_last_name_max_length','2026-04-05 07:55:30.333823'),(15,'auth','0010_alter_group_name_max_length','2026-04-05 07:55:30.366922'),(16,'auth','0011_update_proxy_permissions','2026-04-05 07:55:30.380871'),(17,'auth','0012_alter_user_first_name_max_length','2026-04-05 07:55:30.523194'),(18,'charging','0001_initial','2026-04-05 07:55:44.214261'),(19,'charging','0002_evstation_is_active','2026-04-05 07:55:44.222115'),(20,'charging','0003_remove_charginghistory_booking_remove_evslot_station_and_more','2026-04-05 07:55:44.230185'),(21,'charging','0004_remove_evstation_last_seen','2026-04-05 07:55:44.239012'),(22,'charging','0005_evstation_last_seen','2026-04-05 07:55:44.247026'),(23,'sessions','0001_initial','2026-04-05 07:55:53.767833');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES ('4bp8qc2rdezgb0gqq5dl70puceve0rj8','eyJ1c2VyIjoiTmF2ZWVuQCJ9:1wBSoX:kJo7EsWndXZ3vwmIbSowMF740QDoPyrg7IWSfyjZyKY','2026-04-12 07:31:33.936204'),('v7jtyxacwjdvbb3j2ca40l12y6sy4z15','.eJxVjs0KgzAQhN9lzxJMNRo99t5nkN2N0fQnARMtpfTdS8SLp4GZj4_5ApqX89AfWcCAa5qHNY7L4Az0IM8dIT9GnwdzRz8FwcGnxZHIiDjWKG7BjM_rwZ4EM8Y5azvWpbTWaOLOYq3sRZVGl9QQt6RQVa2tWmkr1iSxwY60xNKokRpW3OVXWQc9fNYNoQAK4eH8tJ-uC4gJkwt-CG-_Uxs6-P0BcfJOrA:1w9JiV:5EtLkBGJMSkh4xl18TzMWcHtS1mXWfZ9V74no9zqdpI','2026-04-06 09:24:27.826247');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
DROP TABLE IF EXISTS `ev_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ev_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `ev_admin` DISABLE KEYS */;
INSERT INTO `ev_admin` (`username`, `password`) VALUES ('admin','admin@');
/*!40000 ALTER TABLE `ev_admin` ENABLE KEYS */;
DROP TABLE IF EXISTS `ev_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ev_booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) NOT NULL,
  `station` varchar(20) NOT NULL,
  `carno` varchar(20) NOT NULL,
  `reserve` varchar(20) NOT NULL DEFAULT '',
  `slot` int NOT NULL,
  `cimage` varchar(20) NOT NULL DEFAULT '',
  `mins` int NOT NULL DEFAULT '0',
  `plan` int NOT NULL DEFAULT '0',
  `amount` decimal(8,2) NOT NULL DEFAULT '0.00',
  `rtime` varchar(20) NOT NULL DEFAULT '',
  `etime` varchar(20) NOT NULL DEFAULT '',
  `rdate` varchar(15) NOT NULL DEFAULT '',
  `edate` varchar(15) NOT NULL DEFAULT '',
  `otp` varchar(10) NOT NULL DEFAULT '',
  `charge` double NOT NULL DEFAULT '0',
  `chargetime` int NOT NULL DEFAULT '0',
  `chargemin` int NOT NULL DEFAULT '0',
  `chargesec` int NOT NULL DEFAULT '0',
  `chargest` int NOT NULL DEFAULT '0',
  `paymode` varchar(20) NOT NULL DEFAULT '',
  `payst` int NOT NULL DEFAULT '0',
  `status` int NOT NULL DEFAULT '0',
  `btime1` varchar(20) NOT NULL DEFAULT '',
  `btime2` varchar(20) NOT NULL DEFAULT '',
  `alertst` int NOT NULL DEFAULT '0',
  `duration_seconds` int NOT NULL DEFAULT '0',
  `end_time` datetime DEFAULT NULL,
  `smsst` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_booking_user` (`uname`),
  KEY `fk_booking_station` (`station`),
  CONSTRAINT `fk_booking_station` FOREIGN KEY (`station`) REFERENCES `ev_station` (`uname`) ON DELETE CASCADE,
  CONSTRAINT `fk_booking_user` FOREIGN KEY (`uname`) REFERENCES `ev_register` (`uname`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `ev_booking` DISABLE KEYS */;
INSERT INTO `ev_booking` (`id`, `uname`, `station`, `carno`, `reserve`, `slot`, `cimage`, `mins`, `plan`, `amount`, `rtime`, `etime`, `rdate`, `edate`, `otp`, `charge`, `chargetime`, `chargemin`, `chargesec`, `chargest`, `paymode`, `payst`, `status`, `btime1`, `btime2`, `alertst`, `duration_seconds`, `end_time`, `smsst`) VALUES (3,'navven','vai','tn46','1',3,'evch.jpg',5,3,300.00,'14:25','14:30','2026-04-05','2026-04-05','',0,0,5,0,3,'Cash',1,3,'14:25','14:30',0,300,'2026-04-05 09:00:51',0),(4,'yuva','vai','tn46','1',3,'evch.jpg',5,3,300.00,'20:45','20:50','2026-04-05','2026-04-05','',0,0,5,0,3,'',0,1,'20:45','20:50',0,300,'2026-04-05 09:14:45',0);
/*!40000 ALTER TABLE `ev_booking` ENABLE KEYS */;
DROP TABLE IF EXISTS `ev_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ev_register` (
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
  `amount` double NOT NULL DEFAULT '10000',
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `ev_register` DISABLE KEYS */;
INSERT INTO `ev_register` (`name`, `address`, `mobile`, `email`, `uname`, `passw`, `latitude`, `longitude`, `account`, `card`, `bank`, `amount`) VALUES ('Naveen','Perambalur ',6379241960,'naveenceo86@gmail.com','Naveen@','Naveen@123','','','','','',10000),('navven','siruvachur',5646456411,'naveenarul783@gmail.com','navven','naveen','','','','','',10000),('yuva','perambalur',8610725539,'raj366089@gmail.com','yuva','yuva@','','','','','',10000);
/*!40000 ALTER TABLE `ev_register` ENABLE KEYS */;
DROP TABLE IF EXISTS `ev_station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ev_station` (
  `name` varchar(20) NOT NULL,
  `stype` varchar(20) NOT NULL DEFAULT 'Private',
  `numcharger` int NOT NULL DEFAULT '0',
  `area` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `lat` varchar(20) NOT NULL DEFAULT '',
  `lon` varchar(20) NOT NULL DEFAULT '',
  `uname` varchar(20) NOT NULL,
  `passw` varchar(20) NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  `landmark` varchar(30) NOT NULL DEFAULT '',
  `mobile` bigint NOT NULL,
  `email` varchar(40) NOT NULL DEFAULT '',
  `distance` double NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `last_seen` datetime DEFAULT NULL,
  PRIMARY KEY (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40000 ALTER TABLE `ev_station` DISABLE KEYS */;
INSERT INTO `ev_station` (`name`, `stype`, `numcharger`, `area`, `city`, `lat`, `lon`, `uname`, `passw`, `status`, `landmark`, `mobile`, `email`, `distance`, `is_active`, `last_seen`) VALUES ('Auto_LPG','Private',6,'NH 38','Perambalur','11.201109','78.878258','Auto_LPG_ST','Auto_LPG@',1,'near Sri Ramakrishna College',6398765432,'autolpgstation@gmail.com',0,0,NULL),('HPCL','Private',7,'NH 38, Irungalur','TRICHY','10.95453','78.75907','HPCL_ST','HPCL@',1,'Chennai to Trichy HW',9608754321,'hpclhpcl3452@gmail.com',0,0,NULL),('vai machan','Private',10,'perambalur','Perambalur','21545454','23115454','vai','vai@',1,'yuva house',6379241960,'naveenarul637@gmail.com',0,0,'2026-04-08 04:54:57'),('Zeon','Private',8,'NH 38','Perambalur','11.206906','78.881544','Zeon_ST','Zeon@',1,'Near Aswins Veg Restaurant',9876543210,'zeonstation@gmail.com',0,0,NULL);
/*!40000 ALTER TABLE `ev_station` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

