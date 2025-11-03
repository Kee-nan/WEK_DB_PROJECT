SELECT MIN(cpi.first_name) AS player_first,
       MIN(cpi.last_name) AS player_last,
       MIN(dc.wingspan_ft_in) AS wingspan,
       MIN(dh.season) AS draft_season,
       MIN(t.city) AS team_city,
       MIN(td.owner) AS owner_name
FROM common_player_info AS cpi,
     draft_combine_stats AS dc,
     draft_history AS dh,
     team AS t,
     team_details AS td,
     team_history AS th
WHERE dc.height_w_shoes > 78
  AND dh.season > 2005
  AND cpi.person_id = dc.player_id
  AND cpi.person_id = dh.person_id
  AND dh.team_id = t.id
  AND t.id = td.team_id
  AND t.id = th.team_id;