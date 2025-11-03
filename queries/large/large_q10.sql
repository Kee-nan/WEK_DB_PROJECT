SELECT MIN(gs.gamecode) AS game_code,
       MIN(gi.attendance) AS attendance,
       MIN(o.first_name) AS ref_first,
       MIN(t.full_name) AS home_team,
       MIN(td.arena) AS arena_name,
       MIN(os.pts_paint_home) AS paint_points
FROM game_summary AS gs,
     game_info AS gi,
     officials AS o,
     game AS g,
     team AS t,
     team_details AS td,
     other_stats AS os
WHERE gi.attendance > 10000
  AND os.pts_paint_home > 40
  AND g.game_id = gi.game_id
  AND g.game_id = gs.game_id
  AND g.game_id = o.game_id
  AND g.team_id_home = t.id
  AND t.id = td.team_id
  AND g.game_id = os.game_id;