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
-- Table structure for table `ijp_application`
--

DROP TABLE IF EXISTS `ijp_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ijp_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `applied_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  `ijp_id` bigint NOT NULL,
  `decided_at` datetime(6) DEFAULT NULL,
  `decided_by_id` bigint DEFAULT NULL,
  `decision_remarks` longtext,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `IJP_ijpapplication_employee_id_ijp_id_59c1089d_uniq` (`employee_id`,`ijp_id`),
  KEY `IJP_ijpapplication_ijp_id_9e3abb30_fk_internal_job_posting_id` (`ijp_id`),
  KEY `IJP_ijpapplication_decided_by_id_fb66f0f6_fk_Accounts_` (`decided_by_id`),
  CONSTRAINT `IJP_ijpapplication_decided_by_id_fb66f0f6_fk_Accounts_` FOREIGN KEY (`decided_by_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `IJP_ijpapplication_employee_id_33467a5a_fk_Accounts_` FOREIGN KEY (`employee_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `IJP_ijpapplication_ijp_id_9e3abb30_fk_internal_job_posting_id` FOREIGN KEY (`ijp_id`) REFERENCES `internal_job_posting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ijp_application`
--

LOCK TABLES `ijp_application` WRITE;
/*!40000 ALTER TABLE `ijp_application` DISABLE KEYS */;
INSERT INTO `ijp_application` VALUES (4,'2026-08-06 19:34:30.473042',479,3,'2026-09-22 13:24:52.068106',18,'Your the only one suitable person for this Job','Approved'),(5,'2026-09-08 12:34:06.830825',282,3,NULL,NULL,NULL,'Pending'),(6,'2026-09-16 14:52:45.240707',356,3,NULL,NULL,NULL,'Pending'),(7,'2026-09-16 14:53:59.855034',353,3,NULL,NULL,NULL,'Pending'),(8,'2026-09-16 14:58:43.108029',364,3,NULL,NULL,NULL,'Pending'),(9,'2026-09-16 15:04:51.543632',297,3,NULL,NULL,NULL,'Pending'),(10,'2026-09-16 15:09:38.767377',357,3,NULL,NULL,NULL,'Pending'),(11,'2026-09-17 17:47:19.704334',366,3,NULL,NULL,NULL,'Pending'),(12,'2026-09-17 17:47:35.039630',371,3,NULL,NULL,NULL,'Pending'),(13,'2026-09-17 17:48:11.375543',373,3,NULL,NULL,NULL,'Pending'),(14,'2026-09-17 17:49:23.872879',369,3,NULL,NULL,NULL,'Pending'),(15,'2026-09-17 17:57:39.190615',442,3,NULL,NULL,NULL,'Pending'),(16,'2026-09-17 17:57:51.259192',524,3,NULL,NULL,NULL,'Pending'),(17,'2026-09-17 18:33:16.653694',458,3,NULL,NULL,NULL,'Pending'),(18,'2026-09-17 18:33:57.017829',467,3,NULL,NULL,NULL,'Pending'),(19,'2026-09-17 19:35:13.279993',418,3,NULL,NULL,NULL,'Pending'),(20,'2026-09-18 09:50:01.612440',456,3,NULL,NULL,NULL,'Pending'),(21,'2026-09-18 09:51:10.987379',473,3,NULL,NULL,NULL,'Pending'),(22,'2026-09-18 10:51:52.406207',483,3,NULL,NULL,NULL,'Pending'),(23,'2026-09-18 10:56:51.785898',495,3,NULL,NULL,NULL,'Pending'),(24,'2026-09-18 10:59:20.135549',493,3,NULL,NULL,NULL,'Pending'),(25,'2026-09-18 11:59:08.662415',521,3,NULL,NULL,NULL,'Pending'),(26,'2026-09-18 21:34:21.043209',538,3,NULL,NULL,NULL,'Pending'),(27,'2026-09-19 09:35:51.101506',499,3,NULL,NULL,NULL,'Pending'),(28,'2026-09-19 15:43:29.208920',377,3,NULL,NULL,NULL,'Pending'),(29,'2026-09-19 16:55:38.723079',525,3,NULL,NULL,NULL,'Pending'),(30,'2026-09-19 16:56:56.820535',465,3,NULL,NULL,NULL,'Pending'),(31,'2026-09-19 17:09:11.713919',317,3,NULL,NULL,NULL,'Pending'),(32,'2026-09-19 17:09:11.713919',18,3,NULL,18,'Testing','Pending'),(33,'2026-10-23 13:21:53.293829',311,6,NULL,NULL,'','Pending'),(34,'2026-10-24 00:04:43.330118',363,6,NULL,NULL,'','Pending'),(35,'2026-10-31 03:12:43.955170',391,6,NULL,NULL,'','Pending');
/*!40000 ALTER TABLE `ijp_application` ENABLE KEYS */;
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
