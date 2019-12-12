/*
Navicat MySQL Data Transfer

Source Server         : 172.16.101.223
Source Server Version : 50719
Source Host           : 172.16.101.223:3306
Source Database       : testresult

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2019-12-11 18:54:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for apicount
-- ----------------------------
DROP TABLE IF EXISTS `apicount`;
CREATE TABLE `apicount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(255) DEFAULT NULL COMMENT '项目名称',
  `total` int(11) DEFAULT NULL COMMENT 'api接口数量',
  `starttime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '统计时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='统计各项目接口数量';
