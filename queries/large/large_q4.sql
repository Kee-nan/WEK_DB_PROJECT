SELECT MIN(pb.pctimestring)      AS play_time,
       MIN(cpi.first_name)       AS player_first,
       MIN(cpi.last_name)        AS player_last,
       MIN(dh.season)            AS draft_season,
       MIN(t.nickname)           AS team_nickname,
       MIN(gs.season)            AS game_summary_season
FROM playbyplay        AS pb,
     common_player_info AS cpi,
     draft_history      AS dh,
     team               AS t,
     game               AS g,
     game_summary       AS gs
WHERE pb.player1_id = cpi.person_id
  AND cpi.person_id = dh.person_id
  AND pb.player1_team_id = t.id
  AND pb.game_id = g.game_id
  AND g.game_id = gs.game_id
  AND gs.season BETWEEN 2005 AND 2010
  AND cpi.position ILIKE '%F%'
  AND dh.overall_pick <= 100;
