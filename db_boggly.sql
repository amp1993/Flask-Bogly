
DROP DATABASE IF EXISTS  boggly;

CREATE DATABASE boggly;

\c boggly


CREATE TABLE users
(id SERIAL PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
image_url TEXT
);

INSERT INTO users
(first_name,last_name,image_url)
VALUES
('Alexandra','Pena','example.com');