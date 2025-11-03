SELECT MIN(cpi.first_name) AS first_name,
       MIN(cpi.last_name) AS last_name,
       MIN(dc.height_w_shoes_ft_in) AS height,
       MIN(dh.season) AS draft_season,
       MIN(t.city) AS team_city
FROM common_player_info AS cpi,
     draft_combine_stats AS dc,
     draft_history AS dh,
     team AS t
WHERE dc.height_w_shoes > 75
  AND dh.season BETWEEN 2000 AND 2010
  AND cpi.person_id = dh.person_id
  AND cpi.person_id = dc.player_id
  AND dh.team_id = t.id;