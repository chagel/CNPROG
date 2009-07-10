USE cnprog;


/************ Add Foreign Keys to Database ***************/

/************ Foreign Key: fk_activity_auth_user ***************/
ALTER TABLE activity ADD CONSTRAINT fk_activity_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_revision_auth_user ***************/
ALTER TABLE question_revision ADD CONSTRAINT fk_question_revision_auth_user
	FOREIGN KEY (author_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_question_revision_question ***************/
ALTER TABLE question_revision ADD CONSTRAINT fk_question_revision_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_repute_auth_user ***************/
ALTER TABLE repute ADD CONSTRAINT fk_repute_auth_user
	FOREIGN KEY (user_id) REFERENCES auth_user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

/************ Foreign Key: fk_repute_question ***************/
ALTER TABLE repute ADD CONSTRAINT fk_repute_question
	FOREIGN KEY (question_id) REFERENCES question (id) ON UPDATE NO ACTION ON DELETE NO ACTION;