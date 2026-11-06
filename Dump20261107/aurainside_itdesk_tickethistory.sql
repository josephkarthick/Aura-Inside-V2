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
-- Table structure for table `itdesk_tickethistory`
--

DROP TABLE IF EXISTS `itdesk_tickethistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itdesk_tickethistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `previous_status` varchar(20) DEFAULT NULL,
  `new_status` varchar(20) DEFAULT NULL,
  `changed_at` datetime(6) NOT NULL,
  `changed_by` varchar(20) DEFAULT NULL,
  `ticket_id` bigint NOT NULL,
  `assigned_to` varchar(20) DEFAULT NULL,
  `notes` longtext,
  `status_updated_at` datetime(6) DEFAULT NULL,
  `status_updated_by` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ITDesk_tickethistory_ticket_id_b3a70141_fk_ITDesk_new_tkt_id` (`ticket_id`),
  CONSTRAINT `ITDesk_tickethistory_ticket_id_b3a70141_fk_ITDesk_new_tkt_id` FOREIGN KEY (`ticket_id`) REFERENCES `itdesk_new_tkt` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itdesk_tickethistory`
--

LOCK TABLES `itdesk_tickethistory` WRITE;
/*!40000 ALTER TABLE `itdesk_tickethistory` DISABLE KEYS */;
INSERT INTO `itdesk_tickethistory` VALUES (3,NULL,'NEW','2026-10-09 02:57:17.790088','ars3016',3,'ars3016','Ticket created.','2026-10-09 02:57:17.790088','ars3016'),(4,'NEW','IN_PROGRESS','2026-10-09 02:58:40.083073','ars3016',3,'ars3016','On Monday, 21st September 2026, we informed Velmurugan Sir about the issue. He started working on it with support from Parthiban.','2026-10-09 02:58:40.083073','ars3016'),(5,'IN_PROGRESS','ON_HOLD','2026-10-09 03:02:52.671949','ars3016',3,'ars3016','From 21st to 25th September 2026, we worked continuously to restore the mail server. The main challenges were heavy spam traffic due to limited spam filtering on the Mac server, SSL issues, and other server-related problems. We were also dependent on Velmurugan Sir for resolving critical issues, which caused some delays due to his hospitalisation and limited availability.','2026-10-09 03:02:52.671949','ars3016'),(6,'ON_HOLD','RESOLVED','2026-10-09 03:05:23.555450','ars3016',3,'ars3016','I have decided to migrate the on-premises mail server to the existing Zoho cloud environment, where the Aurarcm mail server was already hosted, avoiding additional domain hosting costs. After receiving approval on 26th September 2026, we successfully migrated aurabpo.com to Zoho Cloud. This resolved the incoming and outgoing email issues and improved overall mail server reliability.','2026-10-09 03:05:23.555450','ars3016'),(7,'RESOLVED','PENDING','2026-10-09 03:06:22.455540','ars3016',3,'ars3016','Currently, we are working on migrating the old emails to the new Zoho Cloud mail server.','2026-10-09 03:06:22.455540','ars3016'),(8,NULL,'NEW','2026-10-14 20:01:48.789412','ars3141',4,'ars3141','Ticket created.','2026-10-14 20:01:48.789412','ars3141'),(9,'NEW','IN_PROGRESS','2026-10-14 20:09:26.593924','ars3141',4,'ars3141','On 10th October 2026, we investigated the network issue in the Agastya Wing and identified a faulty power adapter for the D-Link media converter. We replaced the power adapter and verified that fiber connectivity from Visvam to Agastya was restored.\r\n\r\nHowever, the local LAN connectivity was still not working. We restarted all the switches, after which the LAN issue was resolved. Finally, we verified that both fiber uplink and local LAN connectivity were functioning properly .','2026-10-14 20:09:26.593924','ars3141'),(10,'IN_PROGRESS','RESOLVED','2026-10-14 21:04:08.956675','ars3141',4,'ars3141','On 10th October 2026, we investigated the network issue in the Agastya Wing and identified a faulty power adapter for the D-Link media converter. We replaced the power adapter and verified that fiber connectivity from Visvam to Agastya was restored. However, the local LAN connectivity was still not working. We restarted all the switches, after which the LAN issue was resolved. Finally, we verified that both fiber uplink and local LAN connectivity were functioning properly . so we are closing this ticket .','2026-10-14 21:04:08.956675','ars3141'),(11,'NEW','VIEWED','2026-10-17 10:20:59.382060','ars3016',6,'ars3016','Ticket automatically marked as VIEWED when opened.',NULL,NULL),(12,'VIEWED','IN_PROGRESS','2026-10-17 10:22:52.553783','ars3016',6,'ars3016','Sept 29, 3:40:\r\nRaised complaints with both ISPs (TTSL and TCL).',NULL,NULL),(13,'IN_PROGRESS','IN_PROGRESS','2026-10-17 10:23:37.723027','ars3016',6,'ars3016','Troubleshooting Steps Performed:\r\n\r\nTested the Internet connection by bypassing the firewall to rule out a firewall-related issue.\r\nRestarted the MUX power unit.\r\nGenerated troubleshooting reports and submitted them to the TTSL team for further investigation.',NULL,NULL),(14,'IN_PROGRESS','RESOLVED','2026-10-17 10:25:03.957107','ars3016',6,'ars3016','04:42 AM: After Troubleshooting reports were submitted to the TTSL team. The primary network link was subsequently restored.',NULL,NULL),(15,'RESOLVED','RESOLVED','2026-10-17 10:25:35.295544','ars3016',6,'ars3016','04:51 AM: The TCL ILL link was restored.',NULL,NULL),(16,'RESOLVED','RESOLVED','2026-10-17 10:25:50.248687','ars3016',6,'ars3016','04:53 AM: Both Internet links were confirmed to be working normally.',NULL,NULL),(17,'RESOLVED','CLOSED','2026-10-17 10:32:07.166831','ars3016',6,'ars3016','Both the primary TTSL and secondary TCL ILL Internet links were restored. Connectivity was verified, and both links were confirmed operational\r\n\r\nImpact: A major event or technical failure occurred in the provider’s IP backbone network.\r\nResolution: The service provider fixed the issue, and services have now been restored.',NULL,NULL),(18,'NEW','VIEWED','2026-10-29 22:15:29.958363','ars3016',7,'ARS3016','Ticket automatically marked as VIEWED when opened.',NULL,'ARS3016'),(19,'VIEWED','IN_PROGRESS','2026-10-29 22:17:27.542960','ars3016',7,'ARS3016','Ticket Has been Raised :\r\nService Request Number 619822041',NULL,'ARS3016'),(20,'IN_PROGRESS','RESOLVED','2026-10-29 23:03:29.779717','ars3016',7,'ARS3016','The TTSL MUX Router was restarted, The link came back up and connectivity was restored.',NULL,'ARS3016'),(21,'RESOLVED','CLOSED','2026-10-30 03:28:59.508635','ars3016',7,'ars3016','The TTSL MUX Router was restarted, And The link came back up and connectivity was restored.\r\n\r\nPossible Reason: The issue may have been caused by a temporary software hang, a stuck interface, or a communication issue within the router.\r\n\r\nafter Restarting the router may have cleared the temporary fault.',NULL,'ARS3016');
/*!40000 ALTER TABLE `itdesk_tickethistory` ENABLE KEYS */;
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
