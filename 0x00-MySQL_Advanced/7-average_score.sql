-- ComputeAverageScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE v_avg_score FLOAT;

    -- Compute average score for the user
    SELECT AVG(score) INTO v_avg_score
    FROM corrections as c
    WHERE c.user_id = user_id;

    -- Update the user's average score
    UPDATE users
    SET average_score = v_avg_score
    WHERE id = user_id;

END//

DELIMITER ;

