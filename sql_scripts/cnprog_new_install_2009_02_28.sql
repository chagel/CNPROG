SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE `activity` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `activity_type` smallint(6) NOT NULL,
  `active_at` datetime NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `is_auditted` tinyint(1) default '0',
  PRIMARY KEY  (`id`),
  KEY `activity_user_id` (`user_id`),
  KEY `activity_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;


CREATE TABLE `answer` (
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
  `comment_count` int(10) unsigned NOT NULL,
  `offensive_flag_count` smallint(6) NOT NULL,
  `last_edited_at` datetime default NULL,
  `last_edited_by_id` int(11) default NULL,
  `html` longtext NOT NULL,
  `vote_up_count` int(11) NOT NULL,
  `vote_down_count` int(11) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;


CREATE TABLE `answer_revision` (
  `id` int(11) NOT NULL auto_increment,
  `answer_id` int(11) NOT NULL,
  `revision` int(10) unsigned NOT NULL,
  `author_id` int(11) NOT NULL,
  `revised_at` datetime NOT NULL,
  `summary` varchar(300) collate utf8_unicode_ci NOT NULL,
  `text` longtext collate utf8_unicode_ci NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `answer_revision_answer_id` (`answer_id`),
  KEY `answer_revision_author_id` (`author_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;


CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_5886d21f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_5886d21f` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_650f49a6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;


CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;


CREATE TABLE `auth_user` (
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


CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f116770` (`group_id`),
  CONSTRAINT `group_id_refs_id_f116770` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_7ceef80f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_dfbab7d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `award` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `badge_id` int(11) NOT NULL,
  `awarded_at` datetime NOT NULL,
  `notified` tinyint(1) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` int(10) default NULL,
  PRIMARY KEY  (`id`),
  KEY `award_user_id` (`user_id`),
  KEY `award_badge_id` (`badge_id`),
  CONSTRAINT `badge_id_refs_id_651af0e1` FOREIGN KEY (`badge_id`) REFERENCES `badge` (`id`),
  CONSTRAINT `user_id_refs_id_2d83e9b6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;


CREATE TABLE `badge` (
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;


CREATE TABLE `comment` (
  `id` int(11) NOT NULL auto_increment,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` varchar(300) NOT NULL,
  `added_at` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `comment_content_type_id` (`content_type_id`),
  KEY `comment_user_id` (`user_id`),
  KEY `content_type_id` (`content_type_id`,`object_id`,`user_id`),
  CONSTRAINT `content_type_id_refs_id_13a5866c` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_6be725e8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;


CREATE TABLE `django_admin_log` (
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


CREATE TABLE `django_authopenid_association` (
  `id` int(11) NOT NULL auto_increment,
  `server_url` longtext NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` longtext NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


CREATE TABLE `django_authopenid_nonce` (
  `id` int(11) NOT NULL auto_increment,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(40) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;


CREATE TABLE `django_authopenid_userassociation` (
  `id` int(11) NOT NULL auto_increment,
  `openid_url` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_163d208d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


CREATE TABLE `django_authopenid_userpasswordqueue` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `new_password` varchar(30) NOT NULL,
  `confirm_key` varchar(40) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_76bcaaa4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;


CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE `favorite_question` (
  `id` int(11) NOT NULL auto_increment,
  `question_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `added_at` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `favorite_question_question_id` (`question_id`),
  KEY `favorite_question_user_id` (`user_id`),
  CONSTRAINT `question_id_refs_id_1ebe1cc3` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `user_id_refs_id_52853822` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


CREATE TABLE `flagged_item` (
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


CREATE TABLE `question` (
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
  `vote_up_count` int(11) NOT NULL,
  `vote_down_count` int(11) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;


CREATE TABLE `question_revision` (
  `id` int(11) NOT NULL auto_increment,
  `question_id` int(11) NOT NULL,
  `revision` int(10) unsigned NOT NULL,
  `title` varchar(300) NOT NULL,
  `author_id` int(11) NOT NULL,
  `revised_at` datetime NOT NULL,
  `tagnames` varchar(125) NOT NULL,
  `summary` varchar(300) NOT NULL,
  `text` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `question_revision_question_id` (`question_id`),
  KEY `question_revision_author_id` (`author_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;


CREATE TABLE `question_tags` (
  `id` int(11) NOT NULL auto_increment,
  `question_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `question_id` (`question_id`,`tag_id`),
  KEY `tag_id_refs_id_43fcb953` (`tag_id`),
  CONSTRAINT `question_id_refs_id_266147c6` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `tag_id_refs_id_43fcb953` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;


CREATE TABLE `repute` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `positive` smallint(6) NOT NULL,
  `negative` smallint(6) NOT NULL,
  `question_id` int(11) NOT NULL,
  `reputed_at` datetime NOT NULL,
  `reputation_type` smallint(6) NOT NULL,
  `reputation` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `repute_user_id` (`user_id`),
  KEY `repute_question_id` (`question_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;


CREATE TABLE `tag` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `used_count` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `tag_created_by_id` (`created_by_id`),
  CONSTRAINT `created_by_id_refs_id_47205d6d` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;


CREATE TABLE `user_badge` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `badge_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `user_favorite_questions` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `user_id` int(10) unsigned NOT NULL,
  `question_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `vote` (
  `id` int(11) NOT NULL auto_increment,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  `vote` smallint(6) NOT NULL,
  `voted_at` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`object_id`,`user_id`),
  KEY `vote_content_type_id` (`content_type_id`),
  KEY `vote_user_id` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_50124414` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_760a4df0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;


SET FOREIGN_KEY_CHECKS = 1;
