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
-- Table structure for table `hrdesk_recognitionposter_employees`
--

DROP TABLE IF EXISTS `hrdesk_recognitionposter_employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hrdesk_recognitionposter_employees` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recognitionposter_id` bigint NOT NULL,
  `aurainsideuser_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HRDesk_recognitionposter_recognitionposter_id_aur_ce09d2eb_uniq` (`recognitionposter_id`,`aurainsideuser_id`),
  KEY `HRDesk_recognitionpo_aurainsideuser_id_8b45f656_fk_Accounts_` (`aurainsideuser_id`),
  CONSTRAINT `HRDesk_recognitionpo_aurainsideuser_id_8b45f656_fk_Accounts_` FOREIGN KEY (`aurainsideuser_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `HRDesk_recognitionpo_recognitionposter_id_a411cc33_fk_HRDesk_re` FOREIGN KEY (`recognitionposter_id`) REFERENCES `hrdesk_recognitionposter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrdesk_recognitionposter_employees`
--

LOCK TABLES `hrdesk_recognitionposter_employees` WRITE;
/*!40000 ALTER TABLE `hrdesk_recognitionposter_employees` DISABLE KEYS */;
INSERT INTO `hrdesk_recognitionposter_employees` VALUES (70,1,10),(78,1,159),(75,1,187),(77,1,317),(71,1,335),(46,3,284),(49,3,292),(58,3,333),(80,3,392);
/*!40000 ALTER TABLE `hrdesk_recognitionposter_employees` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:11
