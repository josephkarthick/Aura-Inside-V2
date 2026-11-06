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
-- Table structure for table `assessment_testoption`
--

DROP TABLE IF EXISTS `assessment_testoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_testoption` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `option_text` varchar(500) NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `question_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Assessment_testoptio_question_id_8001f377_fk_Assessmen` (`question_id`),
  CONSTRAINT `Assessment_testoptio_question_id_8001f377_fk_Assessmen` FOREIGN KEY (`question_id`) REFERENCES `assessment_testquestion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_testoption`
--

LOCK TABLES `assessment_testoption` WRITE;
/*!40000 ALTER TABLE `assessment_testoption` DISABLE KEYS */;
INSERT INTO `assessment_testoption` VALUES (1,'asdfa',0,1),(2,'asdfasdf',1,1),(3,'asdfdf',1,1),(4,'fdfdsfa',0,1),(5,'A',0,2),(6,'B',1,2),(7,'C',0,2),(8,'D',0,2),(9,'Active Directory',1,3),(10,'Action Directory',0,3),(11,'Add Data',0,3),(12,'Active data',0,3),(13,'Network Security & Controlls',1,4),(14,'User Controlls',0,4),(15,'Authendication controll',0,4),(16,'Asset Management',0,4),(17,'A',0,5),(18,'B',1,5),(19,'Active Directory',1,6),(20,'Active Data',0,6),(21,'Add Data',0,6),(22,'Active Data',0,6),(23,'Network Security',1,7),(24,'Network Load Balancer',1,7),(25,'User Authendication ',0,7),(26,'Antivirus',0,7),(27,' A method used by hackers to steal sensitive information',0,8),(28,'A type of antivirus software',0,8),(29,'A network cable standard',0,8),(30,'A backup solution',0,8),(31,'A. Eligibility',0,9),(32,'B. Units and administration coding',1,9),(33,'C. Provider credentialing',0,9),(34,'D. Insurance premium',0,9),(35,'A. Modifier 59',0,10),(36,'B. Modifier 26',0,10),(37,'C. Modifier 57',0,10),(38,'D. Modifier 25',1,10),(39,'A. Verify the provider contract with the payer and patient benefits',1,11),(40,'B. Delete the claim',0,11),(41,'C. Bill patient immediately',0,11),(42,'D. Submit duplicate claim',0,11),(43,'A. Authorization number',0,12),(44,'B. DOS, CPT/drug, and insurance',0,12),(45,'C. #Units and Frequency',0,12),(46,'D. All the Above',1,12),(47,'A. Progress notes and lab reports',0,13),(48,'B. Progress notes ',0,13),(49,'C. Letter of medical necessity',1,13),(50,'D. Medical records',0,13),(51,'A. 2 & 95',1,14),(52,'B. 11 & 95',0,14),(53,'C. 11 & 25',0,14),(54,'D. 10 & 25 ',0,14),(55,'11',0,15),(56,'15',0,15),(57,'10',1,15),(58,'1',0,15),(59,'A. DX codes',0,16),(60,'B. CPT codes, NCCI edits, and modifier usage',1,16),(61,'C. Surgery code',0,16),(62,'D.  Infusion service',0,16),(63,'A. Delete claim',0,17),(64,'B. Submit corrected claim or appeal with supporting documentation',1,17),(65,'C. Ignore denial',0,17),(66,'D. Bill patient directly',0,17),(67,'A. All federal',0,18),(68,'B. Only federal',0,18),(69,'C. BCBS Federal',0,18),(70,'D.  veteran affairs.',1,18),(71,'A. Father’s insurance always',0,19),(72,'B. Mother’s insurance always',0,19),(73,'C. The payer of the parent whose birthday comes first in the calendar year',1,19),(74,'D. The payer with higher coverage ',0,19),(75,'A. Delete the claim',0,20),(76,'B. Review billed CPT codes and panel coding guidelines',1,20),(77,'C. Bill patient directly',0,20),(78,'D. Ignore denial',0,20),(79,'59',1,21),(80,'25',0,21),(81,'95',0,21),(82,'24',0,21),(83,'95',0,22),(84,'59',1,22),(85,'24',0,22),(86,'25',0,22),(87,'95',0,23),(88,'25',0,23),(89,'24',0,23),(90,'59',1,23),(91,'A. 50% of physician fee schedule',0,24),(92,'B. 85% of physician fee schedule',1,24),(93,'C. 100% always',0,24),(94,'D. 25% of physician fee schedule',0,24),(95,'A. Patient name',0,25),(96,'B. Insurance representative',0,25),(97,'C. Supervising physician NPI',0,25),(98,'D. Front desk staff',0,25),(99,'A. Clinical Laboratory Improvement Amendments',1,26),(100,'B.  Clinical Laboratory Improvement Acts',0,26),(101,'C.  Clinical Laboratory Implementation Amendments',0,26),(102,'D. Clinical Laboratory Implementation Acts',0,26),(103,'A. Box 1a',0,27),(104,'B. Box 21',0,27),(105,'C. Box 23',1,27),(106,'D. Box 24J',0,27),(107,'A. Box 1a',0,28),(108,'B. Box 21',0,28),(109,'C. Box 10',0,28),(110,'D. Box 24J',1,28);
/*!40000 ALTER TABLE `assessment_testoption` ENABLE KEYS */;
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
