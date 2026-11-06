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
-- Table structure for table `hrdesk_option`
--

DROP TABLE IF EXISTS `hrdesk_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hrdesk_option` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` varchar(255) NOT NULL,
  `question_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HRDesk_option_question_id_2d485dc6_fk_HRDesk_question_id` (`question_id`),
  CONSTRAINT `HRDesk_option_question_id_2d485dc6_fk_HRDesk_question_id` FOREIGN KEY (`question_id`) REFERENCES `hrdesk_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrdesk_option`
--

LOCK TABLES `hrdesk_option` WRITE;
/*!40000 ALTER TABLE `hrdesk_option` DISABLE KEYS */;
INSERT INTO `hrdesk_option` VALUES (154,'Veg',35),(155,'Non Veg',35),(180,'Yes',47),(181,'No',47),(182,'Yes',48),(183,'No',48),(184,'Yes ',49),(185,'No',49),(186,'Yes',50),(187,'No',50),(188,'A+',54),(189,'A-',54),(190,'B+',54),(191,'B-',54),(192,'AB+',54),(193,'AB-',54),(194,'O+',54),(195,'O-',54),(196,'? Veg',55),(197,'? Non-Veg',55),(198,'12:30 PM to 1:00 PM',56),(199,'1.00 PM to 1:30 PM',56),(200,'1:30 PM to 2:00 PM',56),(201,'Lunch - Outside Office',56);
/*!40000 ALTER TABLE `hrdesk_option` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:13
