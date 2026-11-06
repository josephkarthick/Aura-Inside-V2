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
-- Table structure for table `dashboard_dashboardwidget`
--

DROP TABLE IF EXISTS `dashboard_dashboardwidget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_dashboardwidget` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `widget_type` varchar(10) NOT NULL,
  `app_name` varchar(50) NOT NULL,
  `model_name` varchar(50) NOT NULL,
  `metric` varchar(50) NOT NULL,
  `group_by` varchar(50) DEFAULT NULL,
  `chart_type` varchar(10) DEFAULT NULL,
  `order` int unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `dashboard_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Dashboard_dashboardw_dashboard_id_e0a1652c_fk_Dashboard` (`dashboard_id`),
  CONSTRAINT `Dashboard_dashboardw_dashboard_id_e0a1652c_fk_Dashboard` FOREIGN KEY (`dashboard_id`) REFERENCES `dashboard_dashboard` (`id`),
  CONSTRAINT `dashboard_dashboardwidget_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dashboardwidget`
--

LOCK TABLES `dashboard_dashboardwidget` WRITE;
/*!40000 ALTER TABLE `dashboard_dashboardwidget` DISABLE KEYS */;
INSERT INTO `dashboard_dashboardwidget` VALUES (1,'Ticket Master','table','ITDesk','TicketHistory','count',NULL,NULL,0,1,1);
/*!40000 ALTER TABLE `dashboard_dashboardwidget` ENABLE KEYS */;
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
