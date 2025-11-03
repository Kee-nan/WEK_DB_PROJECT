SELECT 
    MIN(cpi.first_name) AS first_name,
    MIN(cpi.last_name) AS last_name,
    MIN(dh.overall_pick) AS draft_pick,
    MIN(t.full_name) AS drafted_team
FROM common_player_info AS cpi,
     draft_history AS dh,
     team AS t,
     team_details AS td
WHERE cpi.person_id = dh.person_id
  AND dh.team_id = t.id
  AND t.id = td.team_id
  AND dh.overall_pick <= 20
  AND td.arenacapacity > 15000;
