CREATE DATABASE IF NOT EXISTS Authentication_DataBase DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Authentication_DataBase`;

CREATE TABLE IF NOT EXISTS `Accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

