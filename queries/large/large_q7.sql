SELECT MIN(g.game_date) AS game_date,
       MIN(gs.gamecode) AS game_code,
       MIN(o.first_name) AS ref_first,
       MIN(o.last_name) AS ref_last,
       MIN(gi.attendance) AS crowd_size
FROM game AS g,
     game_info AS gi,
     game_summary AS gs,
     officials AS o
WHERE gi.attendance > 8000
  AND g.reb_home > 20
  AND g.game_id = gi.game_id
  AND g.game_id = gs.game_id
  AND g.game_id = o.game_id;