SELECT MIN(pb.pctimestring)      AS sample_play_time,
       MIN(g.season_id)          AS season_id,
       MIN(gs.season)            AS game_summary_season,
       MIN(gi.attendance)        AS attendance,
       MIN(t.full_name)          AS team_name
FROM playbyplay AS pb,
     game       AS g,
     game_summary AS gs,
     game_info  AS gi,
     team       AS t
WHERE pb.game_id = g.game_id
  AND g.game_id = gs.game_id
  AND g.game_id = gi.game_id
  AND pb.player1_team_id = t.id
  AND gs.season BETWEEN 2010 AND 2015
  AND gi.attendance > 10000
  AND pb.eventmsgtype IN (1,2);
