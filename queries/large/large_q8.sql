SELECT MIN(g.game_date) AS date_played,
       MIN(l.pts_home) AS home_points,
       MIN(l.pts_away) AS away_points,
       MIN(t.full_name) AS home_team,
       MIN(td.city) AS home_city
FROM line_score AS l,
     game AS g,
     team AS t,
     team_details AS td
WHERE l.pts_home > 50
  AND g.team_id_home = t.id
  AND t.id = td.team_id
  AND l.game_id = g.game_id;