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
-- Table structure for table `itdesk_invoice`
--

DROP TABLE IF EXISTS `itdesk_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itdesk_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_no` varchar(100) NOT NULL,
  `date_of_purchase` date NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `uploaded_copy` varchar(100) DEFAULT NULL,
  `vendor_id` bigint DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `remarks` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_no` (`invoice_no`),
  KEY `ITDesk_invoice_vendor_id_0e7d41b8_fk_ITDesk_vendor_id` (`vendor_id`),
  CONSTRAINT `ITDesk_invoice_vendor_id_0e7d41b8_fk_ITDesk_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `itdesk_vendor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itdesk_invoice`
--

LOCK TABLES `itdesk_invoice` WRITE;
/*!40000 ALTER TABLE `itdesk_invoice` DISABLE KEYS */;
INSERT INTO `itdesk_invoice` VALUES (9,'097/23-24','2023-05-26',105138.00,'invoices/97.pdf',6,NULL,'Switchs'),(10,'098/23-24','2023-05-26',65750.00,'invoices/98.pdf',6,NULL,'AIO'),(11,'303/23-24','2023-09-08',239835.00,'invoices/303.pdf',6,NULL,'Windows 11'),(12,'716/23-24','2024-09-02',167500.00,'invoices/716.pdf',6,NULL,'System'),(13,'354/16-17','2016-09-13',950.00,'invoices/354.pdf',6,NULL,'Catridge'),(14,'739/15-16','2016-03-16',13400.00,'invoices/739.pdf',6,NULL,'Monitor/HDD'),(15,'208/16-17','2016-07-15',4400.00,'invoices/208.pdf',6,NULL,'HS'),(16,'229/23-24','2023-11-07',53354.00,'invoices/229.jpg',6,NULL,'MS Office'),(17,'716/16-17','2017-03-28',1100.00,'invoices/716.pdf',6,NULL,'Keyboard'),(18,'530/21-22','2022-03-28',5275.00,'invoices/530.pdf',6,NULL,'Monitor'),(19,'730/23-24','2024-02-14',132160.00,'invoices/730.pdf',6,NULL,'Windows 11'),(20,'381/22-23','2022-10-13',257830.00,'invoices/381.pdf',6,NULL,'Windows 11/Outlook'),(21,'222/24-25','2024-12-06',169920.00,'invoices/222.pdf',6,NULL,'Windows 11'),(22,'354/22-23','2022-09-29',491700.00,'invoices/354.pdf',6,NULL,'System'),(23,'311/24-25','2024-08-07',169920.00,'invoices/311.pdf',6,NULL,'Windows 11'),(24,'263/24-25','2024-08-23',682040.00,'invoices/263.pdf',6,NULL,'Windows Server'),(25,'137/24-25','2024-08-29',219834.00,'invoices/137.jpg',15,'2025-10-10 03:31:05.323074','Esset Protect 138 Qty'),(26,'742/24-25','2024-07-10',37760.00,'invoices/742.jpg',16,'2025-10-10 03:32:08.289168','20KVA Isolation Transformers ');
/*!40000 ALTER TABLE `itdesk_invoice` ENABLE KEYS */;
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
