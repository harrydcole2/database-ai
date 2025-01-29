PRAGMA foreign_keys = ON;

CREATE TABLE addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    district TEXT,
    street_address TEXT NOT NULL,
    latitude REAL,  -- SQLite does not support POINT, using separate latitude and longitude
    longitude REAL,
    zip_code TEXT NOT NULL
);

CREATE TABLE universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    address_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    university_id INTEGER NOT NULL,
    FOREIGN KEY (university_id) REFERENCES universities(id)
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    university_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    salary REAL,  -- SQLite does not support DECIMAL(10,2)
    job_type TEXT NOT NULL,
    FOREIGN KEY (university_id) REFERENCES universities(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE job_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE job_tag_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (tag_id) REFERENCES job_tags(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE semesters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    quality_rating INTEGER NOT NULL,
    difficulty_rating INTEGER NOT NULL,
    semester_id INTEGER,
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    flagged BOOLEAN DEFAULT FALSE,
    vote_count INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (semester_id) REFERENCES semesters(id)
);

CREATE TABLE rating_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    flagged BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (rating_id) REFERENCES ratings(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE work_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE work_conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating_id INTEGER NOT NULL,
    work_life_balance INTEGER NOT NULL,
    pay_fairness INTEGER NOT NULL,
    workload INTEGER NOT NULL,
    management INTEGER NOT NULL,
    FOREIGN KEY (rating_id) REFERENCES ratings(id)
);

CREATE TABLE job_benefits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    benefit_name TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);