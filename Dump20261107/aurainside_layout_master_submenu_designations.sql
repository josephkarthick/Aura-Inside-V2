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
-- Table structure for table `layout_master_submenu_designations`
--

DROP TABLE IF EXISTS `layout_master_submenu_designations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_submenu_designations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `submenu_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_submenu_de_submenu_id_designation_i_05769482_uniq` (`submenu_id`,`designation_id`),
  KEY `Layout_Master_submen_designation_id_1be1406d_fk_Accounts_` (`designation_id`),
  CONSTRAINT `Layout_Master_submen_designation_id_1be1406d_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`),
  CONSTRAINT `Layout_Master_submen_submenu_id_8c25b4eb_fk_Layout_Ma` FOREIGN KEY (`submenu_id`) REFERENCES `layout_master_submenu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_submenu_designations`
--

LOCK TABLES `layout_master_submenu_designations` WRITE;
/*!40000 ALTER TABLE `layout_master_submenu_designations` DISABLE KEYS */;
INSERT INTO `layout_master_submenu_designations` VALUES (25,1,2),(23,1,32),(24,1,33),(144,1,50),(27,1,55),(143,1,56),(134,2,32),(136,2,55),(132,2,56),(159,5,32),(160,5,55),(142,5,56),(30,6,2),(28,6,32),(29,6,33),(146,6,50),(32,6,55),(145,6,56),(127,12,56),(161,13,32),(163,13,55),(162,13,56),(164,14,32),(165,14,55),(133,14,56),(156,20,32),(157,20,55),(123,20,56),(35,26,2),(33,26,32),(34,26,33),(120,26,50),(37,26,55),(147,26,56),(150,27,2),(38,27,32),(149,27,33),(151,27,50),(41,27,55),(148,27,56),(44,28,2),(42,28,32),(43,28,33),(153,28,50),(46,28,55),(152,28,56),(128,29,56),(129,31,56),(170,33,2),(171,33,13),(9,33,32),(169,33,49),(15,33,55),(124,33,56),(166,34,32),(168,34,55),(167,34,56),(130,36,56),(131,37,56),(16,38,32),(22,38,55),(125,38,56),(79,39,32),(80,39,55),(126,39,56),(154,40,32),(155,40,55),(158,40,56),(139,42,2),(137,42,32),(138,42,33),(140,42,50),(141,42,55);
/*!40000 ALTER TABLE `layout_master_submenu_designations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:15
