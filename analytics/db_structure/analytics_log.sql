create table analytics_log
(
	data_timestamp varchar(20),
	status boolean,
	id serial not null
		constraint analytics_log_id_pk
			primary key
)
;

create unique index analytics_log_id_uindex
	on analytics_log (id)
;