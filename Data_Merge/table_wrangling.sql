create table if not exists fpl_data.fbref as(
select * from fpl.fbref
);

create table if not exists fpl_data.fpl as(
select * from fpl.fpl
);

create table if not exists fpl_data.player as(
select * from fpl.player
);

create table if not exists fpl_data.team as(
select * from fpl.team
);

alter table fpl_data.fpl
add column  int after Squad,
add column Opponent_id int after Opponent;

select t1.team_id
from fbref f
join team t1 on t1.team = f.Squad;

update fpl_data.fpl f, fpl_data.player t
set f.Squad_id = t.team_id
where f.Squad = t.team;

update fpl_data.fbref f, fpl_data.team t
set f.Opponent_id = t.team_id
where f.Opponent = t.team;

alter table fpl_data.fbref drop column Squad;
alter table fpl_data.fbref drop column Opponent;

select * from fpl;

ALTER TABLE fpl
ADD FOREIGN KEY (`unique`) REFERENCES player(`unique`);

alter table fpl_data.fpl
add column player int after name;

update fpl_data.fpl f, (select * from fpl_data.player ip where ip.unique < 2000) p
set f.player = p.unique
where f.id = p.id
and season =2017;


select * from fpl;