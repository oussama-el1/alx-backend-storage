-- trigger that decreases the quantity of an item after adding a new order. 
DELIMITER //

CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - 1
    WHERE name = NEW.item_name;
END;
//

DELIMITER ;

