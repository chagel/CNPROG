ALTER TABLE comment DROP INDEX content_type_id;

ALTER TABLE comment ADD INDEX `content_type_id` (`content_type_id`,`object_id`,`user_id`);