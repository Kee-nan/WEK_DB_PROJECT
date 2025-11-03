CREATE TABLE player (
    id INT PRIMARY KEY,
    full_name VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN
);

CREATE TABLE common_player_info (
    person_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    display_first_last VARCHAR(100),
    display_last_comma_first VARCHAR(100),
    display_fi_last VARCHAR(100),
    player_slug VARCHAR(100),
    birthdate TIMESTAMP,
    school VARCHAR(100),
    country VARCHAR(100),
    last_affiliation VARCHAR(100),
    height VARCHAR(10),
    weight INT,
    season_exp FLOAT,
    jersey VARCHAR(10),
    position VARCHAR(50),
    rosterstatus VARCHAR(20),
    games_played_current_season_flag CHAR(1),
    team_id INT ,
    team_name VARCHAR(100),
    team_abbreviation VARCHAR(10),
    team_code VARCHAR(20),
    team_city VARCHAR(50),
    playercode VARCHAR(100),
    from_year FLOAT,
    to_year FLOAT,
    dleague_flag CHAR(1),
    nba_flag CHAR(1),
    games_played_flag CHAR(1),
    draft_year VARCHAR(20) ,
    draft_round VARCHAR(20),
    draft_number VARCHAR(20),
    greatest_75_flag CHAR(1)
);

CREATE TABLE draft_combine_stats (
    season INT,
    player_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    player_name VARCHAR(100),
    position VARCHAR(10),
    height_wo_shoes FLOAT,
    height_wo_shoes_ft_in VARCHAR(10),
    height_w_shoes FLOAT,
    height_w_shoes_ft_in VARCHAR(10),
    weight FLOAT,
    wingspan FLOAT,
    wingspan_ft_in VARCHAR(10),
    standing_reach FLOAT,
    standing_reach_ft_in VARCHAR(10),
    body_fat_pct FLOAT,
    hand_length FLOAT,
    hand_width FLOAT,
    standing_vertical_leap FLOAT,
    max_vertical_leap FLOAT,
    lane_agility_time FLOAT,
    modified_lane_agility_time FLOAT,
    three_quarter_sprint FLOAT,
    bench_press FLOAT,
    spot_fifteen_corner_left FLOAT,
    spot_fifteen_break_left FLOAT,
    spot_fifteen_top_key FLOAT,
    spot_fifteen_break_right FLOAT,
    spot_fifteen_corner_right FLOAT,
    spot_college_corner_left FLOAT,
    spot_college_break_left FLOAT,
    spot_college_top_key FLOAT,
    spot_college_break_right FLOAT,
    spot_college_corner_right FLOAT,
    spot_nba_corner_left FLOAT,
    spot_nba_break_left FLOAT,
    spot_nba_top_key FLOAT,
    spot_nba_break_right FLOAT,
    spot_nba_corner_right FLOAT,
    off_drib_fifteen_break_left FLOAT,
    off_drib_fifteen_top_key FLOAT,
    off_drib_fifteen_break_right FLOAT,
    off_drib_college_break_left FLOAT,
    off_drib_college_top_key FLOAT,
    off_drib_college_break_right FLOAT,
    on_move_fifteen FLOAT,
    on_move_college FLOAT
);

ALTER TABLE draft_combine_stats
  ALTER COLUMN spot_fifteen_corner_left TYPE TEXT,
  ALTER COLUMN spot_fifteen_break_left TYPE TEXT,
  ALTER COLUMN spot_fifteen_top_key TYPE TEXT,
  ALTER COLUMN spot_fifteen_break_right TYPE TEXT,
  ALTER COLUMN spot_fifteen_corner_right TYPE TEXT,
  ALTER COLUMN spot_college_corner_left TYPE TEXT,
  ALTER COLUMN spot_college_break_left TYPE TEXT,
  ALTER COLUMN spot_college_top_key TYPE TEXT,
  ALTER COLUMN spot_college_break_right TYPE TEXT,
  ALTER COLUMN spot_college_corner_right TYPE TEXT,
  ALTER COLUMN spot_nba_corner_left TYPE TEXT,
  ALTER COLUMN spot_nba_break_left TYPE TEXT,
  ALTER COLUMN spot_nba_top_key TYPE TEXT,
  ALTER COLUMN spot_nba_break_right TYPE TEXT,
  ALTER COLUMN spot_nba_corner_right TYPE TEXT,
  ALTER COLUMN off_drib_fifteen_break_left TYPE TEXT,
  ALTER COLUMN off_drib_fifteen_top_key TYPE TEXT,
  ALTER COLUMN off_drib_fifteen_break_right TYPE TEXT,
  ALTER COLUMN off_drib_college_break_left TYPE TEXT,
  ALTER COLUMN off_drib_college_top_key TYPE TEXT,
  ALTER COLUMN off_drib_college_break_right TYPE TEXT,
  ALTER COLUMN on_move_fifteen TYPE TEXT,
  ALTER COLUMN on_move_college TYPE TEXT;


ALTER TABLE draft_combine_stats 
  ALTER COLUMN spot_fifteen_corner_left TYPE TEXT;
  
CREATE TABLE draft_history (
    person_id INT,
    player_name VARCHAR(100),
    season INT,
    round_number INT,
    round_pick INT,
    overall_pick INT,
    draft_type VARCHAR(50),
    team_id INT,
    team_city VARCHAR(50),
    team_name VARCHAR(100),
    team_abbreviation VARCHAR(10),
    organization VARCHAR(100),
    organization_type VARCHAR(50),
    player_profile_flag BOOLEAN
);

CREATE TABLE game_info (
    game_id VARCHAR(20),
    game_date TIMESTAMP,
    attendance FLOAT,
    game_time VARCHAR(20)
);

CREATE TABLE game_summary (
    game_date_est TIMESTAMP,
    game_sequence FLOAT,
    game_id VARCHAR(20),
    game_status_id INT,
    game_status_text VARCHAR(50),
    gamecode VARCHAR(50),
    home_team_id INT,
    visitor_team_id INT,
    season INT,
    live_period INT,
    live_pc_time VARCHAR(40),
    natl_tv_broadcaster_abbreviation VARCHAR(40),
    live_period_time_bcast VARCHAR(40),
    wh_status INT
);

CREATE TABLE game (
    season_id INT,
    team_id_home INT ,
    team_abbreviation_home VARCHAR(10),
    team_name_home VARCHAR(100),
    game_id VARCHAR(20),
    game_date TIMESTAMP,
    matchup_home VARCHAR(50),
    wl_home CHAR(1),
    min FLOAT,
    fgm_home FLOAT,
    fga_home FLOAT,
    fg_pct_home FLOAT,
    fg3m_home FLOAT,
    fg3a_home FLOAT,
    fg3_pct_home FLOAT,
    ftm_home FLOAT,
    fta_home FLOAT,
    ft_pct_home FLOAT,
    oreb_home FLOAT,
    dreb_home FLOAT,
    reb_home FLOAT,
    ast_home FLOAT,
    stl_home FLOAT,
    blk_home FLOAT,
    tov_home FLOAT,
    pf_home FLOAT,
    pts_home FLOAT,
    plus_minus_home FLOAT,
    video_available_home BOOLEAN,
    team_id_away INT,
    team_abbreviation_away VARCHAR(10),
    team_name_away VARCHAR(100),
    matchup_away VARCHAR(50),
    wl_away CHAR(1),
    fgm_away FLOAT,
    fga_away FLOAT,
    fg_pct_away FLOAT,
    fg3m_away FLOAT,
    fg3a_away FLOAT,
    fg3_pct_away FLOAT,
    ftm_away FLOAT,
    fta_away FLOAT,
    ft_pct_away FLOAT,
    oreb_away FLOAT,
    dreb_away FLOAT,
    reb_away FLOAT,
    ast_away FLOAT,
    stl_away FLOAT,
    blk_away FLOAT,
    tov_away FLOAT,
    pf_away FLOAT,
    pts_away FLOAT,
    plus_minus_away FLOAT,
    video_available_away BOOLEAN,
    season_type VARCHAR(30)
);

CREATE TABLE inactive_players (
    game_id VARCHAR(20),
    player_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    jersey_num INT,
    team_id INT,
    team_city VARCHAR(50),
    team_name VARCHAR(100),
    team_abbreviation VARCHAR(10)
);

CREATE TABLE line_score (
    game_date_est TIMESTAMP,
    game_sequence FLOAT,
    game_id VARCHAR(20),
    team_id_home INT,
    team_abbreviation_home VARCHAR(10),
    team_city_name_home VARCHAR(50),
    team_nickname_home VARCHAR(50),
    team_wins_losses_home VARCHAR(20),
    pts_qtr1_home FLOAT,
    pts_qtr2_home FLOAT,
    pts_qtr3_home FLOAT,
    pts_qtr4_home FLOAT,
    pts_ot1_home FLOAT,
    pts_ot2_home FLOAT,
    pts_ot3_home FLOAT,
    pts_ot4_home FLOAT,
    pts_ot5_home FLOAT,
    pts_ot6_home FLOAT,
    pts_ot7_home FLOAT,
    pts_ot8_home FLOAT,
    pts_ot9_home FLOAT,
    pts_ot10_home FLOAT,
    pts_home FLOAT,
    team_id_away INT,
    team_abbreviation_away VARCHAR(10),
    team_city_name_away VARCHAR(50),
    team_nickname_away VARCHAR(50),
    team_wins_losses_away VARCHAR(20),
    pts_qtr1_away FLOAT,
    pts_qtr2_away FLOAT,
    pts_qtr3_away FLOAT,
    pts_qtr4_away FLOAT,
    pts_ot1_away FLOAT,
    pts_ot2_away FLOAT,
    pts_ot3_away FLOAT,
    pts_ot4_away FLOAT,
    pts_ot5_away FLOAT,
    pts_ot6_away FLOAT,
    pts_ot7_away FLOAT,
    pts_ot8_away FLOAT,
    pts_ot9_away FLOAT,
    pts_ot10_away FLOAT,
    pts_away FLOAT
);


CREATE TABLE officials (
    game_id VARCHAR(20),
    official_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    jersey_num INT
);

CREATE TABLE other_stats (
    game_id VARCHAR(20),
    league_id VARCHAR(10),
    team_id_home INT ,
    team_abbreviation_home VARCHAR(10),
    team_city_home VARCHAR(50),
    pts_paint_home FLOAT,
    pts_2nd_chance_home FLOAT,
    pts_fb_home FLOAT,
    largest_lead_home FLOAT,
    lead_changes INT,
    times_tied INT,
    team_turnovers_home FLOAT,
    total_turnovers_home FLOAT,
    team_rebounds_home FLOAT,
    pts_off_to_home FLOAT,
    team_id_away INT ,
    team_abbreviation_away VARCHAR(10),
    team_city_away VARCHAR(50),
    pts_paint_away FLOAT,
    pts_2nd_chance_away FLOAT,
    pts_fb_away FLOAT,
    largest_lead_away FLOAT,
    team_turnovers_away FLOAT,
    total_turnovers_away FLOAT,
    team_rebounds_away FLOAT,
    pts_off_to_away FLOAT
);

CREATE TABLE team (
    id INT PRIMARY KEY,
    full_name VARCHAR(100),
    abbreviation VARCHAR(10),
    nickname VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    year_founded FLOAT
);

CREATE TABLE team_details (
    team_id INT PRIMARY KEY REFERENCES team(id),
    abbreviation VARCHAR(10),
    nickname VARCHAR(50),
    yearfounded FLOAT,
    city VARCHAR(50),
    arena VARCHAR(100),
    arenacapacity FLOAT,
    owner VARCHAR(100),
    generalmanager VARCHAR(100),
    headcoach VARCHAR(100),
    dleagueaffiliation VARCHAR(100),
    facebook VARCHAR(255),
    instagram VARCHAR(255),
    twitter VARCHAR(255)
);

CREATE TABLE team_history (
    team_id INT REFERENCES team(id),
    city VARCHAR(50),
    nickname VARCHAR(50),
    year_founded INT,
    year_active_till INT,
    PRIMARY KEY (team_id, city, year_founded)
);


ALTER TABLE public.common_player_info
ALTER COLUMN draft_year TYPE TEXT USING draft_year::TEXT;

ALTER TABLE public.common_player_info
ALTER COLUMN draft_year TYPE TEXT USING draft_year::TEXT,
ALTER COLUMN draft_round TYPE TEXT USING draft_round::TEXT,
ALTER COLUMN draft_number TYPE TEXT USING draft_number::TEXT;


CREATE TABLE temp_other_stats (LIKE public.other_stats INCLUDING ALL);
ALTER TABLE temp_other_stats DROP CONSTRAINT IF EXISTS other_stats_pkey;


ALTER TABLE other_stats DROP CONSTRAINT other_stats_team_id_home_fkey;

ALTER TABLE game_info ALTER COLUMN attendance TYPE INTEGER USING attendance::INTEGER;
ALTER TABLE game_summary ALTER COLUMN game_sequence TYPE INTEGER USING game_sequence::INTEGER;

CREATE TABLE PlayByPlay (
    game_id VARCHAR(20),
    eventnum INT,
    eventmsgtype INT,
    eventmsgactiontype INT,
    period INT,
    wctimestring VARCHAR(20),
    pctimestring VARCHAR(20),
    homedescription VARCHAR(255),
    neutraldescription VARCHAR(255),
    visitordescription VARCHAR(255),
    score VARCHAR(20),
    scoremargin VARCHAR(20),
    
    person1type FLOAT,
    player1_id FLOAT,
    player1_name VARCHAR(100),
    player1_team_id FLOAT,
    player1_team_city VARCHAR(100),
    player1_team_nickname VARCHAR(100),
    player1_team_abbreviation VARCHAR(10),
    
    person2type FLOAT,
    player2_id FLOAT,
    player2_name VARCHAR(100),
    player2_team_id FLOAT,
    player2_team_city VARCHAR(100),
    player2_team_nickname VARCHAR(100),
    player2_team_abbreviation VARCHAR(10),
    
    person3type FLOAT,
    player3_id FLOAT,
    player3_name VARCHAR(100),
    player3_team_id FLOAT,
    player3_team_city VARCHAR(100),
    player3_team_nickname VARCHAR(100),
    player3_team_abbreviation VARCHAR(10),
    
    video_available_flag FLOAT
);
