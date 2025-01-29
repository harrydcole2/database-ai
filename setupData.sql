-- 📌 Addresses
INSERT INTO addresses (state, district, street_address, latitude, longitude, zip_code) VALUES
('California', 'District 1', '1234 University St', 37.7749, -122.4194, '90001'),
('New York', 'District 5', '5678 College Ave', 40.7128, -74.0060, '10001'),
('Texas', 'District 3', '4321 Lone Star Rd', 30.2672, -97.7431, '75001'),
('Illinois', 'District 7', '8765 Windy City Blvd', 41.8781, -87.6298, '60601'),
('Florida', 'District 2', '1357 Sunshine St', 27.9949, -81.7603, '33101');

-- 📌 Universities
INSERT INTO universities (name, description, address_id) VALUES
('Stanford University', 'A prestigious private university.', 1),
('Columbia University', 'An Ivy League university.', 2),
('University of Texas', 'Top research institution.', 3),
('University of Chicago', 'Renowned for economics.', 4),
('University of Florida', 'Strong in marine biology.', 5);

-- 📌 Departments
INSERT INTO departments (name, university_id) VALUES
('Computer Science', 1), ('Business', 1), ('Psychology', 2), ('Mathematics', 2),
('Engineering', 3), ('Law', 3), ('Medicine', 4), ('History', 4),
('Physics', 5), ('Finance', 5);

-- 📌 Jobs
INSERT INTO jobs (name, university_id, department_id, salary, job_type) VALUES
('Software Engineer Intern', 1, 1, 20000, 'Internship'),
('Assistant Professor', 2, 4, 85000, 'Faculty'),
('Research Assistant', 1, 3, 25000, 'Research'),
('Teaching Assistant', 3, 2, 15000, 'Part-time'),
('Data Analyst', 4, 9, 55000, 'Full-time'),
('Legal Intern', 3, 6, 18000, 'Internship'),
('Resident Physician', 4, 7, 60000, 'Residency'),
('Finance Associate', 5, 10, 70000, 'Full-time');

-- 📌 Job Tags
INSERT INTO job_tags (name) VALUES
('High Stress'), ('Good Work-Life Balance'), ('Remote Friendly'),
('Low Pay'), ('Excellent Benefits');

-- 📌 Job Tag Assignments
INSERT INTO job_tag_assignments (job_id, tag_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 1), (7, 2), (8, 3);

-- 📌 Users
INSERT INTO users (email, password_hash, display_name, is_verified) VALUES
('alice@example.com', 'hashedpassword1', 'Alice', 1),
('bob@example.com', 'hashedpassword2', 'Bob', 0),
('carol@example.com', 'hashedpassword3', 'Carol', 1),
('dave@example.com', 'hashedpassword4', 'Dave', 1),
('emma@example.com', 'hashedpassword5', 'Emma', 0),
('frank@example.com', 'hashedpassword6', 'Frank', 1),
('grace@example.com', 'hashedpassword7', 'Grace', 0),
('hank@example.com', 'hashedpassword8', 'Hank', 1),
('irene@example.com', 'hashedpassword9', 'Irene', 1),
('jack@example.com', 'hashedpassword10', 'Jack', 0);

-- 📌 Roles
INSERT INTO roles (name) VALUES
('Admin'), ('User'), ('Moderator');

-- 📌 User Roles
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1), (2, 2), (3, 2), (4, 3), (5, 2), (6, 2), (7, 3), (8, 2), (9, 2), (10, 2);

-- 📌 Semesters
INSERT INTO semesters (name) VALUES
('Fall 2022'), ('Spring 2023'), ('Summer 2023'), ('Fall 2023'), ('Spring 2024');

-- 📌 Ratings
INSERT INTO ratings (job_id, user_id, content, quality_rating, difficulty_rating, semester_id, is_anonymous, flagged, vote_count) VALUES
(1, 1, 'Amazing learning experience, but tough workload.', 5, 5, 1, 0, 0, 15),
(2, 2, 'Great pay but management was terrible.', 3, 4, 2, 1, 0, 10),
(3, 3, 'Flexible hours, low pay.', 4, 2, 1, 0, 1, 5),
(4, 4, 'Enjoyed the students, admin was difficult.', 3, 5, 2, 0, 0, 8),
(5, 5, 'The projects were super interesting!', 5, 3, 3, 1, 0, 20),
(6, 6, 'Overworked and underpaid.', 2, 5, 1, 0, 1, 2),
(7, 7, 'Good benefits, but very stressful.', 3, 5, 2, 0, 0, 12),
(8, 8, 'Would do it again, but not for the pay.', 4, 4, 3, 1, 0, 7);

-- 📌 Rating Comments
INSERT INTO rating_comments (rating_id, user_id, content, flagged) VALUES
(1, 2, 'Totally agree with this!', 0),
(2, 3, 'I had the opposite experience.', 0),
(3, 4, 'Management ruined the job for me.', 1);

-- 📌 Work History
INSERT INTO work_history (user_id, job_id, start_date, end_date, is_current) VALUES
(1, 1, '2022-06-01', '2022-12-31', 0),
(2, 2, '2021-08-15', NULL, 1),
(3, 3, '2020-09-01', '2022-05-30', 0),
(4, 4, '2023-01-15', NULL, 1),
(5, 5, '2019-05-10', '2021-12-20', 0);

-- 📌 Work Conditions
INSERT INTO work_conditions (rating_id, work_life_balance, pay_fairness, workload, management) VALUES
(1, 3, 4, 5, 2), (2, 5, 2, 3, 1), (3, 2, 2, 4, 5),
(4, 4, 3, 4, 4), (5, 3, 5, 2, 3), (6, 1, 1, 5, 2);

-- 📌 Job Benefits
INSERT INTO job_benefits (job_id, benefit_name) VALUES
(1, 'Flexible Hours'), (2, 'Tuition Assistance'), (3, 'Health Insurance'),
(4, '401k Matching'), (5, 'Paid Time Off'), (6, 'Remote Work Options');
