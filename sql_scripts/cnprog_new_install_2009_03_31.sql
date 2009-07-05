USE cnprog;


/************ Update: Tables ***************/

/******************** Add Table: activity ************************/

/* Build Table Structure */
CREATE TABLE activity
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	activity_type SMALLINT NOT NULL,
	active_at DATETIME NOT NULL,
	content_type_id INTEGER NOT NULL,
	object_id INTEGER UNSIGNED NOT NULL,
	is_auditted TINYINT NULL DEFAULT 0
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=latin1;

/* Table Items: activity */

/* Add Indexes for: activity */
CREATE INDEX activity_content_type_id ON activity (content_type_id);
CREATE INDEX activity_user_id ON activity (user_id);

/******************** Add Table: answer ************************/

/* Build Table Structure */
CREATE TABLE answer
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	question_id INTEGER NOT NULL,
	author_id INTEGER NOT NULL,
	added_at DATETIME NOT NULL,
	wiki TINYINT NOT NULL,
	wikified_at DATETIME NULL,
	accepted TINYINT NOT NULL,
	deleted TINYINT NOT NULL,
	deleted_by_id INTEGER NULL,
	locked TINYINT NOT NULL,
	locked_by_id INTEGER NULL,
	locked_at DATETIME NULL,
	score INTEGER NOT NULL,
	comment_count INTEGER UNSIGNED NOT NULL,
	offensive_flag_count SMALLINT NOT NULL,
	last_edited_at DATETIME NULL,
	last_edited_by_id INTEGER NULL,
	html LONGTEXT NOT NULL,
	vote_up_count INTEGER NOT NULL,
	vote_down_count INTEGER NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;

/* Table Items: answer */

/* Add Indexes for: answer */
CREATE INDEX answer_author_id ON answer (author_id);
CREATE INDEX answer_deleted_by_id ON answer (deleted_by_id);
CREATE INDEX answer_last_edited_by_id ON answer (last_edited_by_id);
CREATE INDEX answer_locked_by_id ON answer (locked_by_id);
CREATE INDEX answer_question_id ON answer (question_id);

/******************** Add Table: answer_revision ************************/

/* Build Table Structure */
CREATE TABLE answer_revision
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	answer_id INTEGER NOT NULL,
	revision INTEGER UNSIGNED NOT NULL,
	author_id INTEGER NOT NULL,
	revised_at DATETIME NOT NULL,
	summary TEXT NOT NULL,
	`text` LONGTEXT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* Table Items: answer_revision */

/* Add Indexes for: answer_revision */
CREATE INDEX answer_revision_answer_id ON answer_revision (answer_id);
CREATE INDEX answer_revision_author_id ON answer_revision (author_id);

/******************** Add Table: auth_group ************************/

/* Build Table Structure */
CREATE TABLE auth_group
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: auth_group */

/* Add Indexes for: auth_group */
CREATE UNIQUE INDEX name ON auth_group (name);

/******************** Add Table: auth_group_permissions ************************/

/* Build Table Structure */
CREATE TABLE auth_group_permissions
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	group_id INTEGER NOT NULL,
	permission_id INTEGER NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: auth_group_permissions */

/* Add Indexes for: auth_group_permissions */
CREATE UNIQUE INDEX group_id ON auth_group_permissions (group_id, permission_id);
CREATE INDEX permission_id_refs_id_5886d21f ON auth_group_permissions (permission_id);

/******************** Add Table: auth_message ************************/

/* Build Table Structure */
CREATE TABLE auth_message
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	message LONGTEXT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

/* Table Items: auth_message */

/* Add Indexes for: auth_message */
CREATE INDEX auth_message_user_id ON auth_message (user_id);

/******************** Add Table: auth_permission ************************/

/* Build Table Structure */
CREATE TABLE auth_permission
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	content_type_id INTEGER NOT NULL,
	codename VARCHAR(100) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;

/* Table Items: auth_permission */

/* Add Indexes for: auth_permission */
CREATE INDEX auth_permission_content_type_id ON auth_permission (content_type_id);
CREATE UNIQUE INDEX content_type_id ON auth_permission (content_type_id, codename);

/******************** Add Table: auth_user ************************/

/* Build Table Structure */
CREATE TABLE auth_user
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(30) NOT NULL,
	first_name VARCHAR(30) NOT NULL,
	last_name VARCHAR(30) NOT NULL,
	email VARCHAR(75) NOT NULL,
	password VARCHAR(128) NOT NULL,
	is_staff TINYINT NOT NULL,
	is_active TINYINT NOT NULL,
	is_superuser TINYINT NOT NULL,
	last_login DATETIME NOT NULL,
	date_joined DATETIME NOT NULL,
	gold SMALLINT NOT NULL DEFAULT 0,
	silver SMALLINT UNSIGNED NOT NULL DEFAULT 0,
	bronze SMALLINT UNSIGNED NOT NULL DEFAULT 0,
	reputation INTEGER UNSIGNED NULL DEFAULT 1,
	gravatar VARCHAR(128) NULL,
	questions_per_page SMALLINT UNSIGNED NULL DEFAULT 10,
	last_seen DATETIME NULL,
	real_name VARCHAR(100) NULL,
	website VARCHAR(200) NULL,
	location VARCHAR(100) NULL,
	date_of_birth DATETIME NULL,
	about TEXT NULL
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;

/* Table Items: auth_user */

/* Add Indexes for: auth_user */
CREATE UNIQUE INDEX username ON auth_user (username);

/******************** Add Table: auth_user_groups ************************/

/* Build Table Structure */
CREATE TABLE auth_user_groups
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	group_id INTEGER NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: auth_user_groups */

/* Add Indexes for: auth_user_groups */
CREATE INDEX group_id_refs_id_f116770 ON auth_user_groups (group_id);
CREATE UNIQUE INDEX user_id ON auth_user_groups (user_id, group_id);

/******************** Add Table: auth_user_user_permissions ************************/

/* Build Table Structure */
CREATE TABLE auth_user_user_permissions
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	permission_id INTEGER NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: auth_user_user_permissions */

/* Add Indexes for: auth_user_user_permissions */
CREATE INDEX permission_id_refs_id_67e79cb ON auth_user_user_permissions (permission_id);
CREATE UNIQUE INDEX user_id ON auth_user_user_permissions (user_id, permission_id);

/******************** Add Table: award ************************/

/* Build Table Structure */
CREATE TABLE award
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	badge_id INTEGER NOT NULL,
	awarded_at DATETIME NOT NULL,
	notified TINYINT NOT NULL,
	content_type_id INTEGER NULL,
	object_id INTEGER NULL
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

/* Table Items: award */

/* Add Indexes for: award */
CREATE INDEX award_badge_id ON award (badge_id);
CREATE INDEX award_user_id ON award (user_id);

/******************** Add Table: badge ************************/

/* Build Table Structure */
CREATE TABLE badge
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	`type` SMALLINT NOT NULL,
	slug VARCHAR(50) NOT NULL,
	description TEXT NOT NULL,
	multiple TINYINT NOT NULL,
	awarded_count INTEGER UNSIGNED NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;

/* Table Items: badge */

/* Add Indexes for: badge */
CREATE INDEX badge_slug ON badge (slug);
CREATE UNIQUE INDEX name ON badge (name, `type`);

/******************** Add Table: book ************************/

/* Build Table Structure */
CREATE TABLE book
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	short_name VARCHAR(255) NOT NULL,
	author VARCHAR(255) NOT NULL,
	user_id INTEGER NULL,
	price DECIMAL(10, 2) NULL,
	pages SMALLINT NULL,
	published_at DATE NOT NULL,
	publication VARCHAR(255) NOT NULL,
	cover_img VARCHAR(255) NULL,
	tagnames VARCHAR(125) NULL,
	added_at DATETIME NOT NULL,
	last_edited_at DATETIME NOT NULL
) TYPE=InnoDB;

/* Table Items: book */

/* Add Indexes for: book */
CREATE UNIQUE INDEX book_short_name_Idx ON book (short_name);
CREATE INDEX fk_books_auth_user ON book (user_id);

/******************** Add Table: book_author_info ************************/

/* Build Table Structure */
CREATE TABLE book_author_info
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	blog_url VARCHAR(255) NULL,
	user_id INTEGER NOT NULL,
	added_at DATETIME NOT NULL,
	last_edited_at DATETIME NOT NULL
) TYPE=InnoDB;

/* Table Items: book_author_info */

/* Add Indexes for: book_author_info */
CREATE INDEX fk_book_author_info_auth_user ON book_author_info (user_id);

/******************** Add Table: book_author_rss ************************/

/* Build Table Structure */
CREATE TABLE book_author_rss
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	url VARCHAR(255) NOT NULL,
	rss_created_at DATETIME NOT NULL,
	user_id INTEGER NOT NULL,
	added_at DATETIME NOT NULL
) TYPE=InnoDB;

/* Table Items: book_author_rss */

/* Add Indexes for: book_author_rss */
CREATE INDEX fk_book_author_rss_auth_user ON book_author_rss (user_id);

/******************** Add Table: book_question ************************/

/* Build Table Structure */
CREATE TABLE book_question
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	book_id INTEGER NOT NULL,
	question_id INTEGER NOT NULL
) TYPE=InnoDB;

/* Table Items: book_question */

/* Add Indexes for: book_question */
CREATE INDEX fk_book_question_book ON book_question (book_id);
CREATE INDEX fk_book_question_question ON book_question (question_id);

/******************** Add Table: `comment` ************************/

/* Build Table Structure */
CREATE TABLE `comment`
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	content_type_id INTEGER NOT NULL,
	object_id INTEGER UNSIGNED NOT NULL,
	user_id INTEGER NOT NULL,
	`comment` TEXT NOT NULL,
	added_at DATETIME NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

/* Table Items: `comment` */

/* Add Indexes for: comment */
CREATE INDEX comment_content_type_id ON `comment` (content_type_id);
CREATE INDEX comment_user_id ON `comment` (user_id);
CREATE INDEX content_type_id ON `comment` (content_type_id, object_id, user_id);

/******************** Add Table: django_admin_log ************************/

/* Build Table Structure */
CREATE TABLE django_admin_log
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	action_time DATETIME NOT NULL,
	user_id INTEGER NOT NULL,
	content_type_id INTEGER NULL,
	object_id LONGTEXT NULL,
	object_repr VARCHAR(200) NOT NULL,
	action_flag SMALLINT UNSIGNED NOT NULL,
	change_message LONGTEXT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/* Table Items: django_admin_log */

/* Add Indexes for: django_admin_log */
CREATE INDEX django_admin_log_content_type_id ON django_admin_log (content_type_id);
CREATE INDEX django_admin_log_user_id ON django_admin_log (user_id);

/******************** Add Table: django_authopenid_association ************************/

/* Build Table Structure */
CREATE TABLE django_authopenid_association
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	server_url LONGTEXT NOT NULL,
	handle VARCHAR(255) NOT NULL,
	secret LONGTEXT NOT NULL,
	issued INTEGER NOT NULL,
	lifetime INTEGER NOT NULL,
	assoc_type LONGTEXT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/******************** Add Table: django_authopenid_nonce ************************/

/* Build Table Structure */
CREATE TABLE django_authopenid_nonce
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	server_url VARCHAR(255) NOT NULL,
	`timestamp` INTEGER NOT NULL,
	salt VARCHAR(40) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

/******************** Add Table: django_authopenid_userassociation ************************/

/* Build Table Structure */
CREATE TABLE django_authopenid_userassociation
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	openid_url VARCHAR(255) NOT NULL,
	user_id INTEGER NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/* Table Items: django_authopenid_userassociation */

/* Add Indexes for: django_authopenid_userassociation */
CREATE UNIQUE INDEX user_id ON django_authopenid_userassociation (user_id);

/******************** Add Table: django_authopenid_userpasswordqueue ************************/

/* Build Table Structure */
CREATE TABLE django_authopenid_userpasswordqueue
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	new_password VARCHAR(30) NOT NULL,
	confirm_key VARCHAR(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: django_authopenid_userpasswordqueue */

/* Add Indexes for: django_authopenid_userpasswordqueue */
CREATE UNIQUE INDEX user_id ON django_authopenid_userpasswordqueue (user_id);

/******************** Add Table: django_content_type ************************/

/* Build Table Structure */
CREATE TABLE django_content_type
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	app_label VARCHAR(100) NOT NULL,
	model VARCHAR(100) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

/* Table Items: django_content_type */

/* Add Indexes for: django_content_type */
CREATE UNIQUE INDEX app_label ON django_content_type (app_label, model);

/******************** Add Table: django_session ************************/

/* Build Table Structure */
CREATE TABLE django_session
(
	session_key VARCHAR(40) NOT NULL,
	session_data LONGTEXT NOT NULL,
	expire_date DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: django_session */
ALTER TABLE django_session ADD CONSTRAINT pkdjango_session
	PRIMARY KEY (session_key);

/******************** Add Table: django_site ************************/

/* Build Table Structure */
CREATE TABLE django_site
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	domain VARCHAR(100) NOT NULL,
	name VARCHAR(50) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/******************** Add Table: favorite_question ************************/

/* Build Table Structure */
CREATE TABLE favorite_question
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	question_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	added_at DATETIME NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/* Table Items: favorite_question */

/* Add Indexes for: favorite_question */
CREATE INDEX favorite_question_question_id ON favorite_question (question_id);
CREATE INDEX favorite_question_user_id ON favorite_question (user_id);

/******************** Add Table: flagged_item ************************/

/* Build Table Structure */
CREATE TABLE flagged_item
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	content_type_id INTEGER NOT NULL,
	object_id INTEGER UNSIGNED NOT NULL,
	user_id INTEGER NOT NULL,
	flagged_at DATETIME NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/* Table Items: flagged_item */

/* Add Indexes for: flagged_item */
CREATE UNIQUE INDEX content_type_id ON flagged_item (content_type_id, object_id, user_id);
CREATE INDEX flagged_item_content_type_id ON flagged_item (content_type_id);
CREATE INDEX flagged_item_user_id ON flagged_item (user_id);

/******************** Add Table: question ************************/

/* Build Table Structure */
CREATE TABLE question
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	title TEXT NOT NULL,
	author_id INTEGER NOT NULL,
	added_at DATETIME NOT NULL,
	wiki TINYINT NOT NULL,
	wikified_at DATETIME NULL,
	answer_accepted TINYINT NOT NULL,
	closed TINYINT NOT NULL,
	closed_by_id INTEGER NULL,
	closed_at DATETIME NULL,
	close_reason SMALLINT NULL,
	deleted TINYINT NOT NULL,
	deleted_at DATETIME NULL,
	deleted_by_id INTEGER NULL,
	locked TINYINT NOT NULL,
	locked_by_id INTEGER NULL,
	locked_at DATETIME NULL,
	score INTEGER NOT NULL,
	answer_count INTEGER UNSIGNED NOT NULL,
	comment_count INTEGER UNSIGNED NOT NULL,
	view_count INTEGER UNSIGNED NOT NULL,
	offensive_flag_count SMALLINT NOT NULL,
	favourite_count INTEGER UNSIGNED NOT NULL,
	last_edited_at DATETIME NULL,
	last_edited_by_id INTEGER NULL,
	last_activity_at DATETIME NOT NULL,
	last_activity_by_id INTEGER NOT NULL,
	tagnames VARCHAR(125) NOT NULL,
	summary VARCHAR(180) NOT NULL,
	html LONGTEXT NOT NULL,
	vote_up_count INTEGER NOT NULL,
	vote_down_count INTEGER NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

/* Table Items: question */

/* Add Indexes for: question */
CREATE INDEX question_author_id ON question (author_id);
CREATE INDEX question_closed_by_id ON question (closed_by_id);
CREATE INDEX question_deleted_by_id ON question (deleted_by_id);
CREATE INDEX question_last_activity_by_id ON question (last_activity_by_id);
CREATE INDEX question_last_edited_by_id ON question (last_edited_by_id);
CREATE INDEX question_locked_by_id ON question (locked_by_id);

/******************** Add Table: question_revision ************************/

/* Build Table Structure */
CREATE TABLE question_revision
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	question_id INTEGER NOT NULL,
	revision INTEGER UNSIGNED NOT NULL,
	title TEXT NOT NULL,
	author_id INTEGER NOT NULL,
	revised_at DATETIME NOT NULL,
	tagnames VARCHAR(125) NOT NULL,
	summary TEXT NOT NULL,
	`text` LONGTEXT NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/* Table Items: question_revision */

/* Add Indexes for: question_revision */
CREATE INDEX question_revision_author_id ON question_revision (author_id);
CREATE INDEX question_revision_question_id ON question_revision (question_id);

/******************** Add Table: question_tags ************************/

/* Build Table Structure */
CREATE TABLE question_tags
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	question_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

/* Table Items: question_tags */

/* Add Indexes for: question_tags */
CREATE UNIQUE INDEX question_id ON question_tags (question_id, tag_id);
CREATE INDEX tag_id_refs_id_43fcb953 ON question_tags (tag_id);

/******************** Add Table: repute ************************/

/* Build Table Structure */
CREATE TABLE repute
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	positive SMALLINT NOT NULL,
	negative SMALLINT NOT NULL,
	question_id INTEGER NOT NULL,
	reputed_at DATETIME NOT NULL,
	reputation_type SMALLINT NOT NULL,
	reputation INTEGER NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/* Table Items: repute */

/* Add Indexes for: repute */
CREATE INDEX repute_question_id ON repute (question_id);
CREATE INDEX repute_user_id ON repute (user_id);

/******************** Add Table: tag ************************/

/* Build Table Structure */
CREATE TABLE tag
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	created_by_id INTEGER NOT NULL,
	used_count INTEGER UNSIGNED NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

/* Table Items: tag */

/* Add Indexes for: tag */
CREATE UNIQUE INDEX name ON tag (name);
CREATE INDEX tag_created_by_id ON tag (created_by_id);

/******************** Add Table: user_badge ************************/

/* Build Table Structure */
CREATE TABLE user_badge
(
	id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	badge_id INTEGER NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: user_badge */

/* Add Indexes for: user_badge */
CREATE INDEX fk_user_badge_auth_user ON user_badge (user_id);
CREATE INDEX fk_user_badge_badge ON user_badge (badge_id);

/******************** Add Table: user_favorite_questions ************************/

/* Build Table Structure */
CREATE TABLE user_favorite_questions
(
	id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	question_id INTEGER NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* Table Items: user_favorite_questions */

/* Add Indexes for: user_favorite_questions */
CREATE INDEX fk_user_favorite_questions_auth_user ON user_favorite_questions (user_id);
CREATE INDEX fk_user_favorite_questions_question ON user_favorite_questions (question_id);

/******************** Add Table: vote ************************/

/* Build Table Structure */
CREATE TABLE vote
(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	content_type_id INTEGER NOT NULL,
	object_id INTEGER UNSIGNED NOT NULL,
	user_id INTEGER NOT NULL,
	vote SMALLINT NOT NULL,
	voted_at DATETIME NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/* Table Items: vote */

/* Add Indexes for: vote */
CREATE UNIQUE INDEX content_type_id ON vote (content_type_id, object_id, user_id);
CREATE INDEX vote_content_type_id ON vote (content_type_id);
CREATE INDEX vote_user_id ON vote (user_id);


/************ Add Foreign Keys to Database ***************/
/*-----------------------------------------------------------
Warning: Versions of MySQL prior to 4.1.2 require indexes on all columns involved in a foreign key. The following indexes may be required: 
fk_auth_group_permissions_auth_group may require an index on table: auth_group_permissions, column: group_id
fk_auth_user_groups_auth_user may require an index on table: auth_user_groups, column: user_id
fk_auth_user_user_permissions_auth_user may require an index on table: auth_user_user_permissions, column: user_id
fk_question_tags_question may require an index on table: question_tags, column: question_id
-----------------------------------------------------------
*/

/************ Foreign Key: fk_activity_auth_user ***************/
ALTER TABLE activity ADD CONSTRAINT fk_activity_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: deleted_by_id_refs_id_192b0170 ***************/
ALTER TABLE answer ADD CONSTRAINT deleted_by_id_refs_id_192b0170
	FOREIGN KEY (deleted_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_answer_auth_user ***************/
ALTER TABLE answer ADD CONSTRAINT fk_answer_auth_user
	FOREIGN KEY (author_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_answer_question ***************/
ALTER TABLE answer ADD CONSTRAINT fk_answer_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: last_edited_by_id_refs_id_192b0170 ***************/
ALTER TABLE answer ADD CONSTRAINT last_edited_by_id_refs_id_192b0170
	FOREIGN KEY (last_edited_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: locked_by_id_refs_id_192b0170 ***************/
ALTER TABLE answer ADD CONSTRAINT locked_by_id_refs_id_192b0170
	FOREIGN KEY (locked_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_answer_revision_auth_user ***************/
ALTER TABLE answer_revision ADD CONSTRAINT fk_answer_revision_auth_user
	FOREIGN KEY (author_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_group_permissions_auth_group ***************/
ALTER TABLE auth_group_permissions ADD CONSTRAINT fk_auth_group_permissions_auth_group
	FOREIGN KEY (group_id) REFERENCES auth_group (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_group_permissions_auth_permission ***************/
ALTER TABLE auth_group_permissions ADD CONSTRAINT fk_auth_group_permissions_auth_permission
	FOREIGN KEY (permission_id) REFERENCES auth_permission (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_message_auth_user ***************/
ALTER TABLE auth_message ADD CONSTRAINT fk_auth_message_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_permission_django_content_type ***************/
ALTER TABLE auth_permission ADD CONSTRAINT fk_auth_permission_django_content_type
	FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_user_groups_auth_group ***************/
ALTER TABLE auth_user_groups ADD CONSTRAINT fk_auth_user_groups_auth_group
	FOREIGN KEY (group_id) REFERENCES auth_group (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_user_groups_auth_user ***************/
ALTER TABLE auth_user_groups ADD CONSTRAINT fk_auth_user_groups_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_user_user_permissions_auth_permission ***************/
ALTER TABLE auth_user_user_permissions ADD CONSTRAINT fk_auth_user_user_permissions_auth_permission
	FOREIGN KEY (permission_id) REFERENCES auth_permission (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_auth_user_user_permissions_auth_user ***************/
ALTER TABLE auth_user_user_permissions ADD CONSTRAINT fk_auth_user_user_permissions_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_award_auth_user ***************/
ALTER TABLE award ADD CONSTRAINT fk_award_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_award_badge ***************/
ALTER TABLE award ADD CONSTRAINT fk_award_badge
	FOREIGN KEY (badge_id) REFERENCES badge (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_books_auth_user ***************/
ALTER TABLE book ADD CONSTRAINT fk_books_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_book_author_info_auth_user ***************/
ALTER TABLE book_author_info ADD CONSTRAINT fk_book_author_info_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_book_author_rss_auth_user ***************/
ALTER TABLE book_author_rss ADD CONSTRAINT fk_book_author_rss_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_book_question_book ***************/
ALTER TABLE book_question ADD CONSTRAINT fk_book_question_book
	FOREIGN KEY (book_id) REFERENCES book (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_book_question_question ***************/
ALTER TABLE book_question ADD CONSTRAINT fk_book_question_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_comment_auth_user ***************/
ALTER TABLE `comment` ADD CONSTRAINT fk_comment_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_comment_django_content_type ***************/
ALTER TABLE `comment` ADD CONSTRAINT fk_comment_django_content_type
	FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_django_admin_log_auth_user ***************/
ALTER TABLE django_admin_log ADD CONSTRAINT fk_django_admin_log_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_django_admin_log_django_content_type ***************/
ALTER TABLE django_admin_log ADD CONSTRAINT fk_django_admin_log_django_content_type
	FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_django_authopenid_userassociation_auth_user ***************/
ALTER TABLE django_authopenid_userassociation ADD CONSTRAINT fk_django_authopenid_userassociation_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_django_authopenid_userpasswordqueue_auth_user ***************/
ALTER TABLE django_authopenid_userpasswordqueue ADD CONSTRAINT fk_django_authopenid_userpasswordqueue_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_favorite_question_auth_user ***************/
ALTER TABLE favorite_question ADD CONSTRAINT fk_favorite_question_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_favorite_question_question ***************/
ALTER TABLE favorite_question ADD CONSTRAINT fk_favorite_question_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_flagged_item_auth_user ***************/
ALTER TABLE flagged_item ADD CONSTRAINT fk_flagged_item_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_flagged_item_django_content_type ***************/
ALTER TABLE flagged_item ADD CONSTRAINT fk_flagged_item_django_content_type
	FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: closed_by_id_refs_id_56e9d00c ***************/
ALTER TABLE question ADD CONSTRAINT closed_by_id_refs_id_56e9d00c
	FOREIGN KEY (closed_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: deleted_by_id_refs_id_56e9d00c ***************/
ALTER TABLE question ADD CONSTRAINT deleted_by_id_refs_id_56e9d00c
	FOREIGN KEY (deleted_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_auth_user ***************/
ALTER TABLE question ADD CONSTRAINT fk_question_auth_user
	FOREIGN KEY (author_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: last_activity_by_id_refs_id_56e9d00c ***************/
ALTER TABLE question ADD CONSTRAINT last_activity_by_id_refs_id_56e9d00c
	FOREIGN KEY (last_activity_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: last_edited_by_id_refs_id_56e9d00c ***************/
ALTER TABLE question ADD CONSTRAINT last_edited_by_id_refs_id_56e9d00c
	FOREIGN KEY (last_edited_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: locked_by_id_refs_id_56e9d00c ***************/
ALTER TABLE question ADD CONSTRAINT locked_by_id_refs_id_56e9d00c
	FOREIGN KEY (locked_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_revision_auth_user ***************/
ALTER TABLE question_revision ADD CONSTRAINT fk_question_revision_auth_user
	FOREIGN KEY (author_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_revision_question ***************/
ALTER TABLE question_revision ADD CONSTRAINT fk_question_revision_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_tags_question ***************/
ALTER TABLE question_tags ADD CONSTRAINT fk_question_tags_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_tags_tag ***************/
ALTER TABLE question_tags ADD CONSTRAINT fk_question_tags_tag
	FOREIGN KEY (tag_id) REFERENCES tag (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_repute_auth_user ***************/
ALTER TABLE repute ADD CONSTRAINT fk_repute_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_repute_question ***************/
ALTER TABLE repute ADD CONSTRAINT fk_repute_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_tag_auth_user ***************/
ALTER TABLE tag ADD CONSTRAINT fk_tag_auth_user
	FOREIGN KEY (created_by_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_user_badge_auth_user ***************/
ALTER TABLE user_badge ADD CONSTRAINT fk_user_badge_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_user_badge_badge ***************/
ALTER TABLE user_badge ADD CONSTRAINT fk_user_badge_badge
	FOREIGN KEY (badge_id) REFERENCES badge (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_user_favorite_questions_auth_user ***************/
ALTER TABLE user_favorite_questions ADD CONSTRAINT fk_user_favorite_questions_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_user_favorite_questions_question ***************/
ALTER TABLE user_favorite_questions ADD CONSTRAINT fk_user_favorite_questions_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_vote_auth_user ***************/
ALTER TABLE vote ADD CONSTRAINT fk_vote_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_vote_django_content_type ***************/
ALTER TABLE vote ADD CONSTRAINT fk_vote_django_content_type
	FOREIGN KEY (content_type_id) REFERENCES django_content_type (id) ON UPDATE NO ACTION ON DELETE NO ACTION;