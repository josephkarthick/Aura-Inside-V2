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
-- Table structure for table `layout_master_submenudesignationaccess`
--

DROP TABLE IF EXISTS `layout_master_submenudesignationaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_submenudesignationaccess` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  `submenu_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_submenu_dept_designation_access` (`submenu_id`,`department_id`,`designation_id`),
  KEY `Layout_Master_submen_department_id_594b72ca_fk_Accounts_` (`department_id`),
  KEY `Layout_Master_submen_designation_id_f8c79b7e_fk_Accounts_` (`designation_id`),
  CONSTRAINT `Layout_Master_submen_department_id_594b72ca_fk_Accounts_` FOREIGN KEY (`department_id`) REFERENCES `accounts_department` (`id`),
  CONSTRAINT `Layout_Master_submen_designation_id_f8c79b7e_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`),
  CONSTRAINT `Layout_Master_submen_submenu_id_016fe9cf_fk_Layout_Ma` FOREIGN KEY (`submenu_id`) REFERENCES `layout_master_submenu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_submenudesignationaccess`
--

LOCK TABLES `layout_master_submenudesignationaccess` WRITE;
/*!40000 ALTER TABLE `layout_master_submenudesignationaccess` DISABLE KEYS */;
INSERT INTO `layout_master_submenudesignationaccess` VALUES (115,42,32,1),(116,42,55,1),(117,43,50,1),(113,46,2,1),(114,46,33,1),(112,48,56,1),(163,42,32,2),(164,42,55,2),(162,48,56,2),(160,42,32,5),(161,42,55,5),(159,48,56,5),(121,42,32,6),(122,42,55,6),(123,43,50,6),(119,46,2,6),(120,46,33,6),(118,48,56,6),(88,48,56,12),(166,42,32,13),(167,42,55,13),(165,48,56,13),(169,42,32,14),(170,42,55,14),(168,48,56,14),(145,42,32,20),(146,42,55,20),(144,48,56,20),(127,42,32,26),(128,42,55,26),(129,43,50,26),(125,46,2,26),(126,46,33,26),(124,48,56,26),(133,42,32,27),(134,42,55,27),(135,43,50,27),(131,46,2,27),(132,46,33,27),(130,48,56,27),(139,42,32,28),(140,42,55,28),(141,43,50,28),(137,46,2,28),(138,46,33,28),(136,48,56,28),(89,48,56,29),(90,48,56,31),(177,33,2,33),(178,33,13,33),(179,33,49,33),(175,42,32,33),(176,42,55,33),(174,48,56,33),(172,42,32,34),(173,42,55,34),(171,48,56,34),(91,48,56,36),(92,48,56,37),(151,42,32,38),(152,42,55,38),(150,48,56,38),(154,42,32,39),(155,42,55,39),(153,48,56,39),(157,42,32,40),(158,42,55,40),(156,48,56,40),(109,15,33,42),(107,42,32,42),(108,42,55,42),(110,43,50,42),(105,46,2,42),(106,46,33,42);
/*!40000 ALTER TABLE `layout_master_submenudesignationaccess` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:14
