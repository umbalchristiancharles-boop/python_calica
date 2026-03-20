-- Updated Hotel Database Schema v2.0
-- Generated for Hotel Reservation System
-- Run this in phpMyAdmin after backing up existing DB

DROP DATABASE IF EXISTS `hotel_db`;
CREATE DATABASE `hotel_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `hotel_db`;

-- Room Types Table (normalized prices)
CREATE TABLE `room_types` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `price_per_night` DECIMAL(8,2) NOT NULL,
  `max_guests` INT DEFAULT 4,
  `description` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `room_types` (`name`, `price_per_night`, `max_guests`, `description`) VALUES
('Standard', 100.00, 4, 'Comfortable standard room'),
('Deluxe', 250.00, 4, 'Luxury deluxe room with extra amenities'),
('Suite', 500.00, 6, 'Presidential suite with full amenities');

-- Users Table (unified auth for admin/customer)
CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `email` VARCHAR(255) UNIQUE NOT NULL,
  `phone` VARCHAR(20),
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('admin', 'customer') DEFAULT 'customer',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_username` (`username`),
  INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Default admin
INSERT INTO `users` (`name`, `username`, `email`, `phone`, `password`, `role`) VALUES
('Hotel Admin', 'Admin', 'admin@hotel.com', '09000000000', 'Admin@123', 'admin');

-- Updated Bookings Table with FKs
CREATE TABLE `bookings` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NULL,
  `room_type_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(20),
  `email` VARCHAR(255),
  `checkin` DATE NOT NULL,
  `checkout` DATE NOT NULL,
  `nights` INT NOT NULL,
  `guests` INT NOT NULL,
  `payment` VARCHAR(50) DEFAULT 'Cash at Check-in',
  `requests` TEXT,
  `status` ENUM('Pending', 'Confirmed', 'Checked-in', 'Checked-out', 'Cancelled') DEFAULT 'Confirmed',
  `total_bill` DECIMAL(10,2) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
  FOREIGN KEY (`room_type_id`) REFERENCES `room_types`(`id`) ON DELETE RESTRICT,
  INDEX `idx_name` (`name`),
  INDEX `idx_checkin` (`checkin`),
  INDEX `idx_status` (`status`),
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Trigger to auto-calculate nights and total
DELIMITER //
CREATE TRIGGER `before_booking_insert` BEFORE INSERT ON `bookings`
FOR EACH ROW
BEGIN
  SET NEW.nights = DATEDIFF(NEW.checkout, NEW.checkin);
  IF NEW.nights <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Checkout must be after checkin';
  END IF;
  SET NEW.total_bill = NEW.nights * (SELECT price_per_night FROM room_types WHERE id = NEW.room_type_id) * NEW.guests;
END//

CREATE TRIGGER `before_booking_update` BEFORE UPDATE ON `bookings`
FOR EACH ROW
BEGIN
  SET NEW.nights = DATEDIFF(NEW.checkout, NEW.checkin);
  SET NEW.total_bill = NEW.nights * (SELECT price_per_night FROM room_types WHERE id = NEW.room_type_id) * NEW.guests;
END//
DELIMITER ;

-- Sample data migration for existing bookings
INSERT INTO `bookings` (`user_id`, `room_type_id`, `name`, `phone`, `email`, `room_type`, `checkin`, `checkout`, `nights`, `guests`, `payment`, `requests`, `status`, `total_bill`) VALUES
(1, 1, 'Charles Umbal', '09071616515', 'charles@test.com', 'Standard - $100', '2026-04-02', '2026-04-06', 4, 4, 'Cash at Check-in', 'none', 'Confirmed', 1600.00),
(1, 1, 'Gab', '09071413515', 'gab@test.com', 'Standard - $100', '2026-04-20', '2026-04-23', 3, 10, 'Credit Card', 'ywuwu', 'Confirmed', 3000.00);

-- View for app compatibility (old room_type string)
CREATE VIEW `bookings_view` AS
SELECT b.*, u.name AS user_name, u.username, rt.name AS room_type_name, 
       CONCAT(rt.name, ' - $', rt.price_per_night) AS room_type_display
FROM bookings b
LEFT JOIN users u ON b.user_id = u.id
LEFT JOIN room_types rt ON b.room_type_id = rt.id;

-- Migration Notes:
-- 1. Backup your current DB first!
-- 2. Run this full script to recreate DB with improvements
-- 3. Update app queries to use room_type_id (1=Standard,2=Deluxe,3=Suite)
-- 4. For existing data: manually update room_type column or remap
