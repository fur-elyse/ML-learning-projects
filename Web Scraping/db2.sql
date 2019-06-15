CREATE DATABASE scraperdb;
USE scraperdb;
ALTER DATABASE scraperdb CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE reviews (id BIGINT(7) NOT NULL AUTO_INCREMENT,
reviewId VARCHAR(100), title VARCHAR(200), stars VARCHAR(100), reviewDate VARCHAR(50), content VARCHAR(10000),PRIMARY KEY(id));
ALTER TABLE reviews CONVERT TO CHARACTER SET utf8mb4 COLLATE
utf8mb4_unicode_ci;
ALTER TABLE reviews CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
ALTER TABLE reviews CHANGE content content VARCHAR(10000) CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
