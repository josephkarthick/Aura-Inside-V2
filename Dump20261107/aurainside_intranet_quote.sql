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
-- Table structure for table `intranet_quote`
--

DROP TABLE IF EXISTS `intranet_quote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intranet_quote` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intranet_quote`
--

LOCK TABLES `intranet_quote` WRITE;
/*!40000 ALTER TABLE `intranet_quote` DISABLE KEYS */;
INSERT INTO `intranet_quote` VALUES (13,'Success is not final, failure is not fatal: it is the courage to continue that counts.','Winston Churchill',1,'2026-04-15 21:42:04.000000'),(14,'The only way to do great work is to love what you do.','Steve Jobs',1,'2026-04-15 21:42:04.000000'),(15,'Don’t watch the clock; do what it does. Keep going.','Sam Levenson',1,'2026-04-15 21:42:04.000000'),(16,'Opportunities don\'t happen. You create them.','Chris Grosser',1,'2026-04-15 21:42:04.000000'),(17,'Hard work beats talent when talent doesn’t work hard.','Tim Notke',1,'2026-04-15 21:42:04.000000'),(18,'Your limitation—it’s only your imagination.','',1,'2026-04-15 21:42:04.000000'),(19,'Push yourself, because no one else is going to do it for you.','',1,'2026-04-15 21:42:04.000000'),(20,'Great things never come from comfort zones.','',1,'2026-04-15 21:42:04.000000'),(21,'Dream it. Wish it. Do it.','',1,'2026-04-15 21:42:04.000000'),(22,'Stay positive, work hard, make it happen.','',1,'2026-04-15 21:42:04.000000');
/*!40000 ALTER TABLE `intranet_quote` ENABLE KEYS */;
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
