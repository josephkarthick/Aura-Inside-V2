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
-- Table structure for table `layout_master_menu_designations`
--

DROP TABLE IF EXISTS `layout_master_menu_designations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_menu_designations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_menu_desig_menu_id_designation_id_a3858663_uniq` (`menu_id`,`designation_id`),
  KEY `Layout_Master_menu_d_designation_id_5698b87d_fk_Accounts_` (`designation_id`),
  CONSTRAINT `Layout_Master_menu_d_designation_id_5698b87d_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`),
  CONSTRAINT `Layout_Master_menu_d_menu_id_02b2c53d_fk_Layout_Ma` FOREIGN KEY (`menu_id`) REFERENCES `layout_master_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_menu_designations`
--

LOCK TABLES `layout_master_menu_designations` WRITE;
/*!40000 ALTER TABLE `layout_master_menu_designations` DISABLE KEYS */;
INSERT INTO `layout_master_menu_designations` VALUES (18,1,2),(16,1,32),(17,1,33),(19,1,50),(20,1,55),(21,1,56),(29,2,32),(30,2,55),(14,2,56),(11,3,2),(7,3,32),(8,3,33),(10,3,55),(27,4,32),(28,4,55),(15,4,56),(32,7,2),(33,7,13),(24,7,32),(31,7,49),(25,7,55),(13,7,56),(22,9,32),(23,9,55),(26,9,56);
/*!40000 ALTER TABLE `layout_master_menu_designations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:12
