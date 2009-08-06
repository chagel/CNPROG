ALTER TABLE auth_user ADD COLUMN email_isvalid TINYINT(1) NOT NULL;
UPDATE auth_user SET email_isvalid=1;
ALTER TABLE auth_user ADD COLUMN email_key varchar(32);
