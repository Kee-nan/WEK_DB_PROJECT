SELECT 
    MIN(g.game_date) AS game_date,
    MIN(t.full_name) AS team_name,
    MIN(os.pts_paint_home) AS paint_pts,
    MIN(ls.pts_home) AS total_pts
FROM game AS g,
     team AS t,
     other_stats AS os,
     line_score AS ls
WHERE g.team_id_home = t.id
  AND g.game_id = os.game_id
  AND g.game_id = ls.game_id
  AND os.pts_paint_home > 20
  AND ls.pts_home > 90;
