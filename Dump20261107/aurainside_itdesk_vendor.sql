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
-- Table structure for table `itdesk_vendor`
--

DROP TABLE IF EXISTS `itdesk_vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itdesk_vendor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `gst_number` varchar(50) DEFAULT NULL,
  `address` longtext,
  `contact_number` varchar(50) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itdesk_vendor`
--

LOCK TABLES `itdesk_vendor` WRITE;
/*!40000 ALTER TABLE `itdesk_vendor` DISABLE KEYS */;
INSERT INTO `itdesk_vendor` VALUES (1,'Konet Technology Inc','33AMPPR4120G1Z2','New 20 Old 17, Nakoda Plaza, Ground Gloor, Narasingapuram Street, Mount Road, Chennai - 600002','9840343500','monettechnology@gmail.com'),(6,'Simos Peripherals PVT LTD','33AAFCS9993N1ZF','No 5, Poes Rd 1st St, Subbarayan Nagar, Teynampet, Chennai, Tamil Nadu 600018','9884302635','accounts@simosindia.com'),(8,'Spudweb','33AEEPK6536R1Z0','No  1, Rajambal St, opp. to Hindi Prachara Sabha Street, Tnagar, T. Nagar, Chennai, Tamil Nadu 600017','9382265650','info@spudweb.in'),(9,'Nexbase Information Technologies PVT LTD','33AAFCN6593B1ZJ','No  34,1st Cross Street, Jafferkhanpet, Ganga Nagar, Ashok Nagar, Chennai, Tamil Nadu 600083','0444352402','operation@nexbase.in'),(10,'Siplink','33AAXCS9375G1ZK','No.88, 3rd Floor, Anmol Palani Complex, , Gopathy Narayana Rd, T. Nagar, Chennai, Tamil Nadu 600017','4448636371','billing@siplink.in'),(11,'Skyfall','33AAKCA4657N1Z9',' No.67, Main Road, Sri Kumaran Nagar, Thorapakkamm, Perungudi, Chennai, Tamil Nadu 600097','8754401333','support@skyfall.com'),(12,'Pulse Telesystems PVT LTD','33AADCP2122L1ZP','No :  11/9, Pulse Province, Sterling road 3rd cross street, Nungambakkam, Chennai, Tamil Nadu 600034','4440001800','voice-support@pulse.in'),(13,'Security Planet','33GDLPS2857F1Z6','#9. Shop No.2, First Floor, Nakoda Towers, Narsingapuram St, Chennai 600002','9500816008','eyeon@gmail.com'),(15,'SafeZone Secure Solutions PVT LTD','33AAHCS6574D1Z7','No 3, Palat Madhavan Road, Mahalingapuram, Chennai - 600 034','9382388801','safezone@safezone.co.in'),(16,'PTS Powertronic Solutions PVT LTD','33AAKCA4657N1Z9','No. 50/8, Madhavan Nair Road, Mahalingapuram, Nungambakkam, Chennai - 600 034','9841029976','sales@ptspowertronics.com'),(17,'Abhijith Computers','33BKIPS3612K1Z1','No. 39, O Block, 11th Street, Agathiyar Nagar, Vlillivakkam, Chennai - 600 049','9841430510','abhijithcomputers@gmail.com'),(18,'Pulse Voip','','','0444000180','voice-support@pulse.in'),(19,'Unified','','','0444611535',''),(20,'ISP lease Line  Vendor ','','','9962564662',''),(21,'Website Hosting (Xerago)','','93, Industrial Estate, Perungudi, Chennai, Greater Chennai, Tamil Nadu 600096','9884482934','');
/*!40000 ALTER TABLE `itdesk_vendor` ENABLE KEYS */;
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
