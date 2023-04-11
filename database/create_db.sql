DROP DATABASE IF EXISTS ChatApp;
CREATE DATABASE ChatApp;
USE ChatApp;

CREATE TABLE User (
    id INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Channel (
    id INT AUTO_INCREMENT,
    channel_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Watching (
    user_id INT,
    channel_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (channel_id) REFERENCES Channel(id)
);

CREATE TABLE Block (
    user_id INT,
    block_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (block_id) REFERENCES User(id)
);

CREATE TABLE Active (
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Missed (
    user_id INT,
    message VARCHAR(500) NOT NULL,
    from_user INT NOT NULL,
    sender_name VARCHAR(50) NOT NULL,
    time DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);