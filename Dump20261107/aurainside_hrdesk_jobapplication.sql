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
-- Table structure for table `hrdesk_jobapplication`
--

DROP TABLE IF EXISTS `hrdesk_jobapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hrdesk_jobapplication` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `experience` varchar(50) NOT NULL,
  `current_company` varchar(200) DEFAULT NULL,
  `working_status` varchar(20) NOT NULL,
  `notice_status` varchar(20) DEFAULT NULL,
  `notice_period_days` int DEFAULT NULL,
  `expected_salary` varchar(100) NOT NULL,
  `resume` varchar(100) NOT NULL,
  `cover_letter` longtext,
  `applied_at` datetime(6) NOT NULL,
  `job_id` bigint NOT NULL,
  `applied_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HRDesk_jobapplication_job_id_e22fd081_fk_HRDesk_jobposting_id` (`job_id`),
  KEY `HRDesk_jobapplicatio_applied_by_id_db6fe058_fk_Accounts_` (`applied_by_id`),
  CONSTRAINT `HRDesk_jobapplicatio_applied_by_id_db6fe058_fk_Accounts_` FOREIGN KEY (`applied_by_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `HRDesk_jobapplication_job_id_e22fd081_fk_HRDesk_jobposting_id` FOREIGN KEY (`job_id`) REFERENCES `hrdesk_jobposting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrdesk_jobapplication`
--

LOCK TABLES `hrdesk_jobapplication` WRITE;
/*!40000 ALTER TABLE `hrdesk_jobapplication` DISABLE KEYS */;
/*!40000 ALTER TABLE `hrdesk_jobapplication` ENABLE KEYS */;
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
