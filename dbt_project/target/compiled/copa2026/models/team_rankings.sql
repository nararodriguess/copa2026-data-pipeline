WITH match_results AS (
    SELECT
        home_team AS team,
        CASE WHEN home_score > away_score THEN 3
             WHEN home_score = away_score THEN 1
             ELSE 0 END AS points,
        CASE WHEN home_score > away_score THEN 1 ELSE 0 END AS wins,
        CASE WHEN home_score = away_score THEN 1 ELSE 0 END AS draws,
        CASE WHEN home_score < away_score THEN 1 ELSE 0 END AS losses,
        home_score AS goals_scored,
        away_score AS goals_conceded
    FROM matches
    WHERE status = 'FINISHED'

    UNION ALL

    SELECT
        away_team AS team,
        CASE WHEN away_score > home_score THEN 3
             WHEN away_score = home_score THEN 1
             ELSE 0 END AS points,
        CASE WHEN away_score > home_score THEN 1 ELSE 0 END AS wins,
        CASE WHEN away_score = home_score THEN 1 ELSE 0 END AS draws,
        CASE WHEN away_score < home_score THEN 1 ELSE 0 END AS losses,
        away_score AS goals_scored,
        home_score AS goals_conceded
    FROM matches
    WHERE status = 'FINISHED'
)

SELECT
    team,
    SUM(points)         AS points,
    SUM(wins)           AS wins,
    SUM(draws)          AS draws,
    SUM(losses)         AS losses,
    SUM(goals_scored)   AS goals_scored,
    SUM(goals_conceded) AS goals_conceded,
    SUM(goals_scored) - SUM(goals_conceded) AS goal_difference
FROM match_results
GROUP BY team
ORDER BY points DESC, goal_difference DESC