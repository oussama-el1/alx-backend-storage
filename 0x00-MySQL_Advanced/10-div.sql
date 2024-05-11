-- safe division

DELIMITER //

CREATE PROCEDURE SafeDiv(IN a INT, IN b INT, OUT result INT)
BEGIN
    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = a / b;
    END IF;
END //

DELIMITER ;

