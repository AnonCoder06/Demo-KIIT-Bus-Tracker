-- ============================================================
-- KIIT BUS TRACKER - SAMPLE DATA
-- ============================================================

USE bus_tracker;


-- ============================================================
-- BUSES
-- ============================================================

INSERT INTO buses
    (bus_number, capacity, current_index, current_lat, current_lng)
VALUES
    ('OD01B101', 40, 0, NULL, NULL),
    ('OD01B102', 50, 0, NULL, NULL),
    ('OD01B103', 45, 0, NULL, NULL),
    ('OD01B104', 60, 0, NULL, NULL);


-- ============================================================
-- DRIVERS
-- ============================================================

INSERT INTO drivers
    (driver_name, license_number)
VALUES
    ('Rakesh Nayak', 'OD-DR-1001'),
    ('Suresh Behera', 'OD-DR-1002'),
    ('Amit Mohanty', 'OD-DR-1003');


-- ============================================================
-- ROUTES
-- ============================================================

INSERT INTO routes
    (route_name, start_stop, end_stop)
VALUES
    ('Route 1', 'Master Canteen', 'KIIT Square'),
    ('Route 2', 'Airport', 'Jaydev Vihar'),
    ('Route 3', 'Khandagiri', 'Vani Vihar');


-- ============================================================
-- STOPS
-- ============================================================

INSERT INTO stops
    (stop_name, location, lat, lng)
VALUES
    (
        'Master Canteen',
        'Master Canteen, Bhubaneswar',
        20.2634,
        85.8397
    ),
    (
        'Jaydev Vihar',
        'Jaydev Vihar, Bhubaneswar',
        20.2961,
        85.8245
    ),
    (
        'KIIT Square',
        'KIIT Square, Bhubaneswar',
        20.3555,
        85.8172
    ),
    (
        'Airport',
        'Biju Patnaik International Airport, Bhubaneswar',
        20.2529,
        85.8178
    ),
    (
        'Khandagiri',
        'Khandagiri, Bhubaneswar',
        20.2547,
        85.7756
    ),
    (
        'Vani Vihar',
        'Vani Vihar, Bhubaneswar',
        20.2967,
        85.8415
    );


-- ============================================================
-- ROUTE 1
-- Master Canteen -> Jaydev Vihar -> KIIT Square
-- ============================================================

INSERT INTO route_stops
    (route_id, stop_id, stop_order)
VALUES
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 3);


-- ============================================================
-- ROUTE 2
-- Airport -> Jaydev Vihar
-- ============================================================

INSERT INTO route_stops
    (route_id, stop_id, stop_order)
VALUES
    (2, 4, 1),
    (2, 2, 2);


-- ============================================================
-- ROUTE 3
-- Khandagiri -> Vani Vihar
-- ============================================================

INSERT INTO route_stops
    (route_id, stop_id, stop_order)
VALUES
    (3, 5, 1),
    (3, 6, 2);


-- ============================================================
-- SCHEDULES
-- ============================================================

INSERT INTO schedules
    (bus_id, driver_id, route_id, departure_time)
VALUES
    (1, 1, 1, '08:00:00'),
    (2, 2, 2, '08:30:00'),
    (3, 3, 3, '09:00:00'),
    (4, NULL, 1, '10:00:00');


-- ============================================================
-- VERIFY DATA
-- ============================================================

SELECT * FROM buses;
SELECT * FROM drivers;
SELECT * FROM routes;
SELECT * FROM stops;
SELECT * FROM route_stops;
SELECT * FROM schedules;
