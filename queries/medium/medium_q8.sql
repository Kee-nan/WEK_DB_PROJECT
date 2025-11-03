SELECT 
    MIN(g.game_date) AS game_date,
    MIN(gi.attendance) AS attendance,
    MIN(o.last_name) AS ref_last,
    MIN(o.first_name) AS ref_first
FROM game AS g,
     game_info AS gi,
     officials AS o
WHERE g.game_id = gi.game_id
  AND g.game_id = o.game_id
  AND gi.attendance > 10000
  AND o.jersey_num BETWEEN 5 AND 20;
