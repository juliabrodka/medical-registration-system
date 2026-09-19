-- SELECT patients.first_name,patients.last_name,patients.pesel from patients;

-- SELECT * FROM doctors
-- WHERE active=1;;

-- SELECT * from doctors
-- WHERE specialization='Cardiology';

-- SELECT * FROM patients
-- WHERE last_name LIKE 'Now%';
-- SELECT * FROM doctors
-- ORDER BY last_name ;

-- SELECT COUNT(*) FROM patients

-- SELECT specialization,COUNT(*) AS doctor_count FROM doctors
-- GROUP BY specialization;

-- SELECT doctors.first_name,doctors.last_name,doctors.room from doctors
-- where specialization='Cardiology'
-- order by last_name

-- select * from patients
-- where email is not null

-- select count(*) as doctor_count from doctors
-- where active=1

-- select count(*) as patients_with_phone_num from patients
-- where phone is not null

-- select specialization,count(*) as doctor_count from doctors
-- group by specialization
-- order by doctor_count desc

-- SELECT * FROM appointments;

-- SELECT date, time, doctors.first_name, doctors.last_name, status
-- from appointments
--          join doctors on appointments.doctor_id = doctors.doctor_id

-- select date, time, doctors.first_name, doctors.last_name, patients.first_name, patients.last_name, status
-- from appointments
--          join doctors on appointments.doctor_id = doctors.doctor_id
--          left join patients on appointments.patient_id = patients.patient_id

-- select date,time,status, doctors.last_name as doctor_last_name,patients.last_name as patient_last_name
-- from appointments
-- join doctors on appointments.doctor_id = doctors.doctor_id
-- join patients on appointments.patient_id = patients.patient_id
-- where status="BOOKED"

-- select date, time, status, patients.last_name from appointments
-- join doctors on appointments.doctor_id = doctors.doctor_id
-- left join patients on appointments.patient_id = patients.patient_id
-- where doctors.last_name="Kowalska"

-- select *
-- from appointments
-- where status = 'FREE';

-- select date, time, status
-- from appointments
-- where doctor_id = 1 and date between '2026-09-20' and '2026-09-22' and status='FREE'

-- select date,time,doctors.last_name from appointments
-- join doctors on appointments.doctor_id = doctors.doctor_id
-- where patient_id=2

-- select * from appointments
-- where date='2026-09-20'
-- order by time


-- BEGIN TRANSACTION;
--
-- UPDATE doctors
-- SET room = '25'
-- WHERE employee_number = 'DOC002';
--
-- SELECT *
-- FROM doctors
-- WHERE employee_number = 'DOC002';
--
-- commit ;

-- BEGIN TRANSACTION;
--
-- UPDATE patients
-- SET active = 0
-- WHERE patient_id = 1;
--
-- SELECT *
-- FROM patients
-- WHERE patient_id = '1';
--
-- rollback ;

-- BEGIN TRANSACTION;
--
-- UPDATE appointments
-- SET patient_id=3 ,status='BOOKED'
-- WHERE appointment_id = 1;
--
-- SELECT *
-- FROM appointments
-- WHERE appointment_id = 1;
--
-- rollback ;

-- BEGIN TRANSACTION;
--
-- DELETE  FROM appointments
-- WHERE appointment_id = 5;
--
-- SELECT *
-- FROM appointments;
--
--
-- rollback ;

-- BEGIN TRANSACTION;
--
-- UPDATE appointments
-- SET status='CANCELLED'
-- WHERE doctor_id=2 and date='2026-09-20';
--
-- SELECT *
-- FROM appointments
-- WHERE doctor_id = 2;
--
-- rollback ;

-- select distinct doctors.specialization from doctors;

-- select * from appointments
-- order by date, time
-- limit 2;

-- SELECT specialization, COUNT(*)
-- FROM doctors
-- GROUP BY specialization
-- HAVING COUNT(*) > 1;

-- SELECT first_name,
--        last_name,
--        specialization
-- FROM doctors
-- WHERE active = 1
--   AND specialization IN (
--       SELECT specialization
--       FROM doctors
--       WHERE active = 1
--       GROUP BY specialization
--       HAVING COUNT(*) >= 2
--   );

-- select patients.first_name, patients.last_name
-- from patients
-- where patient_id in (select patient_id
--                      from appointments
--                      where appointments.patient_id is not null)

-- select doctors.first_name, doctors.last_name from doctors
-- where doctor_id in(
--     select doctor_id from appointments
--                      where status='BOOKED'
--     )

-- select * from appointments
-- where date =(
--     select min(date) from appointments
--
--     )

-- EXPLAIN QUERY PLAN
-- SELECT *
-- FROM patients
-- WHERE last_name = 'Nowak';

-- EXPLAIN QUERY PLAN
-- SELECT *
-- FROM appointments
-- WHERE doctor_id = 1
--   AND status = 'FREE'
--   AND date BETWEEN '2026-09-20' AND '2026-09-22';
