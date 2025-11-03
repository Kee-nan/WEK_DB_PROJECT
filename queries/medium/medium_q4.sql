SELECT MIN(cpi.first_name) AS player_first,
       MIN(cpi.last_name) AS player_last,
       MIN(t.full_name) AS drafted_team
FROM common_player_info AS cpi,
     draft_history AS dh,
     team AS t
WHERE dh.overall_pick <= 10
  AND dh.season > 2000
  AND cpi.person_id = dh.person_id
  AND dh.team_id = t.id;