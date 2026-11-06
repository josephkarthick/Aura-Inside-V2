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
-- Table structure for table `assessment_testpapergroup`
--

DROP TABLE IF EXISTS `assessment_testpapergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_testpapergroup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_dn` varchar(500) NOT NULL,
  `test_paper_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Assessment_testpaper_test_paper_id_d8131a2a_fk_Assessmen` (`test_paper_id`),
  CONSTRAINT `Assessment_testpaper_test_paper_id_d8131a2a_fk_Assessmen` FOREIGN KEY (`test_paper_id`) REFERENCES `assessment_testpaper` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_testpapergroup`
--

LOCK TABLES `assessment_testpapergroup` WRITE;
/*!40000 ALTER TABLE `assessment_testpapergroup` DISABLE KEYS */;
INSERT INTO `assessment_testpapergroup` VALUES (1,'CN=Humpreyspeak_gp,OU=Humpreyspeak,DC=aurarcm,DC=org',5),(2,'CN=Humpreyspeak_gp,OU=Humpreyspeak,DC=aurarcm,DC=org',6),(3,'CN=IT_GP,OU=IT,DC=aurarcm,DC=org',6),(4,'CN=Wichita_Charges,OU=Wichita,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',7),(5,'CN=IT_GP,OU=IT,DC=aurarcm,DC=org',8),(6,'CN=IT_GP,OU=IT,DC=aurarcm,DC=org',9),(7,'CN=Humpreyspeak_gp,OU=Humpreyspeak,DC=aurarcm,DC=org',10),(8,'CN=Mount Rainier_gp,OU=Mount Rainier,DC=aurarcm,DC=org',10),(9,'CN=Sunflower,OU=Sunflower,DC=aurarcm,DC=org',10),(10,'CN=Diablo_gp,OU=Diablo,DC=aurarcm,DC=org',10),(11,'CN=Wichita_gp,OU=Wichita,DC=aurarcm,DC=org',10),(12,'CN=HP_BIF,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(13,'CN=HP_MIS,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(14,'CN=HP_PAS,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(15,'CN=HP_RVS,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(16,'CN=HP_Charges,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(17,'CN=HP_Copay_AR,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(18,'CN=HP_AR_Calling,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(19,'CN=HP_Benefit_QA,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(20,'CN=HP_Full_Access,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(21,'CN=HP_AR_Analysis,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(22,'CN=HP_Eligibility,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(23,'CN=HP_Infusion_Fax,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(24,'CN=HP_Auth_Calling,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(25,'CN=HP_Payment_Posting,OU=Humphreys_Peak,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(26,'CN=MS_RVS,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(27,'CN=MS_PAS,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(28,'CN=MS_Charges,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(29,'CN=MS_Copay_AR,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(30,'CN=MS_AR_Calling,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(31,'CN=MS_Full_Access,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(32,'CN=MS_AR_Analysis,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(33,'CN=MS_Medical_Records,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(34,'CN=MS_Payment_Posting,OU=Mount_Sunflower,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(35,'CN=DB_AR_Calling,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(36,'CN=DB_AR_Analysis,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(37,'CN=DB_Charges,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(38,'CN=DB_Full_Access,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(39,'CN=DB_Auth_Calling,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(40,'CN=DB_Medical_Records,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(41,'CN=DB_BIF,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(42,'CN=DB_Payment_Posting,OU=Delray_Beach,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(43,'CN=MR_Triage,OU=Mount_Rainier,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(44,'CN=MR_Full_Access,OU=Mount_Rainier,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(45,'CN=MR_Medical_Records,OU=Mount_Rainier,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(46,'CN=MR_Payment_Posting,OU=Mount_Rainier,OU=Projects,OU=SecurityGroups,OU=AuraRcm,DC=aurarcm,DC=org',10),(47,'CN=IT_GP,OU=IT,DC=aurarcm,DC=org',10),(48,'CN=HR_gp,OU=HR,DC=aurarcm,DC=org',10),(49,'CN=admin_gp,OU=Admin,DC=aurarcm,DC=org',10),(50,'CN=delraybeach_gp,OU=Delraybeach,DC=aurarcm,DC=org',10),(51,'CN=Delray Beach_gp,OU=Delray Beach,DC=aurarcm,DC=org',10);
/*!40000 ALTER TABLE `assessment_testpapergroup` ENABLE KEYS */;
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
