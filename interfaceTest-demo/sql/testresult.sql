/*
Navicat MySQL Data Transfer

Source Server         : 172.16.101.223
Source Server Version : 50719
Source Host           : 172.16.101.223:3306
Source Database       : testresult

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2019-10-14 14:31:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for result
-- ----------------------------
DROP TABLE IF EXISTS `result`;
CREATE TABLE `result` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `project` varchar(255) DEFAULT NULL COMMENT '测试项目',
  `sucesss` int(11) DEFAULT NULL COMMENT '成功数量',
  `error` int(11) DEFAULT NULL COMMENT '报错数量',
  `fail` int(11) DEFAULT NULL COMMENT '失败数量',
  `skip` int(11) DEFAULT NULL COMMENT '跳过数量',
  `total` int(11) DEFAULT NULL COMMENT '总数量',
  `starttime` datetime DEFAULT NULL COMMENT '开始执行时间',
  `duration` text COMMENT '执行耗时',
  `version` varchar(255) DEFAULT NULL COMMENT '测试项目版本',
  `apicount` int(11) DEFAULT NULL COMMENT '本次执行覆盖的接口数',
  `ipaddress` varchar(255) DEFAULT NULL COMMENT '案例执行地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
