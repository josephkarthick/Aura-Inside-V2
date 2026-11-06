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
-- Table structure for table `internal_job_posting_designations`
--

DROP TABLE IF EXISTS `internal_job_posting_designations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internal_job_posting_designations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `internaljobposting_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `internal_job_posting_des_internaljobposting_id_de_caff7307_uniq` (`internaljobposting_id`,`designation_id`),
  KEY `internal_job_posting_designation_id_e8ae9ef0_fk_Accounts_` (`designation_id`),
  CONSTRAINT `internal_job_posting_designation_id_e8ae9ef0_fk_Accounts_` FOREIGN KEY (`designation_id`) REFERENCES `accounts_designation` (`id`),
  CONSTRAINT `internal_job_posting_internaljobposting_i_058d0bc4_fk_internal_` FOREIGN KEY (`internaljobposting_id`) REFERENCES `internal_job_posting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internal_job_posting_designations`
--

LOCK TABLES `internal_job_posting_designations` WRITE;
/*!40000 ALTER TABLE `internal_job_posting_designations` DISABLE KEYS */;
INSERT INTO `internal_job_posting_designations` VALUES (4,6,32),(5,6,36),(6,6,51),(7,6,52),(8,6,54),(9,6,55);
/*!40000 ALTER TABLE `internal_job_posting_designations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:18
