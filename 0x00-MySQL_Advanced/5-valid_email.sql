-- valid email after change
DELIMITER $$
CREATE TRIGGER valid_email_trg
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$$
DELIMITER ;
