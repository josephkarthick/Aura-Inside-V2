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
-- Table structure for table `layout_master_submenu_users`
--

DROP TABLE IF EXISTS `layout_master_submenu_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_submenu_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `submenu_id` bigint NOT NULL,
  `aurainsideuser_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_submenu_us_submenu_id_aurainsideuse_36dce904_uniq` (`submenu_id`,`aurainsideuser_id`),
  KEY `Layout_Master_submen_aurainsideuser_id_a89ae110_fk_Accounts_` (`aurainsideuser_id`),
  CONSTRAINT `Layout_Master_submen_aurainsideuser_id_a89ae110_fk_Accounts_` FOREIGN KEY (`aurainsideuser_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `Layout_Master_submen_submenu_id_45f054f3_fk_Layout_Ma` FOREIGN KEY (`submenu_id`) REFERENCES `layout_master_submenu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_submenu_users`
--

LOCK TABLES `layout_master_submenu_users` WRITE;
/*!40000 ALTER TABLE `layout_master_submenu_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `layout_master_submenu_users` ENABLE KEYS */;
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
