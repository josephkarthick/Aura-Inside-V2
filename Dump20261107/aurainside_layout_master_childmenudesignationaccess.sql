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
-- Table structure for table `layout_master_childmenudesignationaccess`
--

DROP TABLE IF EXISTS `layout_master_childmenudesignationaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_childmenudesignationaccess` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `childmenu_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_childmenu_dept_designation_access` (`childmenu_id`,`department_id`,`designation_id`),
  KEY `Layout_Master_childm_department_id_017ced14_fk_Accounts_` (`department_id`),
  KEY `Layout_Master_childm_designation_id_fd676669_fk_Accounts_` (`designation_id`),
  CONSTRAINT `Layout_Master_childm_childmenu_id_2fadfcec_fk_Layout_Ma` FOREIGN KEY (`childmenu_id`) REFERENCES `layout_master_childmenu` (`id`),
  CONSTRAINT `Layout_Master_childm_department_id_017ced14_fk_Accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `Layout_Master_childm_designation_id_fd676669_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_childmenudesignationaccess`
--

LOCK TABLES `layout_master_childmenudesignationaccess` WRITE;
/*!40000 ALTER TABLE `layout_master_childmenudesignationaccess` DISABLE KEYS */;
INSERT INTO `layout_master_childmenudesignationaccess` VALUES (57,1,42,32),(58,1,42,55),(56,1,48,56),(60,2,42,32),(61,2,42,55),(59,2,48,56),(51,6,42,32),(52,6,42,55),(50,6,48,56),(54,7,42,32),(55,7,42,55),(53,7,48,56),(6,15,48,56),(63,16,42,32),(64,16,42,55),(62,16,48,56),(66,17,42,32),(67,17,42,55),(65,17,48,56),(69,18,42,32),(70,18,42,55),(68,18,48,56),(72,19,42,32),(73,19,42,55),(71,19,48,56),(75,20,42,32),(76,20,42,55),(74,20,48,56),(25,23,42,32),(26,23,42,55),(27,23,43,50),(23,23,46,2),(24,23,46,33),(22,23,48,56),(31,24,42,32),(32,24,42,55),(33,24,43,50),(29,24,46,2),(30,24,46,33),(28,24,48,56),(37,25,42,32),(38,25,42,55),(39,25,43,50),(35,25,46,2),(36,25,46,33),(34,25,48,56),(7,27,48,56),(8,30,48,56),(78,31,42,32),(79,31,42,55),(77,31,48,56),(9,32,48,56),(10,34,48,56),(45,38,42,32),(46,38,42,55),(44,38,48,56),(48,39,42,32),(49,39,42,55),(47,39,48,56);
/*!40000 ALTER TABLE `layout_master_childmenudesignationaccess` ENABLE KEYS */;
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
