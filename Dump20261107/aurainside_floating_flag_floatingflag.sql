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
-- Table structure for table `floating_flag_floatingflag`
--

DROP TABLE IF EXISTS `floating_flag_floatingflag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `floating_flag_floatingflag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `color` varchar(20) NOT NULL,
  `position_type` varchar(20) NOT NULL,
  `width` int unsigned NOT NULL,
  `height` int unsigned NOT NULL,
  `pos_x` double NOT NULL,
  `pos_y` double NOT NULL,
  `camera_angle` double NOT NULL,
  `wave_horizontal` double NOT NULL,
  `wave_vertical` double NOT NULL,
  `wave_strength` double NOT NULL,
  `wave_speed` double NOT NULL,
  `animation_direction` varchar(20) NOT NULL,
  `animation_enabled` tinyint(1) NOT NULL,
  `z_index` int unsigned NOT NULL,
  `show_close_button` tinyint(1) NOT NULL,
  `auto_close` tinyint(1) NOT NULL,
  `auto_close_seconds` int unsigned NOT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `floating_flag_floatingflag_chk_1` CHECK ((`width` >= 0)),
  CONSTRAINT `floating_flag_floatingflag_chk_2` CHECK ((`height` >= 0)),
  CONSTRAINT `floating_flag_floatingflag_chk_3` CHECK ((`z_index` >= 0)),
  CONSTRAINT `floating_flag_floatingflag_chk_4` CHECK ((`auto_close_seconds` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `floating_flag_floatingflag`
--

LOCK TABLES `floating_flag_floatingflag` WRITE;
/*!40000 ALTER TABLE `floating_flag_floatingflag` DISABLE KEYS */;
INSERT INTO `floating_flag_floatingflag` VALUES (1,'Aura Flag','flags/Flag_FUuyL1D.jpg','#ffffff','custom',565,405,15.4,42.5,0,0.2,0.4,0.2,0.65,'both',1,999,1,1,10,'2026-11-05 00:00:00.000000','2027-01-20 00:00:00.000000',1,'2026-11-05 01:21:09.252590','2026-11-07 01:12:42.131644');
/*!40000 ALTER TABLE `floating_flag_floatingflag` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  3:17:16
