-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: esa
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `blocks`
--

DROP TABLE IF EXISTS `blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blocks` (
  `pdfId` int NOT NULL,
  `page_num` int NOT NULL,
  `block_order` int NOT NULL,
  `type` int NOT NULL,
  `block_width` int DEFAULT NULL,
  `block_height` int DEFAULT NULL,
  `bbox_x0` double NOT NULL,
  `bbox_y0` double NOT NULL,
  `bbox_x1` double NOT NULL,
  `bbox_y1` double NOT NULL,
  `ext` text,
  `color` int DEFAULT NULL,
  `xres` int DEFAULT NULL,
  `yres` int DEFAULT NULL,
  `bpc` int DEFAULT NULL,
  `block_area` int DEFAULT NULL,
  `bbox_width` double NOT NULL,
  `bbox_height` double NOT NULL,
  `bbox_area` double NOT NULL,
  `bbox_area_image` double NOT NULL,
  `titleTOC` text,
  `page_name` text,
  `titleTag` text,
  `titleFinal` text,
  PRIMARY KEY (`pdfId`,`page_num`,`block_order`),
  CONSTRAINT `pdfId_and_page` FOREIGN KEY (`pdfId`, `page_num`) REFERENCES `pages` (`pdfId`, `page_num`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `csvs`
--

DROP TABLE IF EXISTS `csvs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `csvs` (
  `csvId` varchar(255) NOT NULL,
  `csvFileName` varchar(255) NOT NULL,
  `csvFullPath` text NOT NULL,
  `pdfId` int NOT NULL,
  `page` int NOT NULL,
  `tableNumber` int NOT NULL,
  `topRowJson` json NOT NULL,
  `titleTag` text,
  `titleTOC` text,
  `titleFinal` text,
  `csvRows` int NOT NULL,
  `csvColumns` int NOT NULL,
  `method` varchar(255) NOT NULL,
  `accuracy` float NOT NULL,
  `whitespace` float NOT NULL,
  `csvText` json NOT NULL,
  `dt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `hasContent` tinyint DEFAULT NULL,
  PRIMARY KEY (`csvId`),
  UNIQUE KEY `csvId_UNIQUE` (`csvId`),
  KEY `pdfs_idx` (`pdfId`),
  CONSTRAINT `pdfs` FOREIGN KEY (`pdfId`) REFERENCES `pdfs` (`pdfId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pages`
--

DROP TABLE IF EXISTS `pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pages` (
  `pdfId` int NOT NULL,
  `page_num` int NOT NULL,
  `width` int NOT NULL,
  `height` int NOT NULL,
  `rotation` int NOT NULL,
  `figures` int NOT NULL,
  `num_images` int NOT NULL,
  `media_x0` int NOT NULL,
  `media_y0` int NOT NULL,
  `media_x1` int NOT NULL,
  `media_y1` int NOT NULL,
  `media_width` int NOT NULL,
  `media_height` int NOT NULL,
  `page_area` int NOT NULL,
  PRIMARY KEY (`pdfId`,`page_num`),
  CONSTRAINT `pdf` FOREIGN KEY (`pdfId`) REFERENCES `pdfs` (`pdfId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pdfs`
--

DROP TABLE IF EXISTS `pdfs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pdfs` (
  `pdfId` int NOT NULL,
  `totalPages` int NOT NULL,
  `csvsExtracted` varchar(255) DEFAULT NULL,
  `xmlContent` text,
  `hearingOrder` text,
  `application_name` text,
  `application_title_short` text,
  `short_name` text,
  `commodity` text,
  PRIMARY KEY (`pdfId`),
  UNIQUE KEY `pdfId_UNIQUE` (`pdfId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `toc`
--

DROP TABLE IF EXISTS `toc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `toc` (
  `assigned_count` int DEFAULT NULL,
  `title_type` varchar(255) NOT NULL,
  `titleTOC` text NOT NULL,
  `page_name` text NOT NULL,
  `toc_page_num` int NOT NULL,
  `toc_pdfId` int NOT NULL,
  `toc_title_order` int NOT NULL,
  PRIMARY KEY (`toc_page_num`,`toc_pdfId`,`toc_title_order`),
  KEY `pdf2` (`toc_pdfId`) /*!80000 INVISIBLE */,
  CONSTRAINT `pdf2` FOREIGN KEY (`toc_pdfId`) REFERENCES `pdfs` (`pdfId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-23 17:03:05
