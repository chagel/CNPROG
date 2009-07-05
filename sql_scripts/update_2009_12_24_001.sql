alter table question add column `vote_up_count` int(11) NOT NULL;
alter table question add column `vote_down_count` int(11) NOT NULL;

alter table answer add column `vote_up_count` int(11) NOT NULL;
alter table answer add column `vote_down_count` int(11) NOT NULL;