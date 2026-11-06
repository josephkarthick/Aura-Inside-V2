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
-- Table structure for table `assessment_testquestion`
--

DROP TABLE IF EXISTS `assessment_testquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_testquestion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question_text` longtext NOT NULL,
  `question_type` varchar(20) NOT NULL,
  `marks` int unsigned NOT NULL,
  `test_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Assessment_testquest_test_id_76d3dbb3_fk_Assessmen` (`test_id`),
  CONSTRAINT `Assessment_testquest_test_id_76d3dbb3_fk_Assessmen` FOREIGN KEY (`test_id`) REFERENCES `assessment_testpaper` (`id`),
  CONSTRAINT `assessment_testquestion_chk_1` CHECK ((`marks` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_testquestion`
--

LOCK TABLES `assessment_testquestion` WRITE;
/*!40000 ALTER TABLE `assessment_testquestion` DISABLE KEYS */;
INSERT INTO `assessment_testquestion` VALUES (1,'Teset','single',1,4),(2,'Testing','single',1,5),(3,'What is AD (Full Form)','single',5,6),(4,'Useage of Firewall','single',1,6),(5,'Radio button Test','single',1,7),(6,'What is AD','single',15,8),(7,'Usage of Firewall ','single',18,8),(8,'What is phishing?','single',1,9),(9,'What does the infusion start and stop time help determine?','single',1,10),(10,' What modifier should be added to an E&M service when an infusion service or minor surgery is billed separately on the same date?','single',1,10),(11,'What is the first action for a non-covered denial?','single',1,10),(12,'04. What should be verified first while working an authorization denial?','single',1,10),(13,'______________________Document may be needed for medical necessity ','single',1,10),(14,'_____________POS & ______________________ modifier commonly used for Tele health services.','single',1,10),(15,'What POS code is used when tele health service is provided in the patient’s home.','single',1,10),(16,'What should be verified first while working a bundled denial?','single',1,10),(17,'If a bundled denial is processed incorrectly, what should be done?','single',1,10),(18,'For which payer is a referral compulsory?','single',1,10),(19,'If the patient is covered as a dependent under both parents’ insurance policies and both payers are active, which payer will be considered primary?','single',1,10),(20,'What is the first step while working a lab codes inclusive denial?','single',1,10),(21,'Which modifier may sometimes be appropriate when lab tests are truly distinct and separately identifiable?','single',1,10),(22,'Which modifier may be required when procedures are performed on different anatomical sites?','single',1,10),(23,'For CPT codes 20610 and 20611, the commonly used modifiers are _____________________________','single',1,10),(24,'Under Medicare, services performed by an NP are generally reimbursed at approximately:','single',1,10),(25,'“Incident-to” billing allows NP services to be billed under:','single',1,10),(26,'CLIA stands for ________________________________','single',1,10),(27,'Which box contains prior authorization number when required?','single',1,10),(28,'Rendering provider NPI & Taxonomy code is generally entered in:','single',1,10);
/*!40000 ALTER TABLE `assessment_testquestion` ENABLE KEYS */;
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
