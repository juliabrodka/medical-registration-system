-- INSERT INTO doctors (employee_number,
--                      first_name,
--                      last_name,
--                      specialization,
--                      room)
-- VALUES ('DOC001',
--         'Anna',
--         'Kowalska',
--         'Cardiology',
--         '12A');
-- INSERT INTO doctors (employee_number,
--                      first_name,
--                      last_name,
--                      specialization,
--                      room)
-- VALUES ('DOC002',
--         'Jan',
--         'Nowak',
--         'Neurology',
--         '21');
-- INSERT INTO doctors (employee_number,
--                      first_name,
--                      last_name,
--                      specialization,
--                      room)
-- VALUES ('DOC003',
--         'Maria',
--         'Nowakowska',
--         'Cardiology',
--         '41');
-- INSERT INTO doctors (employee_number,
--                      first_name,
--                      last_name,
--                      specialization,
--                      room)
-- VALUES ('DOC004',
--         'Piotr',
--         'Wiśniewski',
--         'Dermatology',
--         'B03');
-- INSERT INTO patients(first_name,
--                      last_name,
--                      pesel,
--                      phone,
--                      email,
--                      address)
-- VALUES ("Anna",
--         "Kowalska",
--         "67100702304",
--         "500600700",
--         "",
--         "");
-- INSERT INTO patients(first_name,
--                      last_name,
--                      pesel,
--                      phone,
--                      email,
--                      address)
-- VALUES ("Jan",
--         "Nowak",
--         "92052412346",
--         "",
--         "jan.nowak@example.com",
--         "");
-- INSERT INTO patients(first_name,
--                      last_name,
--                      pesel,
--                      phone,
--                      email,
--                      address)
-- VALUES ("Maria",
--         "Nowakowska",
--         "85031512344",
--         "600700800",
--         "maria@example.com",
--         "");
-- INSERT INTO patients(first_name,
--                      last_name,
--                      pesel,
--                      phone,
--                      email,
--                      address)
-- VALUES ("Piotr",
--         "Wiśniewski",
--         "99010112342",
--         "700800900",
--         "",
--         "");

INSERT INTO appointments(date,
                         time,
                         doctor_id,
                         patient_id,
                         status)
VALUES ("2026-09-20",
        "10:00",
        1,
        NULL,
        "FREE");

INSERT INTO appointments(date,
                         time,
                         doctor_id,
                         patient_id,
                         status)
VALUES ("2026-09-20",
        "11:00",
        1,
        2,
        "BOOKED");
INSERT INTO appointments(date,
                         time,
                         doctor_id,
                         patient_id,
                         status)
VALUES ("2026-09-20",
        "12:00",
        2,
        NULL,
        "CANCELLED");
INSERT INTO appointments(date,
                         time,
                         doctor_id,
                         patient_id,
                         status)
VALUES ("2026-09-21",
        "10:00",
        2,
        1,
        "BOOKED");
INSERT INTO appointments(date,
                         time,
                         doctor_id,
                         patient_id,
                         status)
VALUES ("2026-09-21",
        "9:00",
        1,
        NULL,
        "FREE");