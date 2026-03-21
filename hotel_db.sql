-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 21, 2026 at 11:14 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `room_type_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `checkin` date NOT NULL,
  `checkout` date NOT NULL,
  `nights` int(11) NOT NULL,
  `guests` int(11) NOT NULL,
  `payment` varchar(50) DEFAULT 'Cash at Check-in',
  `requests` text DEFAULT NULL,
  `status` enum('Pending','Confirmed','Checked-in','Checked-out','Cancelled') DEFAULT 'Confirmed',
  `total_bill` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `cancellation_reason` text DEFAULT NULL,
  `rebooked_from_id` int(11) DEFAULT NULL,
  `rebooking_reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `bookings`
--
DELIMITER $$
CREATE TRIGGER `before_booking_insert` BEFORE INSERT ON `bookings` FOR EACH ROW BEGIN
  SET NEW.nights = DATEDIFF(NEW.checkout, NEW.checkin);
  IF NEW.nights <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Checkout must be after checkin';
  END IF;
  SET NEW.total_bill = NEW.nights * (SELECT price_per_night FROM room_types WHERE id = NEW.room_type_id) * NEW.guests;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `before_booking_update` BEFORE UPDATE ON `bookings` FOR EACH ROW BEGIN
  SET NEW.nights = DATEDIFF(NEW.checkout, NEW.checkin);
  SET NEW.total_bill = NEW.nights * (SELECT price_per_night FROM room_types WHERE id = NEW.room_type_id) * NEW.guests;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `bookings_view`
-- (See below for the actual view)
--
CREATE TABLE `bookings_view` (
`id` int(11)
,`user_id` int(11)
,`room_type_id` int(11)
,`name` varchar(255)
,`phone` varchar(20)
,`email` varchar(255)
,`checkin` date
,`checkout` date
,`nights` int(11)
,`guests` int(11)
,`payment` varchar(50)
,`requests` text
,`status` enum('Pending','Confirmed','Checked-in','Checked-out','Cancelled')
,`total_bill` decimal(10,2)
,`created_at` timestamp
,`user_name` varchar(100)
,`username` varchar(50)
,`room_type_name` varchar(50)
,`room_type_display` varchar(64)
);

-- --------------------------------------------------------

--
-- Table structure for table `room_types`
--

CREATE TABLE `room_types` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price_per_night` decimal(8,2) NOT NULL,
  `max_guests` int(11) DEFAULT 4,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room_types`
--

INSERT INTO `room_types` (`id`, `name`, `price_per_night`, `max_guests`, `description`, `created_at`) VALUES
(1, 'Standard', 100.00, 4, 'Comfortable standard room', '2026-03-21 04:01:56'),
(2, 'Deluxe', 250.00, 4, 'Luxury deluxe room with extra amenities', '2026-03-21 04:01:56'),
(3, 'Suite', 500.00, 6, 'Presidential suite with full amenities', '2026-03-21 04:01:56');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','customer') DEFAULT 'customer',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `email`, `phone`, `password`, `role`, `created_at`) VALUES
(1, 'Hotel Admin', 'Admin', 'admin@hotel.com', '09000000000', 'Admin@123', 'admin', '2026-03-21 04:01:56');

-- --------------------------------------------------------

--
-- Structure for view `bookings_view`
--
DROP TABLE IF EXISTS `bookings_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `bookings_view`  AS SELECT `b`.`id` AS `id`, `b`.`user_id` AS `user_id`, `b`.`room_type_id` AS `room_type_id`, `b`.`name` AS `name`, `b`.`phone` AS `phone`, `b`.`email` AS `email`, `b`.`checkin` AS `checkin`, `b`.`checkout` AS `checkout`, `b`.`nights` AS `nights`, `b`.`guests` AS `guests`, `b`.`payment` AS `payment`, `b`.`requests` AS `requests`, `b`.`status` AS `status`, `b`.`total_bill` AS `total_bill`, `b`.`created_at` AS `created_at`, `u`.`name` AS `user_name`, `u`.`username` AS `username`, `rt`.`name` AS `room_type_name`, concat(`rt`.`name`,' - $',`rt`.`price_per_night`) AS `room_type_display` FROM ((`bookings` `b` left join `users` `u` on(`b`.`user_id` = `u`.`id`)) left join `room_types` `rt` on(`b`.`room_type_id` = `rt`.`id`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_type_id` (`room_type_id`),
  ADD KEY `idx_name` (`name`),
  ADD KEY `idx_checkin` (`checkin`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_user` (`user_id`),
  ADD KEY `fk_rebooked_from` (`rebooked_from_id`);

--
-- Indexes for table `room_types`
--
ALTER TABLE `room_types`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `room_types`
--
ALTER TABLE `room_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_type_id`) REFERENCES `room_types` (`id`),
  ADD CONSTRAINT `fk_rebooked_from` FOREIGN KEY (`rebooked_from_id`) REFERENCES `bookings` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
