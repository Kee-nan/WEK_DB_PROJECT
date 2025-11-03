SELECT MIN(dcs.player_name)        AS player_name,
       MIN(cpi.school)             AS college,
       MIN(dh.overall_pick)        AS draft_pick,
       MIN(t.full_name)            AS drafted_team,
       MIN(td.arenacapacity)       AS arena_capacity,
       MIN(p.full_name)            AS player_table_name
FROM draft_combine_stats AS dcs,
     common_player_info   AS cpi,
     draft_history        AS dh,
     team                 AS t,
     team_details         AS td,
     player               AS p
WHERE dcs.player_id = cpi.person_id
  AND cpi.person_id = dh.person_id
  AND dh.team_id = t.id
  AND t.id = td.team_id
  AND cpi.person_id = p.id
  AND dcs.position = 'SG'
  AND dcs.weight > 200
  AND dh.overall_pick <= 50
  AND td.arenacapacity > 15000;
