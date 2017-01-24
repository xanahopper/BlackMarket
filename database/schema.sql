DROP TABLE IF EXISTS `Course`;
CREATE TABLE `Course` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(80) NOT NULL,
    `teacher` varchar(80) NOT NULL,
    `credit` varchar(80) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;