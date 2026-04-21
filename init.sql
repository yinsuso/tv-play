CREATE DATABASE IF NOT EXISTS movie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE movie_db;

CREATE TABLE IF NOT EXISTS vod (
    vod_id INT PRIMARY KEY,
    vod_name VARCHAR(255) NOT NULL,
    type_id INT,
    type_name VARCHAR(100),
    vod_en VARCHAR(255),
    vod_time DATETIME,
    vod_remarks VARCHAR(100),
    vod_play_from VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS category (
    type_id INT PRIMARY KEY,
    type_pid INT DEFAULT 0,
    type_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS play_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vod_id INT,
    play_name VARCHAR(255),
    play_url VARCHAR(500),
    play_index INT,
    FOREIGN KEY (vod_id) REFERENCES vod(vod_id)
);

CREATE INDEX idx_vod_type_id ON vod(type_id);
CREATE INDEX idx_vod_name ON vod(vod_name);
CREATE INDEX idx_category_type_pid ON category(type_pid);
