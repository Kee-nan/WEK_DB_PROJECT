SELECT 
    MIN(dcs.player_name) AS player_name,
    MIN(dcs.height_w_shoes) AS height,
    MIN(dcs.weight) AS weight,
    MIN(dh.overall_pick) AS draft_pick
FROM draft_combine_stats AS dcs,
     draft_history AS dh,
     common_player_info AS cpi,
     team AS t
WHERE dcs.player_id = cpi.person_id
  AND cpi.person_id = dh.person_id
  AND dh.team_id = t.id
  AND dcs.weight > 190
  AND dh.round_number <= 2;
