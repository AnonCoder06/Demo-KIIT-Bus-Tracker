USE bus_tracker;

INSERT INTO buses (bus_number, capacity) VALUES
('OD01B101', 40),
('OD01B102', 50),
('OD01B103', 45),
('OD01B104', 60);

INSERT INTO drivers (driver_name, license_number) VALUES
('Rakesh Nayak', 'OD12345'),
('Suresh Behera', 'OD67890'),
('Amit Mohanty', 'OD54321');

INSERT INTO routes (route_name, start_stop, end_stop) VALUES
('Route 1', 'Master Canteen', 'KIIT Square'),
('Route 2', 'Airport', 'Jaydev Vihar'),
('Route 3', 'Khandagiri', 'Vani Vihar');

INSERT INTO stops (stop_name, location) VALUES
('Master Canteen', 'Central Bhubaneswar'),
('Jaydev Vihar', 'NH16 Junction'),
('KIIT Square', 'Patia Area'),
('Airport', 'Biju Patnaik Airport'),
('Khandagiri', 'Khandagiri Hills'),
('Vani Vihar', 'Utkal University Area');

INSERT INTO route_stops (route_id, stop_id, stop_order) VALUES
(1,1,1),  -- Master Canteen
(1,2,2),  -- Jaydev Vihar
(1,3,3),  -- KIIT Square
(2,4,1),  -- Airport
(2,2,2),  -- Jaydev Vihar
(3,5,1),  -- Khandagiri
(3,6,2);  -- Vani Vihar

INSERT INTO schedules (bus_id, driver_id, route_id, departure_time) VALUES
(1,1,1,'08:00:00'),
(2,2,2,'09:30:00'),
(3,3,3,'10:15:00'),
(4,1,1,'12:00:00');