-- Insert sample students
INSERT INTO students (name, department, year, email, phone) VALUES
('Suruthika T', 'IT', '2nd Year', 'suruthika.t@gmail.com', '9876543210');

INSERT INTO students (name, department, year, email, phone) VALUES
('Nivetha S', 'IT', '2nd Year', 'nivetha@gmail.com', '9876500001');

INSERT INTO students (name, department, year, email, phone) VALUES
('Elavarasi R', 'IT', '2nd Year', 'elavarasi@gmail.com', '9876500002');

INSERT INTO students (name, department, year, email, phone) VALUES
('Krithika S', 'IT', '2nd Year', 'krithika@gmail.com', '9876500003');

-- Insert sample courses
INSERT INTO courses (course_name, department) VALUES
('Database Management Systems', 'IT');

INSERT INTO courses (course_name, department) VALUES
('Linear Algebra', 'IT');

INSERT INTO courses (course_name, department) VALUES
('IT Essentials', 'IT');

COMMIT;
