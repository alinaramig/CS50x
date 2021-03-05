-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Acessing crime scene report
SELECT description FROM crime_scene_reports
    WHERE month = 7
    AND day = 28
    AND year = 2020
    AND street LIKE "%Chamberlin%";

-- 10:15, Chamberlin Street Courthouse, 3 witnesses

-- Find interviews of the 3 witnesses
SELECT transcript FROM interviews
    WHERE month = 7
    AND day = 28
    AND year = 2020;

-- within 10 min the suspect left the scene
-- Before theft suspect withdrew money from ATF on Fifer
-- Called acmplice for less than a minute
-- Earliset flight out of fiftyville the next day
-- Asled acomplice to purchase the ticket

-- Geting court survelince activity
SELECT license_plate FROM courthouse_security_logs
    WHERE month = 7
    AND day = 28
    AND year = 2020
    AND hour = 10
    AND minute > 15
    AND minute <= 25;

-- Possible license plates 5P2BI95
--94KL13X
--6P58WS2
--4328GD8
--G412CB7
--L93JTIZ
--322W7JE
--0NTHK55

-- ATM information
SELECT account_number FROM atm_transactions
    WHERE month = 7
    AND day = 28
    AND year = 2020
    AND atm_location LIKE "%Fifer%"
    AND transaction_type LIKE "Withdraw";

-- Account number and amount withdrew
--28500762
--28296815
--76054385
--49610011
--16153065
--25506511
--81061156 
--26013199

-- Cross refrencing atm info with the bank and license place information
SELECT name FROM people
    WHERE id IN 
        (SELECT person_id FROM bank_accounts WHERE account_number IN
             (SELECT account_number FROM atm_transactions
                 WHERE month = 7
                AND day = 28
                AND year = 2020
                AND atm_location LIKE "%Fifer%"
                AND transaction_type LIKE "Withdraw"))
    AND license_plate IN
        (SELECT license_plate FROM courthouse_security_logs
             WHERE month = 7
             AND day = 28
             AND year = 2020
             AND hour = 10
             AND minute > 15
             AND minute <= 25);

-- Names of possible suspects
--Elizabeth
--Danielle
--Russell
--Ernest

-- Looking into Phone Reccords
SELECT caller FROM phone_calls
    WHERE year = 2020
    AND month = 7
    AND day = 28
    AND duration < 60;

-- Finding the names of the phone calls
SELECT name FROM people
    WHERE phone_number IN
        (SELECT caller FROM phone_calls
            WHERE year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60);

-- Phone number names
--Bobby
--Roger
--Victoria
--Madison
--Russell
--Evelyn
--Ernest
--Kimberly

-- Must be Ernset or Russel

-- What airport can he fly out of
SELECT id, abbreviation, full_name FROM airports
    WHERE city LIKE "%Fiftyville%";

-- 8 CSF | Fiftyville Regional Airport

-- Find the earliest flight the next morning
SELECT id, destination_airport_id, hour, minute FROM flights
    WHERE origin_airport_id = 8
    AND year = 2020
    AND month = 7
    AND day = 29;

-- Flight info: 36  to :4 8:20

--Find passport of everyone on that flight
SELECT name FROM people
    WHERE passport_number IN
    (SELECT passport_number FROM passengers
    WHERE flight_id = 36);

-- Ernest!!!!

-- Where was he going?
SELECT city FROM airports
    WHERE id = 4;

-- London!!

-- Find his phone_number and search for acomplice
 SELECT name FROM people
    WHERE phone_number IN
        (SELECT receiver FROM phone_calls
            WHERE year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60
            AND caller IN 
                (SELECT phone_number FROM people
                    WHERE name LIKE "Ernest"));

--Berthold!!
