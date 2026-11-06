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
-- Table structure for table `aura_books_book`
--

DROP TABLE IF EXISTS `aura_books_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aura_books_book` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `author` varchar(150) DEFAULT NULL,
  `year` int unsigned DEFAULT NULL,
  `front_cover_image` varchar(100) DEFAULT NULL,
  `back_cover_image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `back_inside_cover_image` varchar(100) DEFAULT NULL,
  `back_inside_cover_text` longtext,
  `front_inside_cover_image` varchar(100) DEFAULT NULL,
  `front_inside_cover_text` longtext,
  PRIMARY KEY (`id`),
  CONSTRAINT `aura_books_book_chk_1` CHECK ((`year` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aura_books_book`
--

LOCK TABLES `aura_books_book` WRITE;
/*!40000 ALTER TABLE `aura_books_book` DISABLE KEYS */;
INSERT INTO `aura_books_book` VALUES (34,'HR POLICIES','Aura',2026,'books/covers/Front_Pg_pq2ndWl.jpg','','2026-02-12 17:34:20.876949','',NULL,'',NULL),(35,'ISO 27001:2022','',2026,'books/covers/Front_Pg_Ajcnscg.jpg','books/covers/ISO_Badge_QBowmqE.png','2026-11-05 03:05:13.833308','',NULL,'',NULL),(36,'ISO 9001:2015 – DO’s & DON’Ts ','',2026,'books/covers/Front_Pg_cQROWi7.jpg','books/covers/ISO_9001_Badge_qQipb3M.png','2026-11-05 03:08:15.737551','',NULL,'',NULL),(37,'HIPAA COMPLIANCE AWARENESS ','',2026,'books/covers/Front_Pg_iqNqqBm.jpg','books/covers/HIPAA_Badge_4gqWTBQ.png','2026-11-05 03:09:29.392767','',NULL,'',NULL);
/*!40000 ALTER TABLE `aura_books_book` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:17
