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
-- Table structure for table `internal_job_posting`
--

DROP TABLE IF EXISTS `internal_job_posting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internal_job_posting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `vacancies` int unsigned NOT NULL,
  `minimum_experience_months` int unsigned NOT NULL,
  `minimum_appraisal_rating` decimal(3,1) NOT NULL,
  `appraisal_year` int unsigned NOT NULL,
  `minimum_attendance_rating` decimal(3,1) NOT NULL,
  `attendance_year` int unsigned NOT NULL,
  `description` longtext,
  `application_start_date` date NOT NULL,
  `application_end_date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `internal_job_posting_chk_1` CHECK ((`vacancies` >= 0)),
  CONSTRAINT `internal_job_posting_chk_2` CHECK ((`minimum_experience_months` >= 0)),
  CONSTRAINT `internal_job_posting_chk_3` CHECK ((`appraisal_year` >= 0)),
  CONSTRAINT `internal_job_posting_chk_4` CHECK ((`attendance_year` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internal_job_posting`
--

LOCK TABLES `internal_job_posting` WRITE;
/*!40000 ALTER TABLE `internal_job_posting` DISABLE KEYS */;
INSERT INTO `internal_job_posting` VALUES (3,'AR Analyst',2,18,3.5,2026,93.5,2026,'','2026-08-01','2026-09-20','Closed','2026-08-01 18:07:01.793537','2026-09-19 17:10:55.973498'),(6,'AR Calling – Night Shift',10,1,0.0,2026,1.0,2026,'Night Shift role will be eligible for a night shift allowance of ₹1,200/-','2026-10-21','2026-11-21','Open','2026-10-21 16:31:03.254144','2026-10-21 16:31:03.254144');
/*!40000 ALTER TABLE `internal_job_posting` ENABLE KEYS */;
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
