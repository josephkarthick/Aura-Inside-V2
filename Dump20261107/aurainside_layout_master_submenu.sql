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
-- Table structure for table `layout_master_submenu`
--

DROP TABLE IF EXISTS `layout_master_submenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_submenu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `order` int unsigned NOT NULL,
  `menu_id` bigint NOT NULL,
  `visibility` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Layout_Master_submenu_menu_id_5b975c21_fk_Layout_Master_menu_id` (`menu_id`),
  CONSTRAINT `Layout_Master_submenu_menu_id_5b975c21_fk_Layout_Master_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `layout_master_menu` (`id`),
  CONSTRAINT `layout_master_submenu_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_submenu`
--

LOCK TABLES `layout_master_submenu` WRITE;
/*!40000 ALTER TABLE `layout_master_submenu` DISABLE KEYS */;
INSERT INTO `layout_master_submenu` VALUES (1,'Organization Structure','fa fa-chart','/intranet/admin_org_chart/',0,1,'department'),(2,'Tickets','fa fa-ticket','',0,2,'department'),(5,'Active Directory','fa fa-computer',NULL,0,4,'department'),(6,'Home Page Content',NULL,'/intranet/admin_list_content/',0,1,'department'),(7,'Start Voice',NULL,'/auravoice/',0,5,'department'),(12,'Survey/Poll',NULL,NULL,0,3,'department'),(13,'Asset',NULL,NULL,0,2,'department'),(14,'VoIP',NULL,NULL,4,2,'department'),(18,'My Profile',NULL,'/employee/userprofile/',0,6,'authenticated'),(19,'Calendar',NULL,'/employee/calendar/',0,6,'authenticated'),(20,'IT Dashboard',NULL,'/dashboard/it-dashboard/',0,7,'department'),(21,'Add Password',NULL,'/vault/add/',0,8,'authenticated'),(22,'List Password',NULL,'/vault/list/',0,8,'authenticated'),(26,'Gallery',NULL,NULL,5,1,'department'),(27,'Flag',NULL,'/floating-flag/',7,1,'department'),(28,'Aura Books',NULL,NULL,0,1,'department'),(29,'Careers',NULL,NULL,0,3,'department'),(31,'Assessment',NULL,NULL,4,3,'department'),(32,'Assessment',NULL,'/assessment/qst-paper/',3,6,'authenticated'),(33,'CDR Dashboard',NULL,'/cdr/cdr-dashboard/',0,7,'department'),(34,'CDR',NULL,NULL,0,2,'department'),(35,'Internal Job post',NULL,NULL,5,6,'authenticated'),(36,'IJP',NULL,NULL,0,3,'department'),(37,'Poster',NULL,NULL,0,3,'department'),(38,'IJP Dashboard',NULL,'/IJP/admin/ijps/',0,7,'department'),(39,'Idle Eye Dashboard',NULL,'http://192.168.5.249:8000/',0,7,'department'),(40,'IT Assets',NULL,NULL,0,9,'department'),(41,'List Books',NULL,'/books',0,10,'public'),(42,'Create Books',NULL,'/books/create',0,10,'department');
/*!40000 ALTER TABLE `layout_master_submenu` ENABLE KEYS */;
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
