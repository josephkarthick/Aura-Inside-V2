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
-- Table structure for table `layout_master_childmenu_designations`
--

DROP TABLE IF EXISTS `layout_master_childmenu_designations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_childmenu_designations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `childmenu_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_childmenu__childmenu_id_designation_d5f46b80_uniq` (`childmenu_id`,`designation_id`),
  KEY `Layout_Master_childm_designation_id_d19ae60e_fk_Accounts_` (`designation_id`),
  CONSTRAINT `Layout_Master_childm_childmenu_id_8bdf98d2_fk_Layout_Ma` FOREIGN KEY (`childmenu_id`) REFERENCES `layout_master_childmenu` (`id`),
  CONSTRAINT `Layout_Master_childm_designation_id_d19ae60e_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_childmenu_designations`
--

LOCK TABLES `layout_master_childmenu_designations` WRITE;
/*!40000 ALTER TABLE `layout_master_childmenu_designations` DISABLE KEYS */;
INSERT INTO `layout_master_childmenu_designations` VALUES (62,1,32),(64,1,55),(60,1,56),(90,2,32),(92,2,55),(91,2,56),(86,6,32),(87,6,55),(65,6,56),(88,7,32),(89,7,55),(66,7,56),(41,13,2),(5,13,32),(6,13,33),(8,13,55),(55,15,56),(93,16,32),(95,16,55),(94,16,56),(96,17,32),(98,17,55),(97,17,56),(99,18,32),(101,18,55),(100,18,56),(102,19,32),(104,19,55),(103,19,56),(105,20,32),(106,20,55),(61,20,56),(52,23,2),(50,23,32),(51,23,33),(53,23,50),(54,23,55),(67,23,56),(70,24,2),(68,24,32),(69,24,33),(71,24,50),(72,24,55),(73,24,56),(76,25,2),(74,25,32),(75,25,33),(77,25,50),(78,25,55),(79,25,56),(43,26,2),(13,26,32),(14,26,33),(16,26,55),(56,27,56),(45,29,2),(21,29,32),(22,29,33),(24,29,55),(57,30,56),(107,31,32),(109,31,55),(108,31,56),(58,32,56),(48,33,2),(33,33,32),(34,33,33),(36,33,55),(59,34,56),(80,38,32),(81,38,55),(84,38,56),(82,39,32),(83,39,55),(85,39,56);
/*!40000 ALTER TABLE `layout_master_childmenu_designations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:16
