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
-- Table structure for table `assets_assetassignment`
--

DROP TABLE IF EXISTS `assets_assetassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assets_assetassignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `assigned_date` date NOT NULL,
  `returned_date` date DEFAULT NULL,
  `remarks` longtext,
  `created_at` datetime(6) NOT NULL,
  `asset_id` bigint NOT NULL,
  `assigned_by_id` bigint DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Assets_assetassignment_asset_id_877378f5_fk_Assets_asset_id` (`asset_id`),
  KEY `Assets_assetassignme_assigned_by_id_e339ca9e_fk_Accounts_` (`assigned_by_id`),
  KEY `Assets_assetassignme_employee_id_1f3cb34d_fk_Accounts_` (`employee_id`),
  CONSTRAINT `Assets_assetassignme_assigned_by_id_e339ca9e_fk_Accounts_` FOREIGN KEY (`assigned_by_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `Assets_assetassignme_employee_id_1f3cb34d_fk_Accounts_` FOREIGN KEY (`employee_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `Assets_assetassignment_asset_id_877378f5_fk_Assets_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `assets_asset` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_assetassignment`
--

LOCK TABLES `assets_assetassignment` WRITE;
/*!40000 ALTER TABLE `assets_assetassignment` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_assetassignment` ENABLE KEYS */;
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
