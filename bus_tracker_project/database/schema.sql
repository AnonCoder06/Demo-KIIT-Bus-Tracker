DROP DATABASE IF EXISTS bus_tracker;

CREATE DATABASE bus_tracker;

USE bus_tracker;

CREATE TABLE buses (
    bus_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_number VARCHAR(10) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(50) NOT NULL,
    license_number VARCHAR(20) UNIQUE
);

CREATE TABLE routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(50) NOT NULL,
    start_stop VARCHAR(50),
    end_stop VARCHAR(50)
);

CREATE TABLE stops (
    stop_id INT AUTO_INCREMENT PRIMARY KEY,
    stop_name VARCHAR(50) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE route_stops (
    route_id INT,
    stop_id INT,
    stop_order INT,

    PRIMARY KEY (route_id, stop_id),

    CONSTRAINT fk_route
        FOREIGN KEY (route_id)
        REFERENCES routes(route_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_stop
        FOREIGN KEY (stop_id)
        REFERENCES stops(stop_id)
        ON DELETE CASCADE
);

CREATE TABLE schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT NULL,
    driver_id INT NULL,
    route_id INT,
    departure_time TIME,

    CONSTRAINT fk_bus
        FOREIGN KEY (bus_id)
        REFERENCES buses(bus_id)
        ON DELETE SET NULL,

    CONSTRAINT fk_driver
        FOREIGN KEY (driver_id)
        REFERENCES drivers(driver_id)
        ON DELETE SET NULL,

    CONSTRAINT fk_route_schedule
        FOREIGN KEY (route_id)
        REFERENCES routes(route_id)
        ON DELETE CASCADE
);