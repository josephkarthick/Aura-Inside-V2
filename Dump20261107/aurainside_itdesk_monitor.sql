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
-- Table structure for table `itdesk_monitor`
--

DROP TABLE IF EXISTS `itdesk_monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itdesk_monitor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `monitor_number` int DEFAULT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `serial_number` varchar(255) DEFAULT NULL,
  `resolution` varchar(100) DEFAULT NULL,
  `refresh_rate` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `asset_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itdesk_monitor`
--

LOCK TABLES `itdesk_monitor` WRITE;
/*!40000 ALTER TABLE `itdesk_monitor` DISABLE KEYS */;
INSERT INTO `itdesk_monitor` VALUES (56,1,'DELF11F','Generic PnP Monitor','689WRS3','1600x900','64 Hz','2026-09-17 17:29:57.843134','ARS-D160'),(57,1,'Default_Monitor','Generic Non-PnP Monitor','Device Parameters','1366x768','32 Hz','2026-09-18 00:25:56.861553','ABSPLD137'),(58,1,'LEN9021','Generic PnP Monitor','Device Parameters','1920x1080','60 Hz','2026-09-25 00:13:00.899669','ARS-L021'),(61,1,'DELF11F','Generic PnP Monitor','5BRB9V3','1600x900','60 Hz','2026-10-01 20:36:54.006385','ABSPLD106'),(62,2,'DELF11E','Generic PnP Monitor','3L1L914','1600x900','60 Hz','2026-10-01 20:36:54.006385','ABSPLD106');
/*!40000 ALTER TABLE `itdesk_monitor` ENABLE KEYS */;
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
