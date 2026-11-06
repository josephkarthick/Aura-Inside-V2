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
-- Table structure for table `layout_master_submenu_departments`
--

DROP TABLE IF EXISTS `layout_master_submenu_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_submenu_departments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `submenu_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_submenu_de_submenu_id_department_id_04aa238e_uniq` (`submenu_id`,`department_id`),
  KEY `Layout_Master_submen_department_id_53c9f529_fk_Accounts_` (`department_id`),
  CONSTRAINT `Layout_Master_submen_department_id_53c9f529_fk_Accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `Layout_Master_submen_submenu_id_c5bee75d_fk_Layout_Ma` FOREIGN KEY (`submenu_id`) REFERENCES `layout_master_submenu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_submenu_departments`
--

LOCK TABLES `layout_master_submenu_departments` WRITE;
/*!40000 ALTER TABLE `layout_master_submenu_departments` DISABLE KEYS */;
INSERT INTO `layout_master_submenu_departments` VALUES (80,1,42),(185,1,43),(82,1,46),(184,1,48),(115,2,42),(176,2,48),(98,5,42),(183,5,48),(83,6,42),(187,6,43),(85,6,46),(186,6,48),(99,12,15),(95,12,42),(122,12,43),(97,12,46),(171,12,48),(116,13,42),(196,13,48),(117,14,42),(177,14,48),(72,20,42),(167,20,48),(86,26,42),(165,26,43),(88,26,46),(188,26,48),(90,27,42),(190,27,43),(191,27,46),(189,27,48),(92,28,42),(193,28,43),(94,28,46),(192,28,48),(103,29,15),(100,29,42),(123,29,43),(102,29,46),(172,29,48),(107,31,15),(104,31,42),(124,31,43),(106,31,46),(173,31,48),(198,33,33),(74,33,42),(168,33,48),(118,34,42),(197,34,48),(52,36,15),(108,36,42),(125,36,43),(110,36,46),(174,36,48),(114,37,15),(111,37,42),(126,37,43),(113,37,46),(175,37,48),(77,38,42),(169,38,48),(71,39,42),(170,39,48),(194,40,42),(195,40,48),(182,42,15),(179,42,42),(180,42,43),(181,42,46);
/*!40000 ALTER TABLE `layout_master_submenu_departments` ENABLE KEYS */;
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
