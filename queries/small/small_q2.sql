SELECT MIN(g.game_date) AS game_date,
       MIN(t.full_name) AS team_name
FROM game AS g,
     team AS t
WHERE g.team_id_home = t.id
  AND g.pts_home > 80;