-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: aurainside
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `intranet_home`
--

DROP TABLE IF EXISTS `intranet_home`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intranet_home` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` longtext,
  `photo` varchar(100) DEFAULT NULL,
  `field1` varchar(100) DEFAULT NULL,
  `field2` varchar(100) DEFAULT NULL,
  `photo_layout` varchar(1) DEFAULT NULL,
  `project` varchar(255) DEFAULT NULL,
  `username_id` bigint DEFAULT NULL,
  `order_no` int unsigned DEFAULT NULL,
  `show` tinyint(1) DEFAULT NULL,
  `content_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Intranet_home_username_id_9f72f7b3_fk_Accounts_aurainsideuser_id` (`username_id`),
  CONSTRAINT `Intranet_home_username_id_9f72f7b3_fk_Accounts_aurainsideuser_id` FOREIGN KEY (`username_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `intranet_home_chk_1` CHECK ((`order_no` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intranet_home`
--

LOCK TABLES `intranet_home` WRITE;
/*!40000 ALTER TABLE `intranet_home` DISABLE KEYS */;
INSERT INTO `intranet_home` VALUES (20,'Upcoming Trip','A fun-filled one-day outing is being planned for Jan 4th, 2026.\r\nWill you join the outing?\r\n\r\nhttp://192.168.5.249/hrdesk/survey/31/take/','home_banners/trip.jpeg',NULL,NULL,'1','',NULL,1,0,'news'),(21,'T-Shirt Size Collection Form','Please select your T-shirt size : http://192.168.5.249/hrdesk/survey/33/take/','home_banners/Tshirt.png',NULL,NULL,'1','',NULL,2,0,'announcement'),(24,'Transport Availability Survey ','Please select your preferred pickup point\r\nhttp://192.168.5.249/hrdesk/survey/35/take/','home_banners/Inked39249_LI_jqamwDd.jpg',NULL,NULL,'1','',NULL,1,0,'news'),(51,'POTLUCK','\r\n1	ARN 	2/11/2026\r\n2	Humphreys Peak - RVS / Charges Team	2/12/2026\r\n3	Humphreys Peak - Copay / Payment Posting Team	2/13/2026\r\n4	Mount Rainier / Wichita / Delray / Mount Diablo	2/14/2026\r\n5	Mount Sunflower	2/17/2026\r\n6	Humphreys Peak ( Analyst Team )	2/18/2026\r\n','home_banners/1697791371163.jfif',NULL,NULL,'1','',NULL,1,0,'event'),(55,'Indoor Tournament Interest Survey','http://192.168.5.249/hrdesk/survey/44/take/','home_banners/group-app-games.jpg',NULL,NULL,'1','',NULL,2,0,'event'),(56,'Basic Information','Kindly fill the data for ID card\r\nhttp://192.168.5.249/hrdesk/survey/45/take/','',NULL,NULL,'1','',NULL,1,0,'news'),(58,'Lunch/Dinner Preference – July 15, 2026','Please let us know your preferred meal option (Veg or Non-Veg) by submitting your choice using the link below:\r\n\r\nhttp://192.168.5.249/hrdesk/survey/47/take/','home_banners/local-style-non-veg-dishes-nati-style-nonveg-dishes-plate-photo_c1teuqh.jpg',NULL,NULL,'1','',NULL,1,0,'announcement'),(59,'Lunch Timings - Survey','http://192.168.5.249/hrdesk/survey/48/take/','',NULL,NULL,'1','',NULL,0,0,'announcement');
/*!40000 ALTER TABLE `intranet_home` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:14
