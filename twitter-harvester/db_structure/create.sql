create table keyword
(
	id serial not null
		constraint keyword_pkey
			primary key,
	keyword varchar(50) default ''::character varying,
	keyword_group varchar(50) default ''::character varying,
	max_id integer default '-1'::integer,
	since_id integer default '-1'::integer
)
;

create table twitter_token
(
	id serial not null
		constraint twitter_token_pkey
			primary key,
	consumer_key varchar(100) default ''::character varying,
	consumer_secret varchar(100),
	access_token varchar(100),
	access_token_secret varchar(100),
	keyword_group varchar(100)
)
;