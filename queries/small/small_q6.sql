SELECT MIN(pb.pctimestring)   AS play_time,
       MIN(g.season_id)       AS season_id
FROM playbyplay AS pb,
     game       AS g
WHERE pb.game_id = g.game_id
  AND g.pts_home > 70;
