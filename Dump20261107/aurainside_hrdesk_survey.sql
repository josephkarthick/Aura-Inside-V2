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
-- Table structure for table `hrdesk_survey`
--

DROP TABLE IF EXISTS `hrdesk_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hrdesk_survey` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HRDesk_survey_created_by_id_26c7ec30_fk_Accounts_` (`created_by_id`),
  CONSTRAINT `HRDesk_survey_created_by_id_26c7ec30_fk_Accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_aurainsideuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrdesk_survey`
--

LOCK TABLES `hrdesk_survey` WRITE;
/*!40000 ALTER TABLE `hrdesk_survey` DISABLE KEYS */;
INSERT INTO `hrdesk_survey` VALUES (36,'Monthly Lunch','We’re planning the employee lunch on 4th February\r\nPlease let us know if your preference is Veg or Non-Veg to help us plan better','2026-01-29 11:11:00.000000','2026-02-03 14:00:00.000000','2026-01-29 11:13:11.335802',NULL),(44,'Fun at Work – Let the Games Begin! ','As part of our employee engagement initiative, we are planning to conduct an Indoor Games Tournament featuring Carrom, Chess, and Shuttle for all interested employees.','2026-02-14 14:15:00.000000','2026-02-21 19:30:00.000000','2026-02-14 14:13:51.914454',240),(45,'Basic Information','Kindly fill the basic details mentioned below for new ID card','2026-03-10 10:38:00.000000','2026-03-11 03:00:00.000000','2026-03-10 10:42:57.073059',NULL),(47,'Lunch/Dinner Preference – July 15, 2026','On July 15, 2026, Aura will be providing Lunch/Dinner.','2026-07-10 01:10:00.000000','2026-07-14 01:10:00.000000','2026-07-10 01:09:48.045563',NULL),(48,' Prefered timings for lunch','','2026-08-01 13:00:00.000000','2026-08-01 17:00:00.000000','2026-08-01 13:10:58.943695',240);
/*!40000 ALTER TABLE `hrdesk_survey` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:17
