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
-- Table structure for table `assessment_testpaper`
--

DROP TABLE IF EXISTS `assessment_testpaper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_testpaper` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext,
  `duration_minutes` int unsigned NOT NULL,
  `passing_marks` int unsigned NOT NULL,
  `shuffle_questions` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `end_datetime` datetime(6) DEFAULT NULL,
  `max_attempts` int unsigned NOT NULL,
  `start_datetime` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Assessment_testpaper_created_by_id_31525e25_fk_Accounts_` (`created_by_id`),
  CONSTRAINT `Assessment_testpaper_created_by_id_31525e25_fk_Accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `assessment_testpaper_chk_1` CHECK ((`duration_minutes` >= 0)),
  CONSTRAINT `assessment_testpaper_chk_2` CHECK ((`passing_marks` >= 0)),
  CONSTRAINT `assessment_testpaper_chk_3` CHECK ((`max_attempts` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_testpaper`
--

LOCK TABLES `assessment_testpaper` WRITE;
/*!40000 ALTER TABLE `assessment_testpaper` DISABLE KEYS */;
INSERT INTO `assessment_testpaper` VALUES (4,'Test','Humphres',30,60,1,1,'2026-06-13 00:28:27.589868',NULL,NULL,1,NULL),(5,'IT Test','Testing Page',30,60,1,1,'2026-06-13 01:01:36.057035',NULL,NULL,1,NULL),(6,'IT Test','This to check your skills',1,10,1,1,'2026-06-13 01:25:16.869889',NULL,NULL,1,NULL),(7,'IT Paper','Test',30,60,1,1,'2026-06-13 01:55:51.431167',NULL,NULL,1,NULL),(8,'IT Test','IT Test paper for testing',1,35,1,1,'2026-06-13 02:54:58.964760',NULL,NULL,1,NULL),(9,'Cyber Security Awareness 2026','This assessment evaluates employees\' understanding of basic cyber security practices, phishing awareness, password security, and safe internet usage.',1,60,1,1,'2026-06-16 02:18:03.483977',NULL,'2026-06-16 02:20:00.000000',1,'2026-06-16 02:18:00.000000'),(10,'AR General','AR General',15,2,1,1,'2026-07-01 15:24:57.344147',NULL,'2026-07-03 17:30:00.000000',1,'2026-07-02 14:00:00.000000');
/*!40000 ALTER TABLE `assessment_testpaper` ENABLE KEYS */;
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
