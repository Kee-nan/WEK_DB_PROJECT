SELECT MIN(o.first_name) AS ref_first,
       MIN(o.last_name) AS ref_last,
       MIN(t.city) AS team_city
FROM officials AS o,
     game AS g,
     team AS t
WHERE o.jersey_num > 10
  AND g.team_id_home = t.id
  AND g.game_id = o.game_id;