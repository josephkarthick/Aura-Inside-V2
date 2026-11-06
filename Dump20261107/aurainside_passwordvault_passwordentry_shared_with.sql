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
-- Table structure for table `passwordvault_passwordentry_shared_with`
--

DROP TABLE IF EXISTS `passwordvault_passwordentry_shared_with`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passwordvault_passwordentry_shared_with` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `passwordentry_id` bigint NOT NULL,
  `aurainsideuser_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `PasswordVault_passworden_passwordentry_id_aurains_2ad887a4_uniq` (`passwordentry_id`,`aurainsideuser_id`),
  KEY `PasswordVault_passwo_aurainsideuser_id_606dfac7_fk_Accounts_` (`aurainsideuser_id`),
  CONSTRAINT `PasswordVault_passwo_aurainsideuser_id_606dfac7_fk_Accounts_` FOREIGN KEY (`aurainsideuser_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `PasswordVault_passwo_passwordentry_id_9f0aaaed_fk_PasswordV` FOREIGN KEY (`passwordentry_id`) REFERENCES `passwordvault_passwordentry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passwordvault_passwordentry_shared_with`
--

LOCK TABLES `passwordvault_passwordentry_shared_with` WRITE;
/*!40000 ALTER TABLE `passwordvault_passwordentry_shared_with` DISABLE KEYS */;
/*!40000 ALTER TABLE `passwordvault_passwordentry_shared_with` ENABLE KEYS */;
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
