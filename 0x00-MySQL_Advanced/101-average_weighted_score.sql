-- update all students

DELIMITER $$
BEGIN
	UPDATE users
    set average_score = (SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
    						INTO avg_weighted_score
    						FROM corrections
    						INNER JOIN projects ON corrections.project_id = projects.id
    						WHERE corrections.user_id = user_idi;
			)
END $$
DELIMITER ;

