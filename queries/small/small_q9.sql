SELECT MIN(os.game_id)      AS game_id,
       MIN(t.full_name)     AS team_name,
       MIN(os.pts_paint_home) AS pts_paint_home
FROM other_stats AS os,
     team        AS t
WHERE os.team_id_home = t.id
  AND os.pts_paint_home > 30;
