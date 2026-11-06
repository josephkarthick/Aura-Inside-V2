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
-- Table structure for table `itdesk_new_tkt`
--

DROP TABLE IF EXISTS `itdesk_new_tkt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itdesk_new_tkt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ticket_id` varchar(20) NOT NULL,
  `reported_by_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `affected_user_id` bigint DEFAULT NULL,
  `asset_type_id` bigint DEFAULT NULL,
  `asset_id` bigint DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  `description` longtext,
  `priority_id` bigint DEFAULT NULL,
  `status` varchar(30) NOT NULL DEFAULT 'NEW',
  `assigned_to_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itdesk_new_tkt_ticket_id_unique` (`ticket_id`),
  KEY `itdesk_new_tkt_reported_by_idx` (`reported_by_id`),
  KEY `itdesk_new_tkt_affected_user_idx` (`affected_user_id`),
  KEY `itdesk_new_tkt_asset_type_idx` (`asset_type_id`),
  KEY `itdesk_new_tkt_asset_idx` (`asset_id`),
  KEY `itdesk_new_tkt_category_idx` (`category_id`),
  KEY `itdesk_new_tkt_subcategory_idx` (`subcategory_id`),
  KEY `itdesk_new_tkt_priority_idx` (`priority_id`),
  KEY `itdesk_new_tkt_assigned_to_idx` (`assigned_to_id`),
  CONSTRAINT `itdesk_new_tkt_affected_user_fk` FOREIGN KEY (`affected_user_id`) REFERENCES `accounts_aurainsideuser` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_asset_fk` FOREIGN KEY (`asset_id`) REFERENCES `itdesk_itasset` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_asset_type_fk` FOREIGN KEY (`asset_type_id`) REFERENCES `itdesk_assetcategory` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_assigned_to_fk` FOREIGN KEY (`assigned_to_id`) REFERENCES `accounts_aurainsideuser` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_category_fk` FOREIGN KEY (`category_id`) REFERENCES `itdesk_tkt_cat` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_priority_fk` FOREIGN KEY (`priority_id`) REFERENCES `itdesk_priority_choice` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_reported_by_fk` FOREIGN KEY (`reported_by_id`) REFERENCES `accounts_aurainsideuser` (`id`) ON DELETE SET NULL,
  CONSTRAINT `itdesk_new_tkt_subcategory_fk` FOREIGN KEY (`subcategory_id`) REFERENCES `itdesk_tkt_subcat` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itdesk_new_tkt`
--

LOCK TABLES `itdesk_new_tkt` WRITE;
/*!40000 ALTER TABLE `itdesk_new_tkt` DISABLE KEYS */;
INSERT INTO `itdesk_new_tkt` VALUES (3,'ARS-ITINC001',18,'2026-10-09 02:57:17.781089',NULL,5,205,9,68,'<p>On 19th September 2026. We are experiencing <strong>mail server performance issues and slowness due to a large volume of spam emails and associated files accumulating on the server.</strong></p>',1,'PENDING',18),(4,'ARS-ITINC002',496,'2026-10-14 20:01:48.789412',496,4,NULL,3,20,'<p><span style=\"color: rgb(13, 13, 13); font-family: -apple-system-body, ui-sans-serif, -apple-system, system-ui, &quot;Segoe UI&quot;, Helvetica, &quot;Apple Color Emoji&quot;, Arial, sans-serif, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;; white-space: pre-line; background-color: rgb(252, 252, 252);\">We experienced a network issue in the Agastya Wing on 3rd October 2026. The fiber uplink connectivity from Visvam to Agastya was down, resulting in a loss of network connectivity.</span></p>',1,'RESOLVED',496),(6,'ARS-ITINC003',18,'2026-10-17 10:14:27.350283',18,3,206,4,114,'<p data-pm-slice=\"1 1 []\"><span style=\"font-weight: bolder;\">Incident Date:</span> Tuesday, September 29</p><p><br></p><p>Both the primary TTSL Internet link and the secondary TCL ILL link went down simultaneously, resulting in an interruption to Internet connectivity.</p>',1,'CLOSED',18),(7,'ARS-ITINC007',18,'2026-10-29 22:15:19.821102',18,3,206,4,114,'<p>Our TTSL Primary Internet Link Got Down</p>',1,'CLOSED',18);
/*!40000 ALTER TABLE `itdesk_new_tkt` ENABLE KEYS */;
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
