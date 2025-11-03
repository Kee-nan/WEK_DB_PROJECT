SELECT 
    MIN(cpi.first_name) AS first_name,
    MIN(cpi.last_name) AS last_name,
    MIN(cpi.school) AS college,
    MIN(dh.season) AS draft_season,
    MIN(t.nickname) AS drafted_team
FROM common_player_info AS cpi,
     draft_history AS dh,
     team AS t
WHERE cpi.school ILIKE '%Duke%'
  AND dh.overall_pick <= 30
  AND dh.season BETWEEN 2010 AND 2020
  AND t.nickname ILIKE '%Lakers%'
  AND cpi.person_id = dh.person_id
  AND dh.team_id = t.id;