SELECT MIN(cpi.first_name) AS player_first,
       MIN(cpi.last_name) AS player_last,
       MIN(dc.height_wo_shoes_ft_in) AS height,
       MIN(t.city) AS team_city,
       MIN(th.year_founded) AS year_founded,
       MIN(gs.gamecode) AS game_code,
       MIN(os.pts_fb_home) AS fastbreak_points
FROM common_player_info AS cpi,
     draft_combine_stats AS dc,
     draft_history AS dh,
     team AS t,
     team_history AS th,
     game_summary AS gs,
     other_stats AS os
WHERE dh.overall_pick < 20
  AND os.pts_fb_home > 10
  AND cpi.person_id = dh.person_id
  AND cpi.person_id = dc.player_id
  AND dh.team_id = t.id
  AND t.id = th.team_id
  AND gs.home_team_id = t.id
  AND gs.game_id = os.game_id;