ALTER TABLE answer ADD COLUMN `accepted_at` datetime default null;

/* Update accepted_at column with answer added datetime for existing data */
UPDATE answer
SET accepted_at = added_at
WHERE accepted = 1 AND accepted_at IS NULL;

/* workround for c# url problem on bluehost server */
UPDATE tag
SET name = 'csharp'
WHERE name = 'c#'

UPDATE question
SET tagnames = replace(tagnames, 'c#', 'csharp')
WHERE tagnames like '%c#%'

UPDATE question_revision
SET tagnames = replace(tagnames, 'c#', 'csharp')
WHERE tagnames like '%c#%'