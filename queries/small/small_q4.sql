SELECT MIN(cpi.first_name) AS player_first,
       MIN(dh.overall_pick) AS draft_pick
FROM common_player_info AS cpi,
     draft_history AS dh
WHERE cpi.person_id = dh.person_id
  AND dh.overall_pick <= 20;