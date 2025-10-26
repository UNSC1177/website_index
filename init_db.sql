CREATE DATABASE IF NOT EXISTS baza_osob CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE baza_osob;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('root','user') NOT NULL
);

CREATE TABLE osoby (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    adres TEXT,
    telefon VARCHAR(20),
    pokrewienstwo VARCHAR(50),
    data_urodzenia DATE,
    opis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Dodanie przykładowych kont
INSERT INTO users (username, password_hash, role)
VALUES
('root', '$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'root'),
('user', '$2b$12$YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', 'user');
