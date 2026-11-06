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
-- Table structure for table `layout_master_menu_departments`
--

DROP TABLE IF EXISTS `layout_master_menu_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_menu_departments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_menu_depar_menu_id_department_id_73ae3c6d_uniq` (`menu_id`,`department_id`),
  KEY `Layout_Master_menu_d_department_id_0c451713_fk_Accounts_` (`department_id`),
  CONSTRAINT `Layout_Master_menu_d_department_id_0c451713_fk_Accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `Layout_Master_menu_d_menu_id_e340c1dd_fk_Layout_Ma` FOREIGN KEY (`menu_id`) REFERENCES `layout_master_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_menu_departments`
--

LOCK TABLES `layout_master_menu_departments` WRITE;
/*!40000 ALTER TABLE `layout_master_menu_departments` DISABLE KEYS */;
INSERT INTO `layout_master_menu_departments` VALUES (59,1,42),(60,1,43),(61,1,46),(58,1,48),(45,2,42),(56,2,48),(53,3,15),(50,3,42),(54,3,43),(52,3,46),(49,4,42),(57,4,48),(64,7,33),(48,7,42),(55,7,48),(62,9,42),(63,9,48);
/*!40000 ALTER TABLE `layout_master_menu_departments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:18
