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
-- Table structure for table `layout_master_childmenu`
--

DROP TABLE IF EXISTS `layout_master_childmenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layout_master_childmenu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `order` int unsigned NOT NULL,
  `submenu_id` bigint NOT NULL,
  `visibility` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Layout_Master_childm_submenu_id_ef996714_fk_Layout_Ma` (`submenu_id`),
  CONSTRAINT `Layout_Master_childm_submenu_id_ef996714_fk_Layout_Ma` FOREIGN KEY (`submenu_id`) REFERENCES `layout_master_submenu` (`id`),
  CONSTRAINT `layout_master_childmenu_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layout_master_childmenu`
--

LOCK TABLES `layout_master_childmenu` WRITE;
/*!40000 ALTER TABLE `layout_master_childmenu` DISABLE KEYS */;
INSERT INTO `layout_master_childmenu` VALUES (1,'View Tickets','/itdesk/tickets/list','fa fa-eye',0,2,'department'),(2,'Raise Ticket','/itdesk/tickets/raise',NULL,1,2,'department'),(6,'AD Users','/admanager/adusers/','fa fa-users',0,5,'department'),(7,'AD Computers','/admanager/adcomputers/','fa fa-computer',0,5,'department'),(13,'Create','/hrdesk/survey/create/',NULL,0,12,'department'),(15,'View Survey/Pool','/hrdesk/surveys/',NULL,0,12,'department'),(16,'Vendors','/itdesk/vendor/list/',NULL,0,13,'department'),(17,'Invoice','/itdesk/invoice/list/',NULL,0,13,'department'),(18,'Assets','/itdesk/asset/list/',NULL,0,13,'department'),(19,'Add VoIP','/itdesk/add_voip',NULL,0,14,'department'),(20,'List VoIP','/itdesk/list_voip',NULL,0,14,'department'),(23,'Upload Img','/intranet/upload/',NULL,4,26,'department'),(24,'Library','/books/',NULL,0,28,'department'),(25,'Write Book','/books/create/',NULL,0,28,'department'),(26,'Create Post','/hrdesk/jobs/create/',NULL,3,29,'department'),(27,'Show Post','/hrdesk/jobs/',NULL,2,29,'department'),(29,'Create Assessment','/assessment/test/create/',NULL,0,31,'department'),(30,'View Assessment','/assessment/view-assessments/',NULL,2,31,'department'),(31,'Import','/cdr/import/',NULL,0,34,'department'),(32,'Create Post','/IJP/create_ijp/',NULL,0,36,'department'),(33,'Create','/hrdesk/recognition/create/',NULL,0,37,'department'),(34,'View','/hrdesk/recognition_list/',NULL,0,37,'department'),(36,'Postings','/IJP/jobs/',NULL,0,35,'authenticated'),(37,'Results','/IJP/my-applications/',NULL,0,35,'authenticated'),(38,'Desktops','/assets/desktops/',NULL,0,40,'department'),(39,'Monitors','/assets/monitors/',NULL,0,40,'department');
/*!40000 ALTER TABLE `layout_master_childmenu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:11
