SELECT MIN(o.first_name) AS official_first,
       MIN(g.pts_home) AS points
FROM officials AS o,
     game AS g
WHERE o.game_id = g.game_id
  AND o.jersey_num > 15;