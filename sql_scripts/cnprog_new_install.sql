-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.67


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema cnprog
--

CREATE DATABASE IF NOT EXISTS cnprog;
USE cnprog;

--
-- Definition of table `cnprog`.`answer`
--

DROP TABLE IF EXISTS `cnprog`.`answer`;
CREATE TABLE  `cnprog`.`answer` (
  `id` int(11) NOT NULL auto_increment,
  `question_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `added_at` datetime NOT NULL,
  `wiki` tinyint(1) NOT NULL,
  `wikified_at` datetime default NULL,
  `accepted` tinyint(1) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `deleted_by_id` int(11) default NULL,
  `locked` tinyint(1) NOT NULL,
  `locked_by_id` int(11) default NULL,
  `locked_at` datetime default NULL,
  `score` int(11) NOT NULL,
  `vote_up_count` int(11) NOT NULL,
  `vote_down_count` int(11) NOT NULL,
  `comment_count` int(10) unsigned NOT NULL,
  `offensive_flag_count` smallint(6) NOT NULL,
  `last_edited_at` datetime default NULL,
  `last_edited_by_id` int(11) default NULL,
  `html` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `answer_question_id` (`question_id`),
  KEY `answer_author_id` (`author_id`),
  KEY `answer_deleted_by_id` (`deleted_by_id`),
  KEY `answer_locked_by_id` (`locked_by_id`),
  KEY `answer_last_edited_by_id` (`last_edited_by_id`),
  CONSTRAINT `author_id_refs_id_192b0170` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `deleted_by_id_refs_id_192b0170` FOREIGN KEY (`deleted_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `last_edited_by_id_refs_id_192b0170` FOREIGN KEY (`last_edited_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `locked_by_id_refs_id_192b0170` FOREIGN KEY (`locked_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `question_id_refs_id_7d6550c9` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`auth_group`
--

DROP TABLE IF EXISTS `cnprog`.`auth_group`;
CREATE TABLE  `cnprog`.`auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_group`
--

--
-- Definition of table `cnprog`.`auth_group_permissions`
--

DROP TABLE IF EXISTS `cnprog`.`auth_group_permissions`;
CREATE TABLE  `cnprog`.`auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_5886d21f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_5886d21f` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_group_permissions`
--

--
-- Definition of table `cnprog`.`auth_message`
--

DROP TABLE IF EXISTS `cnprog`.`auth_message`;
CREATE TABLE  `cnprog`.`auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_650f49a6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_message`
--

--
-- Definition of table `cnprog`.`auth_permission`
--

DROP TABLE IF EXISTS `cnprog`.`auth_permission`;
CREATE TABLE  `cnprog`.`auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_permission`
--
INSERT INTO `cnprog`.`auth_permission` VALUES  (1,'Can add permission',1,'add_permission'),
 (2,'Can change permission',1,'change_permission'),
 (3,'Can delete permission',1,'delete_permission'),
 (4,'Can add group',2,'add_group'),
 (5,'Can change group',2,'change_group'),
 (6,'Can delete group',2,'delete_group'),
 (7,'Can add user',3,'add_user'),
 (8,'Can change user',3,'change_user'),
 (9,'Can delete user',3,'delete_user'),
 (10,'Can add message',4,'add_message'),
 (11,'Can change message',4,'change_message'),
 (12,'Can delete message',4,'delete_message'),
 (13,'Can add content type',5,'add_contenttype'),
 (14,'Can change content type',5,'change_contenttype'),
 (15,'Can delete content type',5,'delete_contenttype'),
 (16,'Can add session',6,'add_session'),
 (17,'Can change session',6,'change_session'),
 (18,'Can delete session',6,'delete_session'),
 (19,'Can add site',7,'add_site'),
 (20,'Can change site',7,'change_site'),
 (21,'Can delete site',7,'delete_site'),
 (25,'Can add answer',9,'add_answer'),
 (26,'Can change answer',9,'change_answer'),
 (27,'Can delete answer',9,'delete_answer'),
 (28,'Can add comment',10,'add_comment'),
 (29,'Can change comment',10,'change_comment'),
 (30,'Can delete comment',10,'delete_comment'),
 (31,'Can add tag',11,'add_tag'),
 (32,'Can change tag',11,'change_tag'),
 (33,'Can delete tag',11,'delete_tag'),
 (37,'Can add nonce',13,'add_nonce'),
 (38,'Can change nonce',13,'change_nonce'),
 (39,'Can delete nonce',13,'delete_nonce'),
 (40,'Can add association',14,'add_association'),
 (41,'Can change association',14,'change_association'),
 (42,'Can delete association',14,'delete_association'),
 (43,'Can add nonce',15,'add_nonce'),
 (44,'Can change nonce',15,'change_nonce'),
 (45,'Can delete nonce',15,'delete_nonce'),
 (46,'Can add association',16,'add_association'),
 (47,'Can change association',16,'change_association'),
 (48,'Can delete association',16,'delete_association'),
 (49,'Can add user association',17,'add_userassociation'),
 (50,'Can change user association',17,'change_userassociation'),
 (51,'Can delete user association',17,'delete_userassociation'),
 (52,'Can add user password queue',18,'add_userpasswordqueue'),
 (53,'Can change user password queue',18,'change_userpasswordqueue'),
 (54,'Can delete user password queue',18,'delete_userpasswordqueue'),
 (55,'Can add log entry',19,'add_logentry'),
 (56,'Can change log entry',19,'change_logentry'),
 (57,'Can delete log entry',19,'delete_logentry'),
 (58,'Can add question',20,'add_question'),
 (59,'Can change question',20,'change_question'),
 (60,'Can delete question',20,'delete_question'),
 (61,'Can add vote',21,'add_vote'),
 (62,'Can change vote',21,'change_vote'),
 (63,'Can delete vote',21,'delete_vote'),
 (64,'Can add flagged item',22,'add_flaggeditem'),
 (65,'Can change flagged item',22,'change_flaggeditem'),
 (66,'Can delete flagged item',22,'delete_flaggeditem'),
 (67,'Can add favorite question',23,'add_favoritequestion'),
 (68,'Can change favorite question',23,'change_favoritequestion'),
 (69,'Can delete favorite question',23,'delete_favoritequestion'),
 (70,'Can add badge',24,'add_badge'),
 (71,'Can change badge',24,'change_badge'),
 (72,'Can delete badge',24,'delete_badge'),
 (73,'Can add award',25,'add_award'),
 (74,'Can change award',25,'change_award'),
 (75,'Can delete award',25,'delete_award');

--
-- Definition of table `cnprog`.`auth_user`
--

DROP TABLE IF EXISTS `cnprog`.`auth_user`;
CREATE TABLE  `cnprog`.`auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  `gold` smallint(6) NOT NULL default '0',
  `silver` smallint(5) unsigned NOT NULL default '0',
  `bronze` smallint(5) unsigned NOT NULL default '0',
  `reputation` int(10) unsigned default '1',
  `gravatar` varchar(128) default NULL,
  `questions_per_page` smallint(5) unsigned default '10',
  `last_seen` datetime default NULL,
  `real_name` varchar(100) default NULL,
  `website` varchar(200) default NULL,
  `location` varchar(100) default NULL,
  `date_of_birth` datetime default NULL,
  `about` text,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_user`
--
INSERT INTO `cnprog`.`auth_user` VALUES  (2,'chagel','','','chagel@gmail.com','sha1$6a2fb$0d2ffe90bcba542fc962f57967a88e507799cc74',1,1,1,'2008-12-16 15:35:17','2008-12-11 20:12:53',0,0,0,1,'8c1efc4f4618aa68b18c88f2bcaa5564',10,NULL,NULL,NULL,NULL,NULL,NULL),
 (3,'mike','','','ichagel@yahoo.com','sha1$f7ef5$1015ae6b2c8a2774a028419d3c57e13145b83284',0,1,0,'2008-12-15 12:56:23','2008-12-15 12:56:23',0,0,0,1,NULL,10,NULL,NULL,NULL,NULL,NULL,NULL),
 (4,'sailingcai','','','sailingcai@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-23 06:14:45','2008-12-20 15:19:21',1,2,3,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','',NULL,''),
 (5,'sailingcai1','','','1@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21',NULL,NULL,NULL,NULL,NULL),
 (6,'sailing2','','','2@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (7,'sailing3','','','3@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (8,'sailing4','','','4@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (9,'sailing5','','','5@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (10,'sailing6','','','6@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (11,'sailing7','','','7@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (12,'sailing8','','','8@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (13,'sailing9','','','9@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (14,'sailing10','','','10@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (15,'sailing11','','','11@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (16,'sailing12','','','12@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (17,'sailing13','','','13@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (18,'sailing14','','','14@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (19,'sailing15','','','15@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (20,'sailing16','','','16@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (21,'sailing17','','','17@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (22,'sailing18','','','18@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (23,'sailing19','','','19@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (24,'sailing20','','','20@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (25,'sailing21','','','21@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (26,'sailing22','','','22@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (27,'sailing23','','','23@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (28,'sailing24','','','24@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (29,'sailing25','','','25@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (30,'sailing26','','','26@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (31,'sailing27','','','27@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (32,'sailing28','','','28@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (33,'sailing29','','','29@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (34,'sailing30','','','30@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (35,'sailing31','','','31@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (36,'sailing32','','','32@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (37,'sailing33','','','33@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (38,'sailing34','','','34@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (39,'sailing35','','','35@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (40,'sailing36','','','36@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (41,'sailing37','','','37@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (42,'sailing38','','','38@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (43,'sailing39','','','39@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (44,'sailing40','','','40@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (45,'sailing41','','','41@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (46,'sailing42','','','42@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (47,'sailing43','','','43@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (48,'sailing44','','','44@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (49,'sailing45','','','45@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (50,'sailing46','','','46@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (51,'sailing47','','','47@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (52,'sailing48','','','48@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (53,'sailing49','','','49@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (54,'sailing50','','','50@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (55,'sailing51','','','51@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (56,'sailing52','','','52@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (57,'sailing53','','','53@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (58,'sailing54','','','54@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (59,'sailing55','','','55@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (60,'sailing56','','','56@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (61,'sailing57','','','57@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (62,'sailing58','','','58@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (63,'sailing59','','','59@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (64,'sailing60','','','60@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (65,'sailing61','','','61@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (66,'sailing62','','','62@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (67,'sailing63','','','63@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (68,'sailing64','','','64@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (69,'sailing65','','','65@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (70,'sailing66','','','66@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (71,'sailing67','','','67@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (72,'sailing68','','','68@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (73,'sailing69','','','69@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (74,'sailing70','','','70@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (75,'sailing71','','','71@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (76,'sailing72','','','72@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (77,'sailing73','','','73@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (78,'sailing74','','','74@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (79,'sailing75','','','75@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (80,'sailing76','','','76@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (81,'sailing77','','','77@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (82,'sailing78','','','78@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (83,'sailing79','','','79@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (84,'sailing80','','','80@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (85,'sailing81','','','81@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (86,'sailing82','','','82@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (87,'sailing83','','','83@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (88,'sailing84','','','84@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (89,'sailing85','','','85@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (90,'sailing86','','','86@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (91,'sailing87','','','87@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (92,'sailing88','','','88@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (93,'sailing89','','','89@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (94,'sailing90','','','90@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (95,'sailing91','','','91@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (96,'sailing92','','','92@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (97,'sailing93','','','93@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (98,'sailing94','','','94@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (99,'sailing95','','','95@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (100,'sailing96','','','96@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (101,'sailing97','','','97@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (102,'sailing98','','','98@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00',''),
 (103,'sailing99','','','99@gmail.com','sha1$a417c$ca7d9f2ad55666bf98068cc392b6f62450b216e0',0,1,0,'2008-12-20 15:19:21','2008-12-20 15:19:21',0,0,0,1,'a1cb9864605a32760518b90a4f9a0e73',10,'2008-12-20 15:19:21','','','','0000-00-00 00:00:00','');

--
-- Definition of table `cnprog`.`auth_user_groups`
--

DROP TABLE IF EXISTS `cnprog`.`auth_user_groups`;
CREATE TABLE  `cnprog`.`auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f116770` (`group_id`),
  CONSTRAINT `group_id_refs_id_f116770` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_7ceef80f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_user_groups`
--

--
-- Definition of table `cnprog`.`auth_user_user_permissions`
--

DROP TABLE IF EXISTS `cnprog`.`auth_user_user_permissions`;
CREATE TABLE  `cnprog`.`auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_dfbab7d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`auth_user_user_permissions`
--

--
-- Definition of table `cnprog`.`award`
--

DROP TABLE IF EXISTS `cnprog`.`award`;
CREATE TABLE  `cnprog`.`award` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `badge_id` int(11) NOT NULL,
  `awarded_at` datetime NOT NULL,
  `notified` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `award_user_id` (`user_id`),
  KEY `award_badge_id` (`badge_id`),
  CONSTRAINT `badge_id_refs_id_651af0e1` FOREIGN KEY (`badge_id`) REFERENCES `badge` (`id`),
  CONSTRAINT `user_id_refs_id_2d83e9b6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`award`
--

--
-- Definition of table `cnprog`.`badge`
--

DROP TABLE IF EXISTS `cnprog`.`badge`;
CREATE TABLE  `cnprog`.`badge` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `type` smallint(6) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` varchar(300) NOT NULL,
  `multiple` tinyint(1) NOT NULL,
  `awarded_count` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`,`type`),
  KEY `badge_slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`badge`
--

--
-- Definition of table `cnprog`.`comment`
--

DROP TABLE IF EXISTS `cnprog`.`comment`;
CREATE TABLE  `cnprog`.`comment` (
  `id` int(11) NOT NULL auto_increment,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` varchar(300) NOT NULL,
  `added_at` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `content_type_id` (`content_type_id`,`object_id`,`user_id`),
  KEY `comment_content_type_id` (`content_type_id`),
  KEY `comment_user_id` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_13a5866c` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_6be725e8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`comment`
--

--
-- Definition of table `cnprog`.`django_admin_log`
--

DROP TABLE IF EXISTS `cnprog`.`django_admin_log`;
CREATE TABLE  `cnprog`.`django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`django_admin_log`
--
INSERT INTO `cnprog`.`django_admin_log` VALUES  (1,'2008-12-18 23:41:41',2,7,'1','cnprog.com',2,'已修改 domain 和 name 。');

--
-- Definition of table `cnprog`.`django_authopenid_association`
--

DROP TABLE IF EXISTS `cnprog`.`django_authopenid_association`;
CREATE TABLE  `cnprog`.`django_authopenid_association` (
  `id` int(11) NOT NULL auto_increment,
  `server_url` longtext NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` longtext NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`django_authopenid_association`
--
INSERT INTO `cnprog`.`django_authopenid_association` VALUES  (2,'https://www.google.com/accounts/o8/ud','AOQobUfcCH4sgjsBGGscrzxIa5UM4clofAB6nixx8Qq_NWco4ynn_Kc4','u5cva43abzdwF8CJOFZfkzfk7x8=\n',1229022261,1229022261,'HMAC-SHA1'),
 (3,'https://api.screenname.aol.com/auth/openidServer','diAyLjAgayAwIGJhT2VvYkdDZ21RSHJ4QldzQnhTdjIxV3BVbz0%3D-j5HRXRB1VbPyg48jGKE1Q70dfv76lGHEPwd9071%2FJ7f6SSw5YhakrwWpsVXtr34T6iHwPDdo6RU%3D','EmQL3+5oR6mFKIaeBNy6hXyUJ/w=\n',1229282202,1229282202,'HMAC-SHA1'),
 (4,'https://open.login.yahooapis.com/openid/op/auth','JcBeY.uWXu2YjzbuCQiqFzAb0MIc7ATeKiPO4eAp3vluPMqZp_NCxepvMLGrJjxxDKTaNnr06wepMos8ap6SQYZiTi51tZ05lMWnpZAiOA1hsq_WMlEL7G9YE66GEA9A','QXiuN6B7E8nP5QhyHI3IB26t4SA=\n',1229282256,1229282256,'HMAC-SHA1'),
 (5,'http://openid.claimid.com/server','{HMAC-SHA1}{494575fd}{uLEbxQ==}','GvPbkgMHh0QVPH7mStCGuWb2AKY=\n',1229288957,1229288957,'HMAC-SHA1'),
 (6,'http://www.blogger.com/openid-server.g','oida-1229424484019-158830626','8gaU4aKnIFCLKIkHdxZQp7ZGNck=\n',1229424478,1229424478,'HMAC-SHA1');

--
-- Definition of table `cnprog`.`django_authopenid_nonce`
--

DROP TABLE IF EXISTS `cnprog`.`django_authopenid_nonce`;
CREATE TABLE  `cnprog`.`django_authopenid_nonce` (
  `id` int(11) NOT NULL auto_increment,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(40) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`django_authopenid_userassociation`
--

DROP TABLE IF EXISTS `cnprog`.`django_authopenid_userassociation`;
CREATE TABLE  `cnprog`.`django_authopenid_userassociation` (
  `id` int(11) NOT NULL auto_increment,
  `openid_url` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_163d208d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`django_authopenid_userassociation`
--
INSERT INTO `cnprog`.`django_authopenid_userassociation` VALUES  (2,'https://www.google.com/accounts/o8/id?id=AItOawl7CVVHl4DWtteqj4dd_A23zKRwPZgOOjw',2),
 (3,'https://me.yahoo.com/a/f8f2zXF91okYL4iN2Zh4P542a5s-#f4af2',3),
 (4,'https://me.yahoo.com/sailingcai#6fa4e',4);

--
-- Definition of table `cnprog`.`django_authopenid_userpasswordqueue`
--

DROP TABLE IF EXISTS `cnprog`.`django_authopenid_userpasswordqueue`;
CREATE TABLE  `cnprog`.`django_authopenid_userpasswordqueue` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `new_password` varchar(30) NOT NULL,
  `confirm_key` varchar(40) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_76bcaaa4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`django_authopenid_userpasswordqueue`
--

--
-- Definition of table `cnprog`.`django_content_type`
--

DROP TABLE IF EXISTS `cnprog`.`django_content_type`;
CREATE TABLE  `cnprog`.`django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`django_content_type`
--
INSERT INTO `cnprog`.`django_content_type` VALUES  (1,'permission','auth','permission'),
 (2,'group','auth','group'),
 (3,'user','auth','user'),
 (4,'message','auth','message'),
 (5,'content type','contenttypes','contenttype'),
 (6,'session','sessions','session'),
 (7,'site','sites','site'),
 (9,'answer','forum','answer'),
 (10,'comment','forum','comment'),
 (11,'tag','forum','tag'),
 (13,'nonce','django_openidconsumer','nonce'),
 (14,'association','django_openidconsumer','association'),
 (15,'nonce','django_authopenid','nonce'),
 (16,'association','django_authopenid','association'),
 (17,'user association','django_authopenid','userassociation'),
 (18,'user password queue','django_authopenid','userpasswordqueue'),
 (19,'log entry','admin','logentry'),
 (20,'question','forum','question'),
 (21,'vote','forum','vote'),
 (22,'flagged item','forum','flaggeditem'),
 (23,'favorite question','forum','favoritequestion'),
 (24,'badge','forum','badge'),
 (25,'award','forum','award');

--
-- Definition of table `cnprog`.`django_session`
--

DROP TABLE IF EXISTS `cnprog`.`django_session`;
CREATE TABLE  `cnprog`.`django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`django_site`
--

DROP TABLE IF EXISTS `cnprog`.`django_site`;
CREATE TABLE  `cnprog`.`django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`django_site`
--
INSERT INTO `cnprog`.`django_site` VALUES  (1,'cnprog.com','CNProg.com');

--
-- Definition of table `cnprog`.`favorite_question`
--

DROP TABLE IF EXISTS `cnprog`.`favorite_question`;
CREATE TABLE  `cnprog`.`favorite_question` (
  `id` int(11) NOT NULL auto_increment,
  `question_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `added_at` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `favorite_question_question_id` (`question_id`),
  KEY `favorite_question_user_id` (`user_id`),
  CONSTRAINT `question_id_refs_id_1ebe1cc3` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `user_id_refs_id_52853822` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`favorite_question`
--

--
-- Definition of table `cnprog`.`flagged_item`
--

DROP TABLE IF EXISTS `cnprog`.`flagged_item`;
CREATE TABLE  `cnprog`.`flagged_item` (
  `id` int(11) NOT NULL auto_increment,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  `flagged_at` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`object_id`,`user_id`),
  KEY `flagged_item_content_type_id` (`content_type_id`),
  KEY `flagged_item_user_id` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_76e44d74` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_35e3c608` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`flagged_item`
--

--
-- Definition of table `cnprog`.`question`
--

DROP TABLE IF EXISTS `cnprog`.`question`;
CREATE TABLE  `cnprog`.`question` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(300) NOT NULL,
  `author_id` int(11) NOT NULL,
  `added_at` datetime NOT NULL,
  `wiki` tinyint(1) NOT NULL,
  `wikified_at` datetime default NULL,
  `answer_accepted` tinyint(1) NOT NULL,
  `closed` tinyint(1) NOT NULL,
  `closed_by_id` int(11) default NULL,
  `closed_at` datetime default NULL,
  `close_reason` smallint(6) default NULL,
  `deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime default NULL,
  `deleted_by_id` int(11) default NULL,
  `locked` tinyint(1) NOT NULL,
  `locked_by_id` int(11) default NULL,
  `locked_at` datetime default NULL,
  `vote_up_count` int(11) NOT NULL,
  `vote_down_count` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `answer_count` int(10) unsigned NOT NULL,
  `comment_count` int(10) unsigned NOT NULL,
  `view_count` int(10) unsigned NOT NULL,
  `offensive_flag_count` smallint(6) NOT NULL,
  `favourite_count` int(10) unsigned NOT NULL,
  `last_edited_at` datetime default NULL,
  `last_edited_by_id` int(11) default NULL,
  `last_activity_at` datetime NOT NULL,
  `last_activity_by_id` int(11) NOT NULL,
  `tagnames` varchar(125) NOT NULL,
  `summary` varchar(180) NOT NULL,
  `html` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `question_author_id` (`author_id`),
  KEY `question_closed_by_id` (`closed_by_id`),
  KEY `question_deleted_by_id` (`deleted_by_id`),
  KEY `question_locked_by_id` (`locked_by_id`),
  KEY `question_last_edited_by_id` (`last_edited_by_id`),
  KEY `question_last_activity_by_id` (`last_activity_by_id`),
  CONSTRAINT `author_id_refs_id_56e9d00c` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `closed_by_id_refs_id_56e9d00c` FOREIGN KEY (`closed_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `deleted_by_id_refs_id_56e9d00c` FOREIGN KEY (`deleted_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `last_activity_by_id_refs_id_56e9d00c` FOREIGN KEY (`last_activity_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `last_edited_by_id_refs_id_56e9d00c` FOREIGN KEY (`last_edited_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `locked_by_id_refs_id_56e9d00c` FOREIGN KEY (`locked_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`question_tags`
--

DROP TABLE IF EXISTS `cnprog`.`question_tags`;
CREATE TABLE  `cnprog`.`question_tags` (
  `id` int(11) NOT NULL auto_increment,
  `question_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `question_id` (`question_id`,`tag_id`),
  KEY `tag_id_refs_id_43fcb953` (`tag_id`),
  CONSTRAINT `question_id_refs_id_266147c6` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `tag_id_refs_id_43fcb953` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`tag`
--

DROP TABLE IF EXISTS `cnprog`.`tag`;
CREATE TABLE  `cnprog`.`tag` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `used_count` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `tag_created_by_id` (`created_by_id`),
  CONSTRAINT `created_by_id_refs_id_47205d6d` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`user_badge`
--

DROP TABLE IF EXISTS `cnprog`.`user_badge`;
CREATE TABLE  `cnprog`.`user_badge` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `badge_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Definition of table `cnprog`.`user_favorite_questions`
--

DROP TABLE IF EXISTS `cnprog`.`user_favorite_questions`;
CREATE TABLE  `cnprog`.`user_favorite_questions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `question_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`user_favorite_questions`
--

DROP TABLE IF EXISTS `cnprog`.`vote`;
CREATE TABLE  `cnprog`.`vote` (
  `id` int(11) NOT NULL auto_increment,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  `vote` smallint(6) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`object_id`,`user_id`),
  KEY `vote_content_type_id` (`content_type_id`),
  KEY `vote_user_id` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_50124414` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_760a4df0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cnprog`.`vote`
--



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
