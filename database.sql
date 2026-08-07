-- =========================================================
-- Smart Disaster Management and Alert System Database Script
-- Database: disaster_management
-- =========================================================

CREATE DATABASE IF NOT EXISTS `disaster_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `disaster_management`;

-- ---------------------------------------------------------
-- Table structure for `users`
-- ---------------------------------------------------------
DROP TABLE IF EXISTS `disaster_reports`;
DROP TABLE IF EXISTS `alerts`;
DROP TABLE IF EXISTS `shelters`;
DROP TABLE IF EXISTS `safety_guidelines`;
DROP TABLE IF EXISTS `admin_logs`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(64) UNIQUE NOT NULL,
  `email` VARCHAR(120) UNIQUE NOT NULL,
  `password_hash` VARCHAR(256) NOT NULL,
  `full_name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20) DEFAULT NULL,
  `role` VARCHAR(20) NOT NULL DEFAULT 'user', -- 'user' or 'admin'
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table structure for `disaster_reports`
-- ---------------------------------------------------------
CREATE TABLE `disaster_reports` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `disaster_type` VARCHAR(50) NOT NULL, -- Flood, Cyclone, Earthquake, Fire, Landslide, Tsunami, Drought, Other
  `location` VARCHAR(255) NOT NULL,
  `latitude` FLOAT DEFAULT NULL,
  `longitude` FLOAT DEFAULT NULL,
  `date_time` DATETIME NOT NULL,
  `description` TEXT NOT NULL,
  `image_path` VARCHAR(255) DEFAULT NULL,
  `severity` VARCHAR(20) NOT NULL, -- Low, Medium, High
  `status` VARCHAR(20) NOT NULL DEFAULT 'Pending', -- Pending, Active, Resolved
  `risk_level` VARCHAR(20) DEFAULT 'MODERATE', -- CRITICAL, HIGH, MODERATE, LOW
  `safety_recommendation` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table structure for `shelters`
-- ---------------------------------------------------------
CREATE TABLE `shelters` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(150) NOT NULL,
  `address` TEXT NOT NULL,
  `capacity` INT NOT NULL,
  `available_space` INT NOT NULL,
  `contact_number` VARCHAR(30) NOT NULL,
  `maps_url` TEXT DEFAULT NULL,
  `status` VARCHAR(20) NOT NULL DEFAULT 'Open', -- Open, Full, Maintenance
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table structure for `alerts`
-- ---------------------------------------------------------
CREATE TABLE `alerts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(200) NOT NULL,
  `disaster_type` VARCHAR(50) NOT NULL,
  `affected_area` VARCHAR(255) NOT NULL,
  `severity_level` VARCHAR(20) NOT NULL, -- Low, Medium, High, Emergency
  `description` TEXT NOT NULL,
  `evacuation_instructions` TEXT DEFAULT NULL,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table structure for `safety_guidelines`
-- ---------------------------------------------------------
CREATE TABLE `safety_guidelines` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `disaster_type` VARCHAR(50) UNIQUE NOT NULL,
  `before_tips` TEXT NOT NULL,
  `during_tips` TEXT NOT NULL,
  `after_tips` TEXT NOT NULL,
  `first_aid` TEXT NOT NULL,
  `emergency_kit` TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table structure for `admin_logs`
-- ---------------------------------------------------------
CREATE TABLE `admin_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `admin_id` INT NOT NULL,
  `action` VARCHAR(255) NOT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- =========================================================
-- SAMPLE SEED DATA
-- =========================================================

-- Password for admin: admin123 (Werkzeug pbkdf2:sha256 hash)
-- Password for user: user123
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `full_name`, `phone`, `role`, `created_at`) VALUES
(1, 'admin', 'admin@disastermanagement.org', 'pbkdf2:sha256:600000$w091ZgYfX9Yp80pG$8ca243a41b1836c28f99e3ebf03fb5ed7fa5cfbc3ff7174dbbf0e854fa169f46', 'System Administrator', '+1-800-555-0199', 'admin', NOW()),
(2, 'johndoe', 'john@example.com', 'pbkdf2:sha256:600000$w091ZgYfX9Yp80pG$8ca243a41b1836c28f99e3ebf03fb5ed7fa5cfbc3ff7174dbbf0e854fa169f46', 'John Doe', '+1-555-0147', 'user', NOW()),
(3, 'sarah_smith', 'sarah@example.com', 'pbkdf2:sha256:600000$w091ZgYfX9Yp80pG$8ca243a41b1836c28f99e3ebf03fb5ed7fa5cfbc3ff7174dbbf0e854fa169f46', 'Sarah Smith', '+1-555-0188', 'user', NOW());

INSERT INTO `disaster_reports` (`id`, `user_id`, `disaster_type`, `location`, `latitude`, `longitude`, `date_time`, `description`, `image_path`, `severity`, `status`, `risk_level`, `safety_recommendation`, `created_at`) VALUES
(1, 2, 'Flood', 'Riverside District, Sector 4', 28.6139, 77.2090, NOW() - INTERVAL 2 DAY, 'Water level rising rapidly over the embankment. Main arterial road submerged.', 'sample_flood.jpg', 'High', 'Active', 'CRITICAL', 'Evacuate to higher ground immediately. Turn off electrical supply. Avoid driving through flooded streets.', NOW() - INTERVAL 2 DAY),
(2, 3, 'Fire', 'Industrial Park, Building B', 28.5355, 77.3910, NOW() - INTERVAL 1 DAY, 'Chemical warehouse fire spreading towards nearby commercial units. Heavy smoke visible.', 'sample_fire.jpg', 'High', 'Active', 'CRITICAL', 'Keep clear of smoke plume. Use N95 masks or wet cloth over nose and mouth. Follow evacuation wardens.', NOW() - INTERVAL 1 DAY),
(3, 2, 'Cyclone', 'Coastal Boulevard, North Bay', 13.0827, 80.2707, NOW() - INTERVAL 5 DAY, 'High winds causing power line disruption and fallen trees blocking access roads.', 'sample_cyclone.jpg', 'Medium', 'Resolved', 'HIGH', 'Stay indoors away from window panes. Store emergency drinking water and flashlights.', NOW() - INTERVAL 5 DAY),
(4, 3, 'Landslide', 'Highland Pass, Highway 12', 31.1048, 77.1734, NOW() - INTERVAL 3 DAY, 'Debris flow blocking both lanes of Highway 12. Traffic halted.', 'sample_landslide.jpg', 'Medium', 'Active', 'HIGH', 'Do not attempt to pass slope. Be alert for falling rocks. Monitor local traffic radio broadcasts.', NOW() - INTERVAL 3 DAY);

INSERT INTO `shelters` (`id`, `name`, `address`, `capacity`, `available_space`, `contact_number`, `maps_url`, `status`, `created_at`) VALUES
(1, 'Central Community High School Relief Shelter', '124 Park Avenue, City Center', 500, 180, '+1-800-555-7435', 'https://maps.google.com/?q=Central+High+School', 'Open', NOW()),
(2, 'St. Jude Sports Complex Evacuation Center', '45 Stadium Drive, Sector 9', 800, 350, '+1-800-555-8821', 'https://maps.google.com/?q=St+Jude+Sports+Complex', 'Open', NOW()),
(3, 'Northside Civic Center Shelter', '88 Northern Boulevard', 350, 45, '+1-800-555-3390', 'https://maps.google.com/?q=Northside+Civic+Center', 'Open', NOW()),
(4, 'West End Primary School Hall', '12 Westside Road', 200, 0, '+1-800-555-1102', 'https://maps.google.com/?q=West+End+School', 'Full', NOW());

INSERT INTO `alerts` (`id`, `title`, `disaster_type`, `affected_area`, `severity_level`, `description`, `evacuation_instructions`, `is_active`, `created_at`) VALUES
(1, 'Flash Flood Warning: Riverside Sector 4', 'Flood', 'Riverside District, Low-lying coastal zones', 'Emergency', 'Heavy continuous downpour leading to rapid river overflow. Immediate evacuation ordered for ground floor residents.', 'Move immediately to Central Community Relief Shelter on 124 Park Avenue. Carry essential documents, medications, and bottled water.', 1, NOW()),
(2, 'Severe Industrial Fire Safety Alert', 'Fire', 'Industrial Park, Sector 15', 'High', 'Toxic smoke advisory due to warehouse fire. Nearby commercial zones evacuated.', 'Close all doors and windows. Turn off air conditioners. Evacuate towards South exit routes.', 1, NOW());

INSERT INTO `safety_guidelines` (`id`, `disaster_type`, `before_tips`, `during_tips`, `after_tips`, `first_aid`, `emergency_kit`) VALUES
(1, 'Flood', 'Prepare an emergency kit with 3 days of food/water. Identify highest ground level in your home. Install check valves in plumbing.', 'Never walk or drive through moving flood water. If trapped in building, move to roof only if necessary. Keep battery radio on.', 'Avoid floodwater as it may be contaminated. Check structural safety before entering buildings. Discard food touched by floodwater.', 'Treat cuts with clean water and antiseptic. Keep hypothermia risk low by keeping dry.', 'Water (1 gal/person/day), non-perishable food, flashlight, first aid kit, multi-tool, extra batteries, whistle, emergency blanket.'),
(2, 'Fire', 'Test smoke alarms monthly. Keep fire extinguishers on every level. Plan two escape routes from every room.', 'Crawl low under smoke to escape. Touch doors before opening; if hot, use alternate exit. Stop, drop, and roll if clothes catch fire.', 'Do not enter burned structure until cleared by fire department. Cool minor burns with cool water. Document property damage.', 'Cool burns with cold running water for 10-15 mins. Cover with sterile non-stick bandage. Do not pop blisters.', 'N95 dust mask, fire-resistant blanket, burn ointment, heavy gloves, flashlight, emergency contact numbers, bottled water.'),
(3, 'Cyclone', 'Trim trees near house. Secure loose outdoor objects. Board up windows with storm shutters or plywood.', 'Stay inside away from windows and glass doors. Take shelter in small interior room or closet on lowest level.', 'Watch out for fallen power lines. Beware of weakened trees or structures. Drink only bottled or boiled water.', 'Clean debris wounds thoroughly. Use pressure dressing for active bleeding.', 'Battery-powered NOAA weather radio, waterproof pouch for documents, power bank, sturdy boots, rain gear, non-perishable food.'),
(4, 'Earthquake', 'Anchor heavy furniture, appliances, and TVs to walls. Store breakables in low cabinets with latches.', 'DROP, COVER, and HOLD ON! Get under sturdy table/desk. Protect head and neck. If outside, move away from buildings.', 'Expect aftershocks. Check for gas leaks and turn off gas valve if smelling odor. Inspect home for structural cracks.', 'Apply splints to suspected fractures. Do not move severely injured persons unless immediate hazard exists.', 'Sturdy gloves, dust mask, heavy duty flashlight, whistle, emergency shelter tent, 3-day water supply, first aid manual.');
