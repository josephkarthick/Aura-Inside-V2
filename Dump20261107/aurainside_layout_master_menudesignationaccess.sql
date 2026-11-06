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
-- Table structure for table `layout_master_menudesignationaccess`
--

DROP TABLE IF EXISTS `layout_master_menudesignationaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_menudesignationaccess` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  `menu_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_menu_dept_designation_access` (`menu_id`,`department_id`,`designation_id`),
  KEY `Layout_Master_menude_department_id_e74b9a11_fk_Accounts_` (`department_id`),
  KEY `Layout_Master_menude_designation_id_dee0f7a3_fk_Accounts_` (`designation_id`),
  CONSTRAINT `Layout_Master_menude_department_id_e74b9a11_fk_Accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `Layout_Master_menude_designation_id_dee0f7a3_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`),
  CONSTRAINT `Layout_Master_menude_menu_id_6499c06c_fk_Layout_Ma` FOREIGN KEY (`menu_id`) REFERENCES `layout_master_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_menudesignationaccess`
--

LOCK TABLES `layout_master_menudesignationaccess` WRITE;
/*!40000 ALTER TABLE `layout_master_menudesignationaccess` DISABLE KEYS */;
INSERT INTO `layout_master_menudesignationaccess` VALUES (8,42,32,1),(9,42,55,1),(10,43,50,1),(6,46,2,1),(7,46,33,1),(5,48,56,1),(23,42,32,2),(24,42,55,2),(22,48,56,2),(20,42,32,4),(21,42,55,4),(19,48,56,4),(28,33,2,7),(29,33,13,7),(30,33,49,7),(26,42,32,7),(27,42,55,7),(25,48,56,7),(17,42,32,9),(18,42,55,9),(16,48,56,9);
/*!40000 ALTER TABLE `layout_master_menudesignationaccess` ENABLE KEYS */;
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
