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
-- Table structure for table `hrdesk_question`
--

DROP TABLE IF EXISTS `hrdesk_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hrdesk_question` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` varchar(500) NOT NULL,
  `question_type` varchar(20) NOT NULL,
  `survey_id` bigint NOT NULL,
  `allow_file_upload` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HRDesk_question_survey_id_d6a8aa16_fk_HRDesk_survey_id` (`survey_id`),
  CONSTRAINT `HRDesk_question_survey_id_d6a8aa16_fk_HRDesk_survey_id` FOREIGN KEY (`survey_id`) REFERENCES `hrdesk_survey` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrdesk_question`
--

LOCK TABLES `hrdesk_question` WRITE;
/*!40000 ALTER TABLE `hrdesk_question` DISABLE KEYS */;
INSERT INTO `hrdesk_question` VALUES (35,'Please let us know if your preference is Veg or Non-Veg ','radio',36,0),(47,'Are you interested in participating in the Carrom tournament?','radio',44,0),(48,'Are you interested in participating in the Chess tournament?','radio',44,0),(49,'Are you interested in participating in the Badminton tournament?','radio',44,0),(50,'Are you interested in participating in the Cooking competition?','radio',44,0),(51,'Employee Name ','text',45,0),(52,'Emergency Contact Person Name ','text',45,0),(53,'Emergency Contact Number','text',45,0),(54,'Blood Group','checkbox',45,0),(55,'Please let us know your preferred meal option by selecting one of the following:','radio',47,0),(56,'Whats your prefered timings for lunch?','radio',48,0);
/*!40000 ALTER TABLE `hrdesk_question` ENABLE KEYS */;
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
