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
-- Table structure for table `itdesk_tkt_subcat`
--

DROP TABLE IF EXISTS `itdesk_tkt_subcat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itdesk_tkt_subcat` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subcategory` varchar(50) NOT NULL,
  `category_id` bigint NOT NULL,
  `priority_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ITDesk_tkt_subcat_category_id_38af8401_fk_ITDesk_tkt_cat_id` (`category_id`),
  KEY `ITDesk_tkt_subcat_priority_id_b41df5ef` (`priority_id`),
  CONSTRAINT `ITDesk_tkt_subcat_category_id_38af8401_fk_ITDesk_tkt_cat_id` FOREIGN KEY (`category_id`) REFERENCES `itdesk_tkt_cat` (`id`),
  CONSTRAINT `ITDesk_tkt_subcat_priority_id_b41df5ef_fk_ITDesk_pr` FOREIGN KEY (`priority_id`) REFERENCES `itdesk_priority_choice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itdesk_tkt_subcat`
--

LOCK TABLES `itdesk_tkt_subcat` WRITE;
/*!40000 ALTER TABLE `itdesk_tkt_subcat` DISABLE KEYS */;
INSERT INTO `itdesk_tkt_subcat` VALUES (1,'Hardware Issue',1,1),(2,'Desktop / Laptop Issue',1,1),(3,'Monitor Issue',1,2),(4,'Keyboard / Mouse Issue',1,2),(5,'Power / Adapter Issue',1,1),(6,'RAM / Storage Issue',1,1),(7,'Hardware Upgrade',1,3),(8,'Hardware Replacement',1,2),(9,'Software Installation',2,2),(10,'Software Uninstallation',2,3),(11,'Software Update',2,2),(12,'Application Error',2,1),(13,'License / Activation Issue',2,2),(14,'Software Configuration',2,2),(15,'Software Compatibility Issue',2,2),(16,'Connectivity Issue',3,1),(17,'Network Configuration',3,2),(18,'VLAN Setup / Change',3,2),(19,'Port Configuration',3,2),(20,'Switch / Router Issue',3,1),(21,'Bandwidth Issue',3,2),(22,'Network Performance Issue',3,2),(23,'Network Hardware Issue',3,1),(24,'Internet Connectivity',4,1),(25,'Slow Internet',4,2),(26,'Internet Access Issue',4,2),(27,'Website Access Issue',4,2),(28,'Proxy Configuration',4,2),(29,'DNS Issue',4,1),(30,'ISP Issue',4,1),(31,'Email Access Issue',5,1),(32,'Email Sending Issue',5,1),(33,'Email Receiving Issue',5,1),(34,'Mailbox Full',5,2),(35,'Password / Login Issue',5,1),(36,'Email Configuration',5,2),(37,'Email Account Setup',5,2),(38,'Spam / Junk Mail Issue',5,2),(39,'Email Forwarding',5,3),(40,'Email Server Issue',5,1),(41,'New User Access',6,2),(42,'Access Request',6,2),(43,'Password Reset',6,1),(44,'Account Lockout',6,1),(45,'Permission Change',6,2),(46,'Application Access',6,2),(47,'Folder / File Access',6,2),(48,'VPN Access',6,2),(49,'User Deactivation',6,1),(50,'Security Alert',7,1),(51,'Virus / Malware Issue',7,1),(52,'Phishing Email',7,1),(53,'Suspicious Activity',7,1),(54,'Firewall Issue',7,1),(55,'Endpoint Security Issue',7,1),(56,'Security Access Request',7,2),(57,'Security Configuration',7,2),(58,'Password Security Issue',7,1),(59,'Printer Not Working',8,1),(60,'Printer Offline',8,2),(61,'Print Quality Issue',8,2),(62,'Paper Jam',8,2),(63,'Printer Installation',8,2),(64,'Printer Configuration',8,2),(65,'Printer Driver Issue',8,2),(66,'Scanner Issue',8,2),(67,'Toner / Cartridge Issue',8,3),(68,'Server Down',9,1),(69,'Server Performance Issue',9,1),(70,'Server Access Issue',9,1),(71,'Server Configuration',9,2),(72,'Server Maintenance',9,2),(73,'Storage Issue',9,1),(74,'Backup Issue',9,1),(75,'Database Issue',9,1),(76,'Server Monitoring Alert',9,1),(77,'Cloud Service Issue',10,1),(78,'Cloud Access Issue',10,1),(79,'Cloud Configuration',10,2),(80,'User Provisioning',10,2),(81,'Service Configuration',10,2),(82,'Storage Issue',10,2),(83,'Backup / Recovery',10,1),(84,'Monitoring / Alerts',10,2),(85,'Application Error',11,1),(86,'Application Access',11,2),(87,'Application Installation',11,2),(88,'Application Configuration',11,2),(89,'Application Update',11,2),(90,'Application Performance Issue',11,2),(91,'Data Issue',11,1),(92,'Integration Issue',11,1),(93,'Telephone Not Working',12,1),(94,'VoIP Issue',12,1),(95,'Call Quality Issue',12,1),(96,'No Incoming Calls',12,1),(97,'No Outgoing Calls',12,1),(98,'Extension Issue',12,2),(99,'VoIP Account Setup',12,2),(100,'VoIP Configuration',12,2),(101,'Call Routing Issue',12,1),(102,'Troubleshooting',13,2),(103,'IT Assistance',13,2),(104,'System Configuration',13,2),(105,'User Support',13,2),(106,'Installation Request',13,2),(107,'Maintenance Request',13,3),(108,'IT Consultation',13,3),(109,'General IT Issue',13,2),(110,'General Issue',14,2),(111,'Service Request',14,2),(112,'Information Request',14,3),(113,'Other',14,3),(114,'Link Down',4,1);
/*!40000 ALTER TABLE `itdesk_tkt_subcat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:12
