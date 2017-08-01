# DROP TABLE IF EXISTS `Course`;
# CREATE TABLE `Course` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `name` varchar(80) NOT NULL,
#     `teacher` varchar(80) NOT NULL,
#     `credit` varchar(80) NOT NULL,
#     PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#  - - - - - - - - - - - - - - - - - - - - - - - - #


DROP TABLE IF EXISTS  `account_pk`;
CREATE TABLE `account_pk` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `type` tinyint(1) unsigned NOT NULL COMMENT '账号类型, 0-学生',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号';


DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` int(11) unsigned NOT NULL,
  `name` varchar(50) NOT NULL COMMENT '用户名',
  `gender` tinyint(1) unsigned DEFAULT NULL COMMENT '学生的性别, 0-女, 1-男, 2-未知',
  `type` tinyint(1) unsigned DEFAULT NULL COMMENT ', 学生类型, 0-双学位, 1-元培PPE',
  `grade` int(11) unsigned DEFAULT NULL COMMENT '学生年级',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `student_account`;
CREATE TABLE `student_account` (
  `id` int(11) unsigned NOT NULL,
    `password` varchar(200) DEFAULT NULL COMMENT '密码',
  `salt` varchar(8) DEFAULT NULL COMMENT '盐',
    `status` tinyint(1) unsigned DEFAULT NULL COMMENT '账号状态, 0-正常, 1-需要验证, 2-失效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `student_account_alias`;
CREATE TABLE `student_account_alias` (
  `id` int(11) unsigned NOT NULL,
    `alias` varchar(255) DEFAULT NULL COMMENT '别名',
  `type` tinyint(1) unsigned DEFAULT NULL COMMENT '类型, 0-手机号码, 1-邮件, 2-微信',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `idx_alias_type` (`alias`,`type`),
  KEY `idx_user_id` (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `oauth_token`;
CREATE TABLE `oauth_token` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `client_id` int(11) unsigned NOT NULL COMMENT 'oauth_client id',
  `user_id` int(11) unsigned NOT NULL COMMENT '账号id',
    `access_token` char(30) NOT NULL DEFAULT '' COMMENT '访问token',
  `refresh_token` char(30) DEFAULT '' COMMENT '刷新token',
    `scopes` varchar(255) NOT NULL DEFAULT '' COMMENT '范围',
  `expires_in` int(11) NOT NULL DEFAULT '7776000',
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
    KEY `idx_access_token` (`access_token`),
  KEY `idx_refresh_token` (`refresh_token`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='OAuth Provider token';


DROP TABLE IF EXISTS `oauth_client`;
CREATE TABLE `oauth_client` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(60) CHARACTER SET ucs2 NOT NULL DEFAULT '' COMMENT '客户端名称',
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '状态, 0-正常, 1-实效',
  `client_id` char(30) NOT NULL DEFAULT '' COMMENT '客户端id',
  `client_secret` char(30) NOT NULL DEFAULT '' COMMENT '客户端secret',
  `account_type` tinyint(1) unsigned NOT NULL COMMENT '账号类型, 0-学生s',
  `allowed_scopes` varchar(255) NOT NULL DEFAULT '' COMMENT '权限范围',
  `redirect_uri` varchar(255) NOT NULL DEFAULT '' COMMENT '回调url',
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='OAuth Provider Client';


DROP TABLE IF EXISTS `oauth_grant`;
CREATE TABLE `oauth_grant` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `client_id` int(11) unsigned NOT NULL COMMENT 'oauth_client id',
  `user_id` int(11) unsigned NOT NULL COMMENT '账号id',
  `code` char(30) NOT NULL DEFAULT '' COMMENT 'grant code',
  `scopes` varchar(255) NOT NULL DEFAULT '' COMMENT '范围',
  `redirect_uri` varchar(255) NOT NULL DEFAULT '' COMMENT '回调url',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth_grant_client_code` (`client_id`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='OAuth Provider grant';
