-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-db
-- Generation Time: Sep 24, 2021 at 10:00 AM
-- Server version: 5.7.35
-- PHP Version: 7.4.20


SET GLOBAL event_scheduler = ON;
SET
SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET
time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db`
--

-- --------------------------------------------------------

--
-- Table structure for table `condo`
--

DROP TABLE IF EXISTS `condo`;
CREATE TABLE `condo`
(
    `id`               int(11) NOT NULL,
    `details`          text,
    `name`             varchar(100) DEFAULT NULL,
    `zone`             varchar(100) DEFAULT NULL,
    `url`              varchar(200) DEFAULT NULL,
    `created_at`       datetime     DEFAULT NULL,
    `updated_at`       datetime     DEFAULT NULL,
    `condo_status_id`  int(11) DEFAULT NULL,
    `source_id`        int(11) NOT NULL,
    `mongo_id`         varchar(50),
    `record_status_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `offer`
--

DROP TABLE IF EXISTS `offer`;
CREATE TABLE `offer`
(
    `id`                 int(11) NOT NULL,
    `bathroom_no`        int(11) DEFAULT NULL,
    `construction_date`  datetime       DEFAULT NULL,
    `created_at`         datetime       DEFAULT NULL,
    `updated_at`         datetime       DEFAULT NULL,
    `current_price`      decimal(10, 0) DEFAULT NULL,
    `description`        text,
    `room_no`            int(11) DEFAULT NULL,
    `mongo_id`           varchar(50),
    `terase_usable_area` decimal(10, 0) DEFAULT NULL,
    `usable_area`        decimal(10, 0) DEFAULT NULL,
    `url`                varchar(200)   DEFAULT NULL,
    `offer_status_id`    int(11) DEFAULT NULL,
    `source_id`          int(11) NOT NULL,
    `parent_id`          int(11) DEFAULT NULL,
    `condo_id`           int(11) NOT NULL,
    `record_status_id`   int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
CREATE TABLE `source`
(
    `id`     int(11) NOT NULL,
    `name`   varchar(10)  DEFAULT NULL,
    `url`    varchar(200) DEFAULT NULL,
    `config` json         DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
CREATE TABLE `status`
(
    `id`   int(11) NOT NULL,
    `name` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `condo`
--
ALTER TABLE `condo`
    ADD PRIMARY KEY (`id`),
  ADD KEY `condo_status_id` (`condo_status_id`),
  ADD KEY `source_id` (`source_id`),
  ADD KEY `record_status_id` (`record_status_id`);

--
-- Indexes for table `offer`
--
ALTER TABLE `offer`
    ADD PRIMARY KEY (`id`),
  ADD KEY `offer_status_id` (`offer_status_id`),
  ADD KEY `source_id` (`source_id`),
  ADD KEY `parent_id` (`parent_id`),
  ADD KEY `condo_id` (`condo_id`),
  ADD KEY `record_status_id` (`record_status_id`);

--
-- Indexes for table `source`
--
ALTER TABLE `source`
    ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `url` (`url`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
    ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `condo`
--
ALTER TABLE `condo`
    MODIFY `id` int (11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `offer`
--
ALTER TABLE `offer`
    MODIFY `id` int (11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `source`
--
ALTER TABLE `source`
    MODIFY `id` int (11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
    MODIFY `id` int (11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `condo`
--
ALTER TABLE `condo`
    ADD CONSTRAINT `condo_ibfk_1` FOREIGN KEY (`condo_status_id`) REFERENCES `status` (`id`),
  ADD CONSTRAINT `condo_ibfk_2` FOREIGN KEY (`source_id`) REFERENCES `source` (`id`),
  ADD CONSTRAINT `condo_ibfk_3` FOREIGN KEY (`record_status_id`) REFERENCES `status` (`id`);

--
-- Constraints for table `offer`
--
ALTER TABLE `offer`
    ADD CONSTRAINT `offer_ibfk_1` FOREIGN KEY (`offer_status_id`) REFERENCES `status` (`id`),
  ADD CONSTRAINT `offer_ibfk_2` FOREIGN KEY (`source_id`) REFERENCES `source` (`id`),
  ADD CONSTRAINT `offer_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `offer` (`id`),
  ADD CONSTRAINT `offer_ibfk_4` FOREIGN KEY (`condo_id`) REFERENCES `condo` (`id`),
  ADD CONSTRAINT `offer_ibfk_5` FOREIGN KEY (`record_status_id`) REFERENCES `status` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
CREATE EVENT cleaning ON SCHEDULE EVERY 1 WEEK ENABLE
  DO
  DELETE FROM `offer`
  WHERE `created_at` < DATE_SUB(NOW() , INTERVAL 1 MONTH);


INSERT INTO `status` (`id`, `name`)

VALUES (4, 'DELETED'),
       (2, 'EXISTING'),
       (1, 'NEW'),
       (5, 'PROCESSED'),
       (3, 'UPDATED');
INSERT INTO `source` (`id`, `name`, `url`, `config`)
    VALUES (1, 'Imobiliare', 'imobiliare.ro', '{\"SOURCE\":{\"BASE_URL\":\"https://www.imobiliare.ro\",\"CONDO_ZONE\":\".header_proiect .linkuri> li:nth-last-child(2) a span\",\"CONDOS_URL\":\"https://www.imobiliare.ro/ansambluri-rezidentiale/bucuresti?sort=1\",\"PAGINATION\":true,\"CONDO_OFFERS_URL_SUFIX\":\"/proprietati#proprietati\",\"CONDO_OFFERS_URL_REPLACE\":\"?sursa=20\",\"DATA\":{\"CONDOS_PAGINATION_SELECTOR_URL\":\"#content-wrapper > div.container-lista-ansambluri > div.container-oferte div.row.imo-paginare > div > div > a\",\"CONDOS_SELECTOR\":\"#content-wrapper > div.container-lista-ansambluri > div.container-oferte.split > div:nth-child(4) > div.row > div\",\"OFFERS_SELECTOR\":\".grup_camere  div.box-oferta > div.detalii-oferta\",\"PRICE_SELECTOR\":\"#content-detalii > div#box-prezentare div.pret.first\",\"EXPIRED_SELECTOR\":\"#oferta_expirata\",\"PROPERTIES_ROOT_SELECTOR\":\"#b_detalii_caracteristici\",\"USABLE_AREA_TEXT\":\"Suprafaţă utilă\",\"BATHROOM_NO_TEXT\":\"Nr. băi\",\"ROOM_NO_TEXT\":\"Nr. camere\",\"CONSTRUCTION_DATE_TEXT\":\"An construcţie\",\"TOTAL_USABLE_AREA_TEXT\":\"Suprafaţă utilă total\"}}}');