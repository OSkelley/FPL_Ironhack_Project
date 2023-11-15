

create table if not exists fpl.fpl as (
select 2017 as season, f.name, f.assists, f.bonus, f.bps, f.clean_sheets, f.creativity,
       f.element, f.fixture, f.goals_conceded, f.goals_scored, f.ict_index,
       f.influence, f.kickoff_time, f.minutes, f.opponent_team, f.own_goals,
       f.penalties_missed, f.penalties_saved, f.red_cards, f.round, f.saves,
       f.selected, f.team_a_score, f.team_h_score, f.threat, f.total_points,
       f.transfers_balance, f.transfers_in, f.transfers_out, f.value,
       f.was_home, f.yellow_cards, f.GW, f.id from 2017_fpl f
union all
select 2018 as season, f.name, f.assists, f.bonus, f.bps, f.clean_sheets, f.creativity,
       f.element, f.fixture, f.goals_conceded, f.goals_scored, f.ict_index,
       f.influence, f.kickoff_time, f.minutes, f.opponent_team, f.own_goals,
       f.penalties_missed, f.penalties_saved, f.red_cards, f.round, f.saves,
       f.selected, f.team_a_score, f.team_h_score, f.threat, f.total_points,
       f.transfers_balance, f.transfers_in, f.transfers_out, f.value,
       f.was_home, f.yellow_cards, f.GW, f.id from 2018_fpl f
union all
select 2019 as season, f.name, f.assists, f.bonus, f.bps, f.clean_sheets, f.creativity,
       f.element, f.fixture, f.goals_conceded, f.goals_scored, f.ict_index,
       f.influence, f.kickoff_time, f.minutes, f.opponent_team, f.own_goals,
       f.penalties_missed, f.penalties_saved, f.red_cards, f.round, f.saves,
       f.selected, f.team_a_score, f.team_h_score, f.threat, f.total_points,
       f.transfers_balance, f.transfers_in, f.transfers_out, f.value,
       f.was_home, f.yellow_cards, f.GW, f.id from 2019_fpl f
union all
select 2020 as season, f.name, f.assists, f.bonus, f.bps, f.clean_sheets, f.creativity,
       f.element, f.fixture, f.goals_conceded, f.goals_scored, f.ict_index,
       f.influence, f.kickoff_time, f.minutes, f.opponent_team, f.own_goals,
       f.penalties_missed, f.penalties_saved, f.red_cards, f.round, f.saves,
       f.selected, f.team_a_score, f.team_h_score, f.threat, f.total_points,
       f.transfers_balance, f.transfers_in, f.transfers_out, f.value,
       f.was_home, f.yellow_cards, f.GW, f.id from 2020_fpl f
union all
select 2021 as season, f.name, f.assists, f.bonus, f.bps, f.clean_sheets, f.creativity,
       f.element, f.fixture, f.goals_conceded, f.goals_scored, f.ict_index,
       f.influence, f.kickoff_time, f.minutes, f.opponent_team, f.own_goals,
       f.penalties_missed, f.penalties_saved, f.red_cards, f.round, f.saves,
       f.selected, f.team_a_score, f.team_h_score, f.threat, f.total_points,
       f.transfers_balance, f.transfers_in, f.transfers_out, f.value,
       f.was_home, f.yellow_cards, f.GW, f.id from 2021_fpl f
union all
select 2022 as season, f.name, f.assists, f.bonus, f.bps, f.clean_sheets, f.creativity,
       f.element, f.fixture, f.goals_conceded, f.goals_scored, f.ict_index,
       f.influence, f.kickoff_time, f.minutes, f.opponent_team, f.own_goals,
       f.penalties_missed, f.penalties_saved, f.red_cards, f.round, f.saves,
       f.selected, f.team_a_score, f.team_h_score, f.threat, f.total_points,
       f.transfers_balance, f.transfers_in, f.transfers_out, f.value,
       f.was_home, f.yellow_cards, f.GW, f.id from 2022_fpl f
);

select * from fbref;

select max(length(Squad)) from fbref;

create table if not exists fpl.team (
team varchar(16),
team_id int auto_increment,
primary key (team_id));

insert into fpl.team(team)
select distinct Squad from fpl.fbref;

select * from fpl;
select * from fpl.fbref;

select * from 2020_fpl;