/*
 Navicat MySQL Data Transfer

 Source Server         : ketof
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : student_management_system

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 05/05/2024 22:15:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('a3efe66ecfa4');

-- ----------------------------
-- Table structure for college
-- ----------------------------
DROP TABLE IF EXISTS `college`;
CREATE TABLE `college`  (
  `COLLEGE_NO` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COLLEGE_NAME` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`COLLEGE_NO`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
CREATE TABLE `course`  (
  `COURSE_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COURSE_NAME` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COURSE_CREDIT` int NOT NULL,
  `COURSE_HOUR` int NOT NULL,
  `COLLEGE_NO` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TEAC_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '教师对应id',
  PRIMARY KEY (`COURSE_NO`) USING BTREE,
  INDEX `COLLEGE_NO`(`COLLEGE_NO`) USING BTREE,
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`COLLEGE_NO`) REFERENCES `college` (`COLLEGE_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('10000001', '高等数学', 4, 48, '0001', NULL);
INSERT INTO `course` VALUES ('10000002', '审计学', 3, 45, '0002', '30000002');
INSERT INTO `course` VALUES ('10000003', '数据库设计', 3, 45, '0001', '30000001');
INSERT INTO `course` VALUES ('10000004', '线性代数', 4, 48, '0001', '30000004');
INSERT INTO `course` VALUES ('10000005', '病理学', 4, 48, '0003', '30000001');
INSERT INTO `course` VALUES ('10000006', 'python', 3, 45, '0001', '30000001');
INSERT INTO `course` VALUES ('10000007', '旅游管理理论', 3, 35, '0002', '30000005');
INSERT INTO `course` VALUES ('10000008', '商法', 3, 23, '0002', '30000003');
INSERT INTO `course` VALUES ('10000009', '财务共享', 3, 48, '0002', NULL);
INSERT INTO `course` VALUES ('10000010', 'C语言', 3, 45, '0001', '30000001');
INSERT INTO `course` VALUES ('10000011', '企业行为模拟', 2, 23, '0002', '30000002');
INSERT INTO `course` VALUES ('10000012', '数据结构', 4, 45, '0001', NULL);
INSERT INTO `course` VALUES ('10000013', '流行病学', 4, 48, '0003', NULL);
INSERT INTO `course` VALUES ('10000014', '数据库原理', 3, 43, '0001', '30000004');
INSERT INTO `course` VALUES ('10000015', 'Java', 4, 45, '0001', NULL);
INSERT INTO `course` VALUES ('10000016', '计算机网络', 3, 45, '0001', '30000001');
INSERT INTO `course` VALUES ('10000017', '计算机组成原理', 4, 45, '0008', '30000001');
INSERT INTO `course` VALUES ('10000018', '多媒体技术与应用', 4, 48, '0001', NULL);
INSERT INTO `course` VALUES ('10000019', '电子技术', 4, 45, '0001', NULL);
INSERT INTO `course` VALUES ('10000020', '微机系统', 4, 48, '0001', '30000004');
INSERT INTO `course` VALUES ('10000021', '管理学原理', 3, 38, '0002', '30000002');
INSERT INTO `course` VALUES ('10000022', '营销学原理', 3, 43, '0002', '30000001');
INSERT INTO `course` VALUES ('10000023', '财务管理', 3, 45, '0002', NULL);
INSERT INTO `course` VALUES ('10000024', '人力资源管理', 3, 45, '0002', NULL);
INSERT INTO `course` VALUES ('10000025', '商务统计', 3, 35, '0002', NULL);
INSERT INTO `course` VALUES ('10000026', '诊断学', 4, 45, '0003', '30000003');
INSERT INTO `course` VALUES ('10000027', '无机化学', 4, 48, '0003', NULL);
INSERT INTO `course` VALUES ('10000028', '医学检验', 3, 35, '0003', '30000001');
INSERT INTO `course` VALUES ('10000029', '内科学', 4, 48, '0003', NULL);
INSERT INTO `course` VALUES ('10000030', '妇产科学', 4, 48, '0003', '30000003');
INSERT INTO `course` VALUES ('10000031', '经济贸易', 4, 45, '0009', '');

-- ----------------------------
-- Table structure for course_select_table
-- ----------------------------
DROP TABLE IF EXISTS `course_select_table`;
CREATE TABLE `course_select_table`  (
  `STU_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TEACHER_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COURSE_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `GRADE` int NULL DEFAULT NULL,
  PRIMARY KEY (`STU_NO`, `TEACHER_NO`, `COURSE_NO`) USING BTREE,
  INDEX `COURSE_NO`(`COURSE_NO`) USING BTREE,
  INDEX `TEACHER_NO`(`TEACHER_NO`) USING BTREE,
  CONSTRAINT `course_select_table_ibfk_1` FOREIGN KEY (`COURSE_NO`) REFERENCES `course` (`COURSE_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `course_select_table_ibfk_2` FOREIGN KEY (`STU_NO`) REFERENCES `student` (`STU_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `course_select_table_ibfk_3` FOREIGN KEY (`TEACHER_NO`) REFERENCES `teacher` (`TEACHER_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_select_table
-- ----------------------------
INSERT INTO `course_select_table` VALUES ('20231001', '30000001', '10000003', 95);
INSERT INTO `course_select_table` VALUES ('20231001', '30000001', '10000006', 66);
INSERT INTO `course_select_table` VALUES ('20231001', '30000001', '10000022', NULL);
INSERT INTO `course_select_table` VALUES ('20231001', '30000001', '10000028', NULL);
INSERT INTO `course_select_table` VALUES ('20231001', '30000002', '10000002', NULL);
INSERT INTO `course_select_table` VALUES ('20231001', '30000003', '10000008', NULL);
INSERT INTO `course_select_table` VALUES ('20231002', '30000002', '10000002', 77);

-- ----------------------------
-- Table structure for course_teacher
-- ----------------------------
DROP TABLE IF EXISTS `course_teacher`;
CREATE TABLE `course_teacher`  (
  `TEACHER_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COURSE_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COURSE_CAPACITY` int NOT NULL,
  PRIMARY KEY (`TEACHER_NO`, `COURSE_NO`) USING BTREE,
  INDEX `COURSE_NO`(`COURSE_NO`) USING BTREE,
  CONSTRAINT `course_teacher_ibfk_1` FOREIGN KEY (`COURSE_NO`) REFERENCES `course` (`COURSE_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `course_teacher_ibfk_2` FOREIGN KEY (`TEACHER_NO`) REFERENCES `teacher` (`TEACHER_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_teacher
-- ----------------------------
INSERT INTO `course_teacher` VALUES ('30000001', '10000003', 90);
INSERT INTO `course_teacher` VALUES ('30000001', '10000005', 34);
INSERT INTO `course_teacher` VALUES ('30000001', '10000006', 12);
INSERT INTO `course_teacher` VALUES ('30000001', '10000007', 66);
INSERT INTO `course_teacher` VALUES ('30000001', '10000010', 11);
INSERT INTO `course_teacher` VALUES ('30000001', '10000016', 57);
INSERT INTO `course_teacher` VALUES ('30000001', '10000017', 34);
INSERT INTO `course_teacher` VALUES ('30000001', '10000022', 87);
INSERT INTO `course_teacher` VALUES ('30000001', '10000027', 33);
INSERT INTO `course_teacher` VALUES ('30000001', '10000028', 43);
INSERT INTO `course_teacher` VALUES ('30000002', '10000002', 45);
INSERT INTO `course_teacher` VALUES ('30000002', '10000011', 47);
INSERT INTO `course_teacher` VALUES ('30000002', '10000021', 68);
INSERT INTO `course_teacher` VALUES ('30000002', '10000030', 30);
INSERT INTO `course_teacher` VALUES ('30000003', '10000008', 65);
INSERT INTO `course_teacher` VALUES ('30000003', '10000026', 49);
INSERT INTO `course_teacher` VALUES ('30000003', '10000029', 43);
INSERT INTO `course_teacher` VALUES ('30000004', '10000004', 20);
INSERT INTO `course_teacher` VALUES ('30000004', '10000014', 9);
INSERT INTO `course_teacher` VALUES ('30000004', '10000020', 42);
INSERT INTO `course_teacher` VALUES ('30000005', '10000007', 0);
INSERT INTO `course_teacher` VALUES ('30000005', '10000022', 87);
INSERT INTO `course_teacher` VALUES ('30000007', '10000001', 40);
INSERT INTO `course_teacher` VALUES ('30000007', '10000023', 78);
INSERT INTO `course_teacher` VALUES ('30000008', '10000013', 45);
INSERT INTO `course_teacher` VALUES ('30000008', '10000015', 42);
INSERT INTO `course_teacher` VALUES ('30000010', '10000009', 9);
INSERT INTO `course_teacher` VALUES ('30000010', '10000024', 20);
INSERT INTO `course_teacher` VALUES ('30000011', '10000014', 55);
INSERT INTO `course_teacher` VALUES ('30000011', '10000028', 43);
INSERT INTO `course_teacher` VALUES ('30000012', '10000012', 3);
INSERT INTO `course_teacher` VALUES ('30000012', '10000018', 0);
INSERT INTO `course_teacher` VALUES ('30000012', '10000019', 58);
INSERT INTO `course_teacher` VALUES ('30000012', '10000031', 30);
INSERT INTO `course_teacher` VALUES ('30000013', '10000025', 67);

-- ----------------------------
-- Table structure for major
-- ----------------------------
DROP TABLE IF EXISTS `major`;
CREATE TABLE `major`  (
  `MAJOR_NO` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MAJOR_NAME` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COLLEGE_NO` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`MAJOR_NO`) USING BTREE,
  INDEX `COLLEGE_NO`(`COLLEGE_NO`) USING BTREE,
  CONSTRAINT `major_ibfk_1` FOREIGN KEY (`COLLEGE_NO`) REFERENCES `college` (`COLLEGE_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
CREATE TABLE `manager`  (
  `MANAGER_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MANAGER_NAME` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MANAGER_PASSWORD` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`MANAGER_NO`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of manager
-- ----------------------------
INSERT INTO `manager` VALUES ('12345678', '管理员', 'admin');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `STU_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `STU_NAME` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `STU_SEX` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IN_YEAR` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `STU_PASSWORD` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MAJOR_NO` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COLLEGE_NO` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`STU_NO`) USING BTREE,
  INDEX `MAJOR_NO`(`MAJOR_NO`) USING BTREE,
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`MAJOR_NO`) REFERENCES `major` (`MAJOR_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('12222222', 'ax', '女', '2022', '48576772', '100001', '0001');
INSERT INTO `student` VALUES ('20201061', '小花花', '女', '2016', '123', '100001', '0001');
INSERT INTO `student` VALUES ('20231001', '刘莉莉', '女', '2020', '123', '100001', '0001');
INSERT INTO `student` VALUES ('20231002', '花朵度', '男', '2024', '123', '100001', '0001');
INSERT INTO `student` VALUES ('20231007', '冯佳家', '女', '2019', '123', '100001', '0001');
INSERT INTO `student` VALUES ('20231008', '关乐', '男', '2022', '123', '100003', '0001');
INSERT INTO `student` VALUES ('20231009', '邓冰清', '女', '2019', '123', '100001', '0001');
INSERT INTO `student` VALUES ('20231011', '胡晓', '女', '2022', '123', '100001', '0001');
INSERT INTO `student` VALUES ('20231014', '李瑞乐', '男', '2014', '123', '100023', '0002');
INSERT INTO `student` VALUES ('22010678', '测试用户一', '男', '2013', '123', '100001', '0001');

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `TEACHER_NO` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TEACHER_NAME` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TEACHER_SEX` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IN_YEAR` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TEACHER_TITLE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `TEACHER_PASSWORD` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `COLLEGE_NO` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`TEACHER_NO`) USING BTREE,
  INDEX `COLLEGE_NO`(`COLLEGE_NO`) USING BTREE,
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`COLLEGE_NO`) REFERENCES `college` (`COLLEGE_NO`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('30000001', '小大锤', '男', '2015', '教师', '123456', '0001');
INSERT INTO `teacher` VALUES ('30000002', '张丽', '女', '2009', '教授', '123456', '0002');
INSERT INTO `teacher` VALUES ('30000003', '黄文英', '女', '2002', '副教授', '123456', '0003');
INSERT INTO `teacher` VALUES ('30000004', '韩正非', '男', '2008', '高级教师', '123456', '0001');
INSERT INTO `teacher` VALUES ('30000005', '唐杰飞', '男', '2002', '副教授', '123456', '0002');
INSERT INTO `teacher` VALUES ('30000007', '王颖', '女', '2002', '副教授', '123456', '0002');
INSERT INTO `teacher` VALUES ('30000008', '陈平', '女', '2001', '教授', '123456', '0001');
INSERT INTO `teacher` VALUES ('30000009', '胡越', '男', '2005', '特评教师', '123456', '0001');
INSERT INTO `teacher` VALUES ('30000010', '陈华', '女', '2004', '高级教师', '123456', '0002');
INSERT INTO `teacher` VALUES ('30000011', '张丽', '女', '1999', '副教授', '123456', '0003');
INSERT INTO `teacher` VALUES ('30000012', '吴曦', '女', '2001', '教师', '123456', '0001');
INSERT INTO `teacher` VALUES ('30000013', '张辉腾', '男', '2003', '教师', '123456', '0002');
INSERT INTO `teacher` VALUES ('30000014', '郭婉茹', '女', '2008', '高级教师', '123456', '0002');
INSERT INTO `teacher` VALUES ('30000015', '王虎', '男', '2006', '高级教师', '123456', '0003');
INSERT INTO `teacher` VALUES ('30000016', '松江', '女', '2020', '教师', '123456', '0001');
INSERT INTO `teacher` VALUES ('30000019', '潇潇', '男', '2015', '副教授', '123456', '0001');

SET FOREIGN_KEY_CHECKS = 1;
