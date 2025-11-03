SELECT MIN(pb.pctimestring) AS pctime,
       MIN(g.season_id) AS game_season,
       MIN(t.full_name) AS team_name
FROM playbyplay AS pb,
     game AS g,
     team AS t
WHERE g.pts_home > 50
  AND pb.game_id = g.game_id
  AND pb.player1_team_id = t.id;