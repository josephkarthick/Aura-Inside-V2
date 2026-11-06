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
-- Table structure for table `layout_master_childmenu_departments`
--

DROP TABLE IF EXISTS `layout_master_childmenu_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_childmenu_departments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `childmenu_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Layout_Master_childmenu__childmenu_id_department__1d63ae3a_uniq` (`childmenu_id`,`department_id`),
  KEY `Layout_Master_childm_department_id_ff373e27_fk_Accounts_` (`department_id`),
  CONSTRAINT `Layout_Master_childm_childmenu_id_a86a0f3d_fk_Layout_Ma` FOREIGN KEY (`childmenu_id`) REFERENCES `layout_master_childmenu` (`id`),
  CONSTRAINT `Layout_Master_childm_department_id_ff373e27_fk_Accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_childmenu_departments`
--

LOCK TABLES `layout_master_childmenu_departments` WRITE;
/*!40000 ALTER TABLE `layout_master_childmenu_departments` DISABLE KEYS */;
INSERT INTO `layout_master_childmenu_departments` VALUES (95,1,42),(120,1,48),(96,2,42),(138,2,48),(57,6,42),(123,6,48),(58,7,42),(124,7,48),(62,13,15),(59,13,42),(103,13,43),(61,13,46),(66,15,15),(63,15,42),(104,15,43),(65,15,46),(115,15,48),(97,16,42),(139,16,48),(98,17,42),(140,17,48),(99,18,42),(141,18,48),(100,19,42),(142,19,48),(101,20,42),(121,20,48),(112,23,42),(113,23,43),(114,23,46),(125,23,48),(127,24,42),(128,24,43),(129,24,46),(126,24,48),(131,25,42),(132,25,43),(133,25,46),(130,25,48),(70,26,15),(67,26,42),(105,26,43),(69,26,46),(74,27,15),(71,27,42),(106,27,43),(73,27,46),(116,27,48),(78,29,15),(75,29,42),(107,29,43),(77,29,46),(82,30,15),(79,30,42),(108,30,43),(81,30,46),(117,30,48),(102,31,42),(143,31,48),(86,32,15),(83,32,42),(109,32,43),(85,32,46),(118,32,48),(90,33,15),(87,33,42),(110,33,43),(89,33,46),(94,34,15),(91,34,42),(111,34,43),(93,34,46),(119,34,48),(134,38,42),(136,38,48),(135,39,42),(137,39,48);
/*!40000 ALTER TABLE `layout_master_childmenu_departments` ENABLE KEYS */;
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
