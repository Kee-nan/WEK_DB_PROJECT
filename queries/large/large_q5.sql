SELECT
	MIN(g.reb_home) AS home_rebounds,
	MIN(g.ast_home) AS home_assists,
    MIN(gi.attendance) AS attendance,
    MIN(o.first_name) AS official_firstname,
    MIN(o.last_name) AS official_lastname,
	Min(gs.gamecode) AS gamecode
FROM 
	game AS g,
    game_info AS gi,
    officials AS o,
	game_summary AS gs
WHERE gi.attendance > 10000
  AND g.reb_home > 20
  AND g.ast_home > 20
  ANd o.jersey_num > 20
  AND g.game_id = gi.game_id
  AND g.game_id = o.game_id
  and g.game_id = gs.game_id;