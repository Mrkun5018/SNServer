CREATE TABLE IF NOT EXISTS `library`
(
	`id` INT AUTO_INCREMENT PRIMARY KEY,
  `md5` varchar(32) NOT NULL UNIQUE,
  `content` text NOT NULL
);

INSERT INTO library(`md5`, `content`) SELECT md5, content from `library.backup`
SELECT * FROM `library`;

CREATE TABLE `record` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(16) DEFAULT NULL,
  `md5` varchar(32) NOT NULL UNIQUE,
  `tags` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `useful` int DEFAULT NULL
)

INSERT INTO record (`title`, `author`, `md5`, `tags`, `timestamp`, `status`, `useful`) SELECT `title`, `author`, `md5`, `tags`, `timestamp`, `status`, `useful` from `library.backup`

SELECT * FROM `record`;