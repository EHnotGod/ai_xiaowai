-- Reconstructed from the SQL statements in the original main.py.
-- The archive did not contain the original DDL; this is a compatible new schema.
-- Create/select your own database before importing this file.

CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `password` TEXT NOT NULL,
    `base64` LONGTEXT,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user-session` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` VARCHAR(255) NOT NULL,
    `session_id` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_user_session_user` (`user_id`),
    KEY `idx_user_session_session` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `conversations` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `session_id` VARCHAR(255) NOT NULL,
    `message` LONGTEXT,
    `picmessage` LONGTEXT,
    PRIMARY KEY (`id`),
    KEY `idx_conversations_session` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
