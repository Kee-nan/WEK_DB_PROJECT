SELECT MIN(g.game_date)           AS game_date,
       MIN(ls.pts_home)           AS pts_home,
       MIN(os.pts_paint_home)     AS pts_paint_home,
       MIN(o.first_name)         AS official_first,
       MIN(o.last_name)          AS official_last,
       MIN(ip.team_name)         AS inactive_team_name
FROM game        AS g,
     line_score  AS ls,
     other_stats AS os,
     officials   AS o,
     team        AS t,
     inactive_players AS ip
WHERE g.game_id = ls.game_id
  AND g.game_id = os.game_id
  AND g.game_id = o.game_id
  AND g.team_id_home = t.id
  AND ip.game_id = g.game_id
  AND os.pts_paint_home > 30
  AND ls.pts_home > 90
  AND o.jersey_num > 10
  AND ip.team_id = t.id;

