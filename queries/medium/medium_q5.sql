SELECT MIN(g.game_date) AS game_date,
       MIN(gi.attendance) AS attendance,
       MIN(t.full_name) AS home_team
FROM game AS g,
     game_info AS gi,
     team AS t
WHERE gi.attendance > 15000
  AND g.team_id_home = t.id
  AND g.game_id = gi.game_id;