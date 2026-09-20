-- ============================================================
-- KIIT BUS TRACKER - DATABASE SCHEMA
-- ============================================================

DROP DATABASE IF EXISTS bus_tracker;
CREATE DATABASE bus_tracker;

USE bus_tracker;


-- ============================================================
-- BUSES
-- ============================================================

CREATE TABLE buses (
    bus_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_number VARCHAR(20) NOT NULL,
    capacity INT NOT NULL,

    -- Used for simulated movement when GPS is unavailable
    current_index INT DEFAULT 0,

    -- Latest GPS position
    current_lat DECIMAL(10, 7) NULL,
    current_lng DECIMAL(10, 7) NULL,

    -- Time at which the GPS position was last received
    last_updated TIMESTAMP NULL DEFAULT NULL
);


-- ============================================================
-- DRIVERS
-- ============================================================

CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE
);


-- ============================================================
-- ROUTES
-- ============================================================

CREATE TABLE routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(100) NOT NULL,
    start_stop VARCHAR(100) NOT NULL,
    end_stop VARCHAR(100) NOT NULL
);


-- ============================================================
-- STOPS
-- ============================================================

CREATE TABLE stops (
    stop_id INT AUTO_INCREMENT PRIMARY KEY,
    stop_name VARCHAR(100) NOT NULL,

    -- Human-readable location description
    location VARCHAR(150),

    -- Geographic coordinates
    lat DECIMAL(10, 7) NULL,
    lng DECIMAL(10, 7) NULL
);


-- ============================================================
-- ROUTE STOPS
-- ============================================================

CREATE TABLE route_stops (
    route_id INT NOT NULL,
    stop_id INT NOT NULL,
    stop_order INT NOT NULL,

    PRIMARY KEY (route_id, stop_id),

    FOREIGN KEY (route_id)
        REFERENCES routes(route_id)
        ON DELETE CASCADE,

    FOREIGN KEY (stop_id)
        REFERENCES stops(stop_id)
        ON DELETE CASCADE
);


-- ============================================================
-- SCHEDULES
-- ============================================================

CREATE TABLE schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,

    bus_id INT NULL,
    driver_id INT NULL,
    route_id INT NOT NULL,

    departure_time TIME NOT NULL,

    FOREIGN KEY (bus_id)
        REFERENCES buses(bus_id)
        ON DELETE SET NULL,

    FOREIGN KEY (driver_id)
        REFERENCES drivers(driver_id)
        ON DELETE SET NULL,

    FOREIGN KEY (route_id)
        REFERENCES routes(route_id)
        ON DELETE CASCADE
);
