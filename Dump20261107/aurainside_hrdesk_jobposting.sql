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
-- Table structure for table `hrdesk_jobposting`
--

DROP TABLE IF EXISTS `hrdesk_jobposting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hrdesk_jobposting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `department` varchar(100) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `employment_type` varchar(50) NOT NULL,
  `shift` varchar(20) NOT NULL,
  `experience_required` varchar(50) NOT NULL,
  `salary_range` varchar(100) DEFAULT NULL,
  `openings` int NOT NULL,
  `last_date` date DEFAULT NULL,
  `description` longtext,
  `responsibilities` longtext,
  `skills_required` longtext,
  `qualification` longtext,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `posted_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HRDesk_jobposting_posted_by_id_7d23dfed_fk_Accounts_` (`posted_by_id`),
  CONSTRAINT `HRDesk_jobposting_posted_by_id_7d23dfed_fk_Accounts_` FOREIGN KEY (`posted_by_id`) REFERENCES `accounts_aurainsideuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrdesk_jobposting`
--

LOCK TABLES `hrdesk_jobposting` WRITE;
/*!40000 ALTER TABLE `hrdesk_jobposting` DISABLE KEYS */;
INSERT INTO `hrdesk_jobposting` VALUES (14,'AR Analyst','AR','Teynampet - Chennai','full_time','Morning','1-3','',3,'2026-04-30','The AR Analyst is responsible for managing accounts receivable within the US healthcare revenue cycle. The role focuses on insurance follow-ups, denial management, and ensuring timely reimbursement of claims from payers. The analyst plays a key role in reducing AR days and improving cash flow.','Perform end-to-end AR follow-up on unpaid or denied claims with insurance companies Analyze and resolve claim denials (e.g., coding issues, eligibility, authorization, timely filing) Work on aging reports to prioritize high-value and old outstanding accounts Initiate appeals and resubmissions for denied or underpaid claims Communicate with payers via calls/emails to resolve claim issues Ensure accurate documentation of all follow-up activities in the system Identify trends in denials and suggest process improvements Coordinate with coding, billing, and front-end teams for issue resolution Meet productivity and quality targets as defined by the organization',NULL,'1.Bachelor’s degree. 2. 1–3 years of experience in US Healthcare AR / RCM','open','2026-04-18 12:12:50.625409',240);
/*!40000 ALTER TABLE `hrdesk_jobposting` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:10
