DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name varchar(125),
    IN p_lastName varchar(125),
    IN p_email varchar(100),
    IN p_mobile varchar(25),
    IN p_address text,
    IN p_sid int(11),
    IN p_password varchar(100)
)
BEGIN
    IF ( select exists (select 1 from users where firstName = p_name) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into users
        (
            sid,
            firstName,
            lastName,
            password,
            email,
            mobile,
            address


        )
        values
        (
            p_sid,
            p_name,
            p_lastName,
            p_password,
            p_email,
            p_mobile,
            p_address


        );
     
    END IF;

END$$
DELIMITER ;










DELIMITER //

CREATE TRIGGER order_det
BEFORE INSERT
   ON orddetails FOR EACH ROW

BEGIN

   DECLARE vUser varchar(50);

   -- Find username of person performing INSERT into table
   SELECT id from orders order by id desc limit 1 INTO vUser;

   -- Update create_date field to current system date
   

   -- Update created_by field to the username of the person performing the INSERT
   SET NEW.ord_id = vUser;

END; //

DELIMITER ;



+---------------------------------------------
| BEGIN
    
+---------------------------------------------



DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_email VARCHAR(100)
)
BEGIN

    select * from users where email = p_email;

END$$
DELIMITER ;