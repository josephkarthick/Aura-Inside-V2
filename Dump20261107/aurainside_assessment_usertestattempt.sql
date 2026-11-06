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
-- Table structure for table `assessment_usertestattempt`
--

DROP TABLE IF EXISTS `assessment_usertestattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_usertestattempt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `started_at` datetime(6) NOT NULL,
  `submitted_at` datetime(6) DEFAULT NULL,
  `total_marks` int unsigned NOT NULL,
  `obtained_marks` int unsigned NOT NULL,
  `percentage` decimal(5,2) NOT NULL,
  `is_passed` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `test_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Assessment_usertesta_test_id_0ca6c52f_fk_Assessmen` (`test_id`),
  KEY `Assessment_usertesta_user_id_ce30cd67_fk_Accounts_` (`user_id`),
  CONSTRAINT `Assessment_usertesta_test_id_0ca6c52f_fk_Assessmen` FOREIGN KEY (`test_id`) REFERENCES `assessment_testpaper` (`id`),
  CONSTRAINT `Assessment_usertesta_user_id_ce30cd67_fk_Accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_aurainsideuser` (`id`),
  CONSTRAINT `assessment_usertestattempt_chk_1` CHECK ((`total_marks` >= 0)),
  CONSTRAINT `assessment_usertestattempt_chk_2` CHECK ((`obtained_marks` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_usertestattempt`
--

LOCK TABLES `assessment_usertestattempt` WRITE;
/*!40000 ALTER TABLE `assessment_usertestattempt` DISABLE KEYS */;
INSERT INTO `assessment_usertestattempt` VALUES (8,'2026-07-01 15:38:02.765754','2026-07-01 15:38:02.765754',20,6,30.00,1,'completed',10,240),(9,'2026-07-02 14:28:37.538391','2026-07-02 14:28:37.538391',20,11,55.00,1,'completed',10,166),(12,'2026-07-02 14:31:00.347183','2026-07-02 14:31:00.347183',20,17,85.00,1,'completed',10,145),(13,'2026-07-02 14:32:25.455321','2026-07-02 14:32:25.455321',20,15,75.00,1,'completed',10,262),(14,'2026-07-02 14:32:44.655539','2026-07-02 14:32:44.655539',20,12,60.00,1,'completed',10,26),(15,'2026-07-02 14:32:46.083439','2026-07-02 14:32:46.083439',20,16,80.00,1,'completed',10,237),(16,'2026-07-02 14:32:49.507388','2026-07-02 14:32:49.507388',20,13,65.00,1,'completed',10,224),(17,'2026-07-02 14:33:02.557959','2026-07-02 14:33:02.557959',20,18,90.00,1,'completed',10,62),(19,'2026-07-02 14:33:46.669620','2026-07-02 14:33:46.669620',20,11,55.00,1,'completed',10,290),(20,'2026-07-02 14:33:53.507399','2026-07-02 14:33:53.507399',20,15,75.00,1,'completed',10,68),(21,'2026-07-02 14:34:08.033632','2026-07-02 14:34:08.033632',20,14,70.00,1,'completed',10,235),(22,'2026-07-02 14:34:38.555664','2026-07-02 14:34:38.555664',20,16,80.00,1,'completed',10,181),(23,'2026-07-02 14:35:32.001454','2026-07-02 14:35:32.001454',20,10,50.00,1,'completed',10,17),(24,'2026-07-02 14:35:43.003081','2026-07-02 14:35:43.003081',20,12,60.00,1,'completed',10,6),(25,'2026-07-02 14:35:56.608423','2026-07-02 14:35:56.608423',20,14,70.00,1,'completed',10,16),(26,'2026-07-02 14:36:00.188890','2026-07-02 14:36:00.188890',20,14,70.00,1,'completed',10,28),(27,'2026-07-02 14:36:02.908574','2026-07-02 14:36:02.908574',20,11,55.00,1,'completed',10,276),(28,'2026-07-02 14:36:10.980411','2026-07-02 14:36:10.980411',20,13,65.00,1,'completed',10,32),(29,'2026-07-02 14:36:28.657611','2026-07-02 14:36:28.657611',20,13,65.00,1,'completed',10,291),(30,'2026-07-02 14:36:39.163472','2026-07-02 14:36:39.163472',20,18,90.00,1,'completed',10,105),(31,'2026-07-02 14:36:45.419545','2026-07-02 14:36:45.419545',20,7,35.00,1,'completed',10,248),(32,'2026-07-02 14:37:28.497470','2026-07-02 14:37:28.497470',20,16,80.00,1,'completed',10,31),(34,'2026-07-02 14:41:09.879570','2026-07-02 14:41:09.879570',20,9,45.00,1,'completed',10,172),(36,'2026-07-02 15:26:02.844613','2026-07-02 15:26:02.844613',20,18,90.00,1,'completed',10,135),(37,'2026-07-02 15:26:03.886548','2026-07-02 15:26:03.886548',20,13,65.00,1,'completed',10,69),(39,'2026-07-03 15:22:33.159427','2026-07-03 15:22:33.159427',20,18,90.00,1,'completed',10,292);
/*!40000 ALTER TABLE `assessment_usertestattempt` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:11
