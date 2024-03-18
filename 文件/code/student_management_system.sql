/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : student_management_system

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2024-01-13 06:50:06
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('a3efe66ecfa4');

-- ----------------------------
-- Table structure for college
-- ----------------------------
DROP TABLE IF EXISTS `college`;
CREATE TABLE `college` (
  `COLLEGE_NO` varchar(4) NOT NULL,
  `COLLEGE_NAME` varchar(10) NOT NULL,
  PRIMARY KEY (`COLLEGE_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of college
-- ----------------------------
INSERT INTO `college` VALUES ('0001', '计算机');
INSERT INTO `college` VALUES ('0002', '管理学');
INSERT INTO `college` VALUES ('0003', '医学');
INSERT INTO `college` VALUES ('0004', '外国语');
INSERT INTO `college` VALUES ('0005', '警官学院');
INSERT INTO `college` VALUES ('0006', '人文学院');
INSERT INTO `college` VALUES ('0007', '体育学院');
INSERT INTO `college` VALUES ('0008', '公共管理');
INSERT INTO `college` VALUES ('0009', '经济');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `COURSE_NO` varchar(8) NOT NULL,
  `COURSE_NAME` varchar(10) NOT NULL,
  `COURSE_CREDIT` int(11) NOT NULL,
  `COURSE_HOUR` int(11) NOT NULL,
  `COLLEGE_NO` varchar(4) NOT NULL,
  PRIMARY KEY (`COURSE_NO`),
  KEY `COLLEGE_NO` (`COLLEGE_NO`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`COLLEGE_NO`) REFERENCES `college` (`COLLEGE_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('10000001', '高等数学', '4', '48', '0001');
INSERT INTO `course` VALUES ('10000002', '审计学', '3', '45', '0002');
INSERT INTO `course` VALUES ('10000003', '数据库设计', '3', '45', '0001');
INSERT INTO `course` VALUES ('10000004', '线性代数', '4', '48', '0001');
INSERT INTO `course` VALUES ('10000005', '病理学', '4', '48', '0003');
INSERT INTO `course` VALUES ('10000006', 'python', '3', '45', '0001');
INSERT INTO `course` VALUES ('10000007', '旅游管理理论', '3', '35', '0002');
INSERT INTO `course` VALUES ('10000008', '商法', '3', '23', '0002');
INSERT INTO `course` VALUES ('10000009', '财务共享', '3', '48', '0002');
INSERT INTO `course` VALUES ('10000010', 'C语言', '3', '45', '0001');
INSERT INTO `course` VALUES ('10000011', '企业行为模拟', '2', '23', '0002');
INSERT INTO `course` VALUES ('10000012', '数据结构', '4', '45', '0001');
INSERT INTO `course` VALUES ('10000013', '流行病学', '4', '48', '0003');
INSERT INTO `course` VALUES ('10000014', '数据库原理', '3', '43', '0001');
INSERT INTO `course` VALUES ('10000015', 'Java', '4', '45', '0001');
INSERT INTO `course` VALUES ('10000016', '计算机网络', '3', '45', '0001');
INSERT INTO `course` VALUES ('10000017', '计算机组成原理', '4', '45', '0008');
INSERT INTO `course` VALUES ('10000018', '多媒体技术与应用', '4', '48', '0001');
INSERT INTO `course` VALUES ('10000019', '电子技术', '4', '45', '0001');
INSERT INTO `course` VALUES ('10000020', '微机系统', '4', '48', '0001');
INSERT INTO `course` VALUES ('10000021', '管理学原理', '3', '38', '0002');
INSERT INTO `course` VALUES ('10000022', '营销学原理', '3', '43', '0002');
INSERT INTO `course` VALUES ('10000023', '财务管理', '3', '45', '0002');
INSERT INTO `course` VALUES ('10000024', '人力资源管理', '3', '45', '0002');
INSERT INTO `course` VALUES ('10000025', '商务统计', '3', '35', '0002');
INSERT INTO `course` VALUES ('10000026', '诊断学', '4', '45', '0003');
INSERT INTO `course` VALUES ('10000027', '无机化学', '4', '48', '0003');
INSERT INTO `course` VALUES ('10000028', '医学检验', '3', '35', '0003');
INSERT INTO `course` VALUES ('10000029', '内科学', '4', '48', '0003');
INSERT INTO `course` VALUES ('10000030', '妇产科学', '4', '48', '0003');
INSERT INTO `course` VALUES ('10000031', '经济贸易', '4', '45', '0009');

-- ----------------------------
-- Table structure for course_select_table
-- ----------------------------
DROP TABLE IF EXISTS `course_select_table`;
CREATE TABLE `course_select_table` (
  `STU_NO` varchar(8) NOT NULL,
  `TEACHER_NO` varchar(8) NOT NULL,
  `COURSE_NO` varchar(8) NOT NULL,
  `GRADE` int(11) DEFAULT NULL,
  PRIMARY KEY (`STU_NO`,`TEACHER_NO`,`COURSE_NO`),
  KEY `COURSE_NO` (`COURSE_NO`),
  KEY `TEACHER_NO` (`TEACHER_NO`),
  CONSTRAINT `course_select_table_ibfk_1` FOREIGN KEY (`COURSE_NO`) REFERENCES `course` (`COURSE_NO`),
  CONSTRAINT `course_select_table_ibfk_2` FOREIGN KEY (`STU_NO`) REFERENCES `student` (`STU_NO`),
  CONSTRAINT `course_select_table_ibfk_3` FOREIGN KEY (`TEACHER_NO`) REFERENCES `teacher` (`TEACHER_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of course_select_table
-- ----------------------------
INSERT INTO `course_select_table` VALUES ('20231001', '30000002', '10000002', null);
INSERT INTO `course_select_table` VALUES ('20231001', '30000007', '10000001', null);
INSERT INTO `course_select_table` VALUES ('20231002', '30000002', '10000002', '77');

-- ----------------------------
-- Table structure for course_teacher
-- ----------------------------
DROP TABLE IF EXISTS `course_teacher`;
CREATE TABLE `course_teacher` (
  `TEACHER_NO` varchar(8) NOT NULL,
  `COURSE_NO` varchar(8) NOT NULL,
  `COURSE_CAPACITY` int(11) NOT NULL,
  PRIMARY KEY (`TEACHER_NO`,`COURSE_NO`),
  KEY `COURSE_NO` (`COURSE_NO`),
  CONSTRAINT `course_teacher_ibfk_1` FOREIGN KEY (`COURSE_NO`) REFERENCES `course` (`COURSE_NO`),
  CONSTRAINT `course_teacher_ibfk_2` FOREIGN KEY (`TEACHER_NO`) REFERENCES `teacher` (`TEACHER_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of course_teacher
-- ----------------------------
INSERT INTO `course_teacher` VALUES ('30000001', '10000003', '45');
INSERT INTO `course_teacher` VALUES ('30000001', '10000005', '34');
INSERT INTO `course_teacher` VALUES ('30000001', '10000006', '11');
INSERT INTO `course_teacher` VALUES ('30000001', '10000016', '57');
INSERT INTO `course_teacher` VALUES ('30000001', '10000017', '34');
INSERT INTO `course_teacher` VALUES ('30000002', '10000002', '44');
INSERT INTO `course_teacher` VALUES ('30000002', '10000011', '44');
INSERT INTO `course_teacher` VALUES ('30000002', '10000021', '68');
INSERT INTO `course_teacher` VALUES ('30000003', '10000008', '66');
INSERT INTO `course_teacher` VALUES ('30000003', '10000026', '49');
INSERT INTO `course_teacher` VALUES ('30000003', '10000029', '43');
INSERT INTO `course_teacher` VALUES ('30000004', '10000004', '19');
INSERT INTO `course_teacher` VALUES ('30000004', '10000014', '10');
INSERT INTO `course_teacher` VALUES ('30000004', '10000020', '42');
INSERT INTO `course_teacher` VALUES ('30000005', '10000007', '0');
INSERT INTO `course_teacher` VALUES ('30000005', '10000022', '0');
INSERT INTO `course_teacher` VALUES ('30000006', '10000010', '22');
INSERT INTO `course_teacher` VALUES ('30000006', '10000013', '40');
INSERT INTO `course_teacher` VALUES ('30000006', '10000027', '67');
INSERT INTO `course_teacher` VALUES ('30000006', '10000030', '0');
INSERT INTO `course_teacher` VALUES ('30000007', '10000001', '39');
INSERT INTO `course_teacher` VALUES ('30000007', '10000023', '78');
INSERT INTO `course_teacher` VALUES ('30000008', '10000015', '42');
INSERT INTO `course_teacher` VALUES ('30000010', '10000009', '9');
INSERT INTO `course_teacher` VALUES ('30000010', '10000024', '20');
INSERT INTO `course_teacher` VALUES ('30000011', '10000028', '0');
INSERT INTO `course_teacher` VALUES ('30000012', '10000012', '4');
INSERT INTO `course_teacher` VALUES ('30000012', '10000018', '0');
INSERT INTO `course_teacher` VALUES ('30000012', '10000019', '58');
INSERT INTO `course_teacher` VALUES ('30000013', '10000025', '67');

-- ----------------------------
-- Table structure for major
-- ----------------------------
DROP TABLE IF EXISTS `major`;
CREATE TABLE `major` (
  `MAJOR_NO` varchar(6) NOT NULL,
  `MAJOR_NAME` varchar(10) NOT NULL,
  `COLLEGE_NO` varchar(4) NOT NULL,
  PRIMARY KEY (`MAJOR_NO`),
  KEY `COLLEGE_NO` (`COLLEGE_NO`),
  CONSTRAINT `major_ibfk_1` FOREIGN KEY (`COLLEGE_NO`) REFERENCES `college` (`COLLEGE_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of major
-- ----------------------------
INSERT INTO `major` VALUES ('100001', '计算机科学与技术', '0001');
INSERT INTO `major` VALUES ('100002', '网络工程', '0001');
INSERT INTO `major` VALUES ('100003', '大数据分析', '0001');
INSERT INTO `major` VALUES ('100004', '人工智能', '0001');
INSERT INTO `major` VALUES ('100005', '会计学', '0002');
INSERT INTO `major` VALUES ('100006', '旅游管理', '0002');
INSERT INTO `major` VALUES ('100007', '护理学', '0003');
INSERT INTO `major` VALUES ('100008', '药学', '0003');
INSERT INTO `major` VALUES ('100009', '软件工程', '0001');
INSERT INTO `major` VALUES ('100010', '通信工程', '0001');
INSERT INTO `major` VALUES ('100011', '物联网工程', '0001');
INSERT INTO `major` VALUES ('100012', '电子信息', '0001');
INSERT INTO `major` VALUES ('100013', '数据科学与大数据', '0001');
INSERT INTO `major` VALUES ('100014', '自动化', '0001');
INSERT INTO `major` VALUES ('100015', '计算机应用技术', '0001');
INSERT INTO `major` VALUES ('100016', '教育技术学', '0001');
INSERT INTO `major` VALUES ('100017', '数字媒体设计', '0001');
INSERT INTO `major` VALUES ('100018', '市场营销', '0002');
INSERT INTO `major` VALUES ('100019', '工商管理', '0002');
INSERT INTO `major` VALUES ('100020', '农林经济管理', '0002');
INSERT INTO `major` VALUES ('100021', '公共事业管理', '0002');
INSERT INTO `major` VALUES ('100022', '图书管理学', '0002');
INSERT INTO `major` VALUES ('100023', '档案学', '0002');
INSERT INTO `major` VALUES ('100024', '人力资源管理', '0002');
INSERT INTO `major` VALUES ('100025', '经济学', '0002');
INSERT INTO `major` VALUES ('100026', '保险学', '0002');
INSERT INTO `major` VALUES ('100027', '国际经济与贸易', '0002');
INSERT INTO `major` VALUES ('100028', '金融学', '0002');
INSERT INTO `major` VALUES ('100029', '文化事业管理', '0002');
INSERT INTO `major` VALUES ('100030', '基础医学', '0003');
INSERT INTO `major` VALUES ('100031', '生物医学', '0003');
INSERT INTO `major` VALUES ('100032', '精神医学', '0003');
INSERT INTO `major` VALUES ('100033', '临床医学', '0003');
INSERT INTO `major` VALUES ('100034', '中医学', '0003');
INSERT INTO `major` VALUES ('100035', '放射医学', '0003');
INSERT INTO `major` VALUES ('100036', '儿科学', '0003');
INSERT INTO `major` VALUES ('100037', '口腔医学', '0003');

-- ----------------------------
-- Table structure for manager
-- ----------------------------
DROP TABLE IF EXISTS `manager`;
CREATE TABLE `manager` (
  `MANAGER_NO` varchar(8) NOT NULL,
  `MANAGER_NAME` varchar(10) NOT NULL,
  `MANAGER_PASSWORD` text NOT NULL,
  PRIMARY KEY (`MANAGER_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of manager
-- ----------------------------
INSERT INTO `manager` VALUES ('12345678', '管理员', 'pbkdf2:sha256:50000$Kd1BWslr$3235dda29fc6980052b036ccff257c2f62a5653260ecd61225916fd8b2844720');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `STU_NO` varchar(8) NOT NULL,
  `STU_NAME` varchar(10) NOT NULL,
  `STU_SEX` varchar(10) NOT NULL,
  `IN_YEAR` varchar(4) NOT NULL,
  `STU_PASSWORD` text NOT NULL,
  `MAJOR_NO` varchar(16) NOT NULL,
  `COLLEGE_NO` varchar(4) NOT NULL,
  PRIMARY KEY (`STU_NO`),
  KEY `MAJOR_NO` (`MAJOR_NO`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`MAJOR_NO`) REFERENCES `major` (`MAJOR_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('20231001', '小明', '女', '2017', 'pbkdf2:sha256:150000$v2dnkDa2$a614e074187cc7314e872d2e7fb095b120eb4c45b114f946f9e283e5266d98fa', '100001', '0001');
INSERT INTO `student` VALUES ('20231002', '高飞', '男', '2022', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '100010', '0001');
INSERT INTO `student` VALUES ('20231007', '冯佳', '女', '2019', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '100002', '0001');
INSERT INTO `student` VALUES ('20231008', '关乐', '男', '2022', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '100003', '0001');
INSERT INTO `student` VALUES ('20231009', '邓冰清', '女', '2019', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '100001', '0001');
INSERT INTO `student` VALUES ('20231011', '胡晓', '女', '2022', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '100001', '0001');
INSERT INTO `student` VALUES ('20231014', '李瑞乐', '男', '2014', 'pbkdf2:sha256:260000$uucUwg2nm8wkyxbt$e92f88dfb5110f5c1ea8e7d0b1d3ac8ed93f689f1a3cfa1d4f43776bb1c42184', '100023', '0002');

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `TEACHER_NO` varchar(8) NOT NULL,
  `TEACHER_NAME` varchar(10) NOT NULL,
  `TEACHER_SEX` varchar(2) NOT NULL,
  `IN_YEAR` varchar(4) NOT NULL,
  `TEACHER_TITLE` varchar(10) DEFAULT NULL,
  `TEACHER_PASSWORD` text NOT NULL,
  `COLLEGE_NO` varchar(4) NOT NULL,
  PRIMARY KEY (`TEACHER_NO`),
  KEY `COLLEGE_NO` (`COLLEGE_NO`),
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`COLLEGE_NO`) REFERENCES `college` (`COLLEGE_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('30000001', '胡建', '男', '2007', '教师', 'pbkdf2:sha256:260000$cf7Kds20QHiA77iV$29f57d3f9d7e71e3465d2167790a827fa939b138a11bed2894cf05e35e98d4a8', '0001');
INSERT INTO `teacher` VALUES ('30000002', '张丽', '女', '2009', '教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0002');
INSERT INTO `teacher` VALUES ('30000003', '黄文英', '女', '2002', '副教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0003');
INSERT INTO `teacher` VALUES ('30000004', '韩正', '男', '2008', '高级教师', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0001');
INSERT INTO `teacher` VALUES ('30000005', '唐杰飞', '男', '2002', '副教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0002');
INSERT INTO `teacher` VALUES ('30000006', '李导', '男', '2000', '副教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0003');
INSERT INTO `teacher` VALUES ('30000007', '王颖', '女', '2002', '副教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0002');
INSERT INTO `teacher` VALUES ('30000008', '陈平', '女', '2001', '教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0001');
INSERT INTO `teacher` VALUES ('30000009', '胡越', '男', '2005', '特评教师', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0001');
INSERT INTO `teacher` VALUES ('30000010', '陈华', '女', '2004', '高级教师', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0002');
INSERT INTO `teacher` VALUES ('30000011', '张丽', '女', '1999', '副教授', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0003');
INSERT INTO `teacher` VALUES ('30000012', '吴曦', '女', '2001', '教师', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0001');
INSERT INTO `teacher` VALUES ('30000013', '张辉腾', '男', '2003', '教师', 'pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862', '0002');
INSERT INTO `teacher` VALUES ('30000014', '郭婉茹', '女', '2008', '高级教师', 'pbkdf2:sha256:260000$8egThgrKfnDlGAkE$ba7101bec5ad495d46c9516222cf2fb621804b71558859bbd8344a75e613da64', '0002');
INSERT INTO `teacher` VALUES ('30000015', '王虎', '男', '2006', '高级教师', 'pbkdf2:sha256:260000$JRVGfbpLaxRhuPlm$774d0cd3a4d2cd2f841a1a511da3c1490c9bbc7db6be2f99500d2e5ea0c154f5', '0003');
INSERT INTO `teacher` VALUES ('30000016', '松江', '女', '2020', '教师', 'pbkdf2:sha256:150000$bOZdci6L$6f299d934b7f0dfadce480c413f20924c2d07fff6b3e30c8645672ddc11b4e21', '0001');
INSERT INTO `teacher` VALUES ('30000019', '潇潇', '男', '2015', '副教授', 'pbkdf2:sha256:150000$QuUdtUzG$1e41704694a931a6849307537b33761e872730620edf192750b2a68deb0d1df1', '0001');
