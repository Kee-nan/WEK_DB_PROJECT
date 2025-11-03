SELECT MIN(cpi.first_name) AS player_first,
       MIN(cpi.last_name)  AS player_last,
       MIN(t.nickname)     AS team_nickname
FROM common_player_info AS cpi,
     team                AS t
WHERE cpi.team_id = t.id
  AND cpi.position ILIKE '%G%';
