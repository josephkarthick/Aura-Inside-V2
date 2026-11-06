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
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'Accounts','aurainsideuser'),(6,'Accounts','department'),(7,'Accounts','designation'),(59,'Accounts','employeeappraisal'),(60,'Accounts','employeeattendance'),(65,'Accounts','securitygroup'),(9,'Accounts','shift'),(1,'admin','logentry'),(54,'Assessment','testoption'),(55,'Assessment','testpaper'),(56,'Assessment','testpapergroup'),(53,'Assessment','testquestion'),(58,'Assessment','useranswer'),(57,'Assessment','usertestattempt'),(78,'Assets','asset'),(79,'Assets','assetassignment'),(77,'Assets','assetcategory'),(81,'Assets','computeruserhistory'),(76,'Assets','desktopasset'),(80,'Assets','monitor'),(44,'aura_books','book'),(45,'aura_books','bookpage'),(25,'auravoice','voiceschedule'),(24,'auravoice','voicetask'),(3,'auth','group'),(2,'auth','permission'),(62,'CDR','calllog'),(63,'CDR','vendor'),(4,'contenttypes','contenttype'),(40,'Dashboard','dashboard'),(39,'Dashboard','dashboardwidget'),(38,'Employee','calendar_event'),(83,'Floating_Flag','floatingflag'),(82,'Floating_Flag','floatingflagdismissal'),(28,'HRDesk','answer'),(50,'HRDesk','jobapplication'),(51,'HRDesk','jobposting'),(30,'HRDesk','option'),(26,'HRDesk','question'),(66,'HRDesk','recognitionposter'),(27,'HRDesk','response'),(29,'HRDesk','survey'),(23,'HRDesk','systemevent'),(64,'IJP','ijpapplication'),(61,'IJP','internaljobposting'),(49,'interactions','comment'),(48,'interactions','reaction'),(13,'Intranet','boardmembers'),(43,'Intranet','floatingflag'),(32,'Intranet','gallery'),(31,'Intranet','gallerygroup'),(14,'Intranet','home'),(52,'Intranet','quote'),(35,'ITDesk','asset'),(33,'ITDesk','assetcategory'),(70,'ITDesk','incidentregister'),(71,'ITDesk','incidentstatushistory'),(36,'ITDesk','invoice'),(22,'ITDesk','itasset'),(68,'ITDesk','monitor'),(16,'ITDesk','new_tkt'),(19,'ITDesk','priority_choice'),(21,'ITDesk','renewal'),(20,'ITDesk','renewalheading'),(17,'ITDesk','tickethistory'),(15,'ITDesk','tkt_cat'),(18,'ITDesk','tkt_subcat'),(34,'ITDesk','vendor'),(67,'ITDesk','voipapi'),(37,'ITDesk','voiprecord'),(12,'Layout_Master','childmenu'),(73,'Layout_Master','childmenudesignationaccess'),(10,'Layout_Master','menu'),(74,'Layout_Master','menudesignationaccess'),(11,'Layout_Master','submenu'),(75,'Layout_Master','submenudesignationaccess'),(46,'PasswordVault','passworddepartmentaccess'),(42,'PasswordVault','passwordentry'),(47,'PasswordVault','passwordgroupaccess'),(69,'PasswordVault','passworduseraccess'),(41,'PasswordVault','vaultaudit'),(5,'sessions','session'),(72,'SpaceView','workstation');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
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
