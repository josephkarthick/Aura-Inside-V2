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
-- Table structure for table `intranet_boardmembers`
--

DROP TABLE IF EXISTS `intranet_boardmembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intranet_boardmembers` (
  `id` varchar(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `manager_id` varchar(50) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `chart_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Intranet_boardmembers_manager_id_659bb25a_fk` (`manager_id`),
  CONSTRAINT `Intranet_boardmembers_manager_id_659bb25a_fk` FOREIGN KEY (`manager_id`) REFERENCES `intranet_boardmembers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intranet_boardmembers`
--

LOCK TABLES `intranet_boardmembers` WRITE;
/*!40000 ALTER TABLE `intranet_boardmembers` DISABLE KEYS */;
INSERT INTO `intranet_boardmembers` VALUES ('bm_1','Sr. Management','AuraRCM Services',NULL,'board_members/AuraRCM_Logo.png','management'),('bm_14','Kokila Narayanan','SVP – Corporate Development & Strategy','bm_1','board_members/ARS3002.jpg','management'),('bm_15','Nandhini Parthasarathy','Vice President – Operations & Human Resources','bm_14','board_members/ARS3001.jpg','management'),('bm_16','Padmanabhan Bakthavathsalam','Vice President – Finance & Administration','bm_14','board_members/ARS3003.jpg','management'),('bm_17','Benziger Peter Deraxan','Senior Director – Transition & Delivery',NULL,'board_members/ARS3044.jpg','operation'),('bm_18','Prakash Sivasankaran','Sr.Manager','bm_17','board_members/ARS3036.jpg','operation'),('bm_19','Kannan Velumani','Manager','bm_17','board_members/ARS3136.jpg','operation'),('bm_20','Naveen Anthony','Manager','bm_18','board_members/ARS3007.jpg','operation'),('bm_21','Dominic Anthony Dcruz ','Asst.Manager','bm_18','board_members/ARS3124.jpg','operation'),('bm_22','Karthikeyan Ramdoss','Asst.Manager','bm_19','board_members/ARS3160.jpg','operation'),('bm_23','IT & Admin','IT / Admin ','bm_16','board_members/itadmin.jpg','management'),('bm_24','HR & Operations','HR & Operations','bm_15','board_members/hr.jpg','management'),('bm_25','Group Coordinator','Group Coordinator','bm_20','board_members/Connected_Team_Network_Illustration.png','operation'),('bm_26','Group Coordinator','Group Coordinator','bm_21','board_members/Connected_Team_Network_Illustration_cvL8kr7.png','operation'),('bm_27','Group Coordinator','Group Coordinator','bm_22','board_members/Connected_Team_Network_Illustration_tQO52lC.png','operation'),('bm_28','Team','Team','bm_25','board_members/Corporate_Team_in_Blue_Arc.png','operation'),('bm_29','Team','Team','bm_26','board_members/Corporate_Team_in_Blue_Arc_QSlG21n.png','operation'),('bm_30','Team','Team','bm_27','board_members/Corporate_Team_in_Blue_Arc_fwKFSg1.png','operation');
/*!40000 ALTER TABLE `intranet_boardmembers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:12
