CREATE DEFINER=`iberlot`@`%` PROCEDURE IF NOT EXISTS get_mail_data (IN mail_id INT)
    BEGIN
    SELECT
        reportes_mail.subject, 
        reportes_mail.body, 
        reportes_mail.status, 
        reportes_mail.send_number, 
        reportes_mail.last_send, 
        reportes_mailcorp.name, 
        reportes_mailcorp.email, 
        reportes_mailcorp.password, 
        reportes_mailcorp.smtp, 
        reportes_mailcorp.smtp_port, 
        clientes.salutation, 
        clientes.first_name, 
        clientes.middle_name, 
        clientes.last_name, 
        clientes.lead_name, 
        clientes.source_information, 
        reportes_clientesemail.data, 
        clientes.company_name, 
        clientes.position, 
        auxiliares_type.name, 
        reportes_mailcorp.firma 
    FROM 
        reportes_mail 
        INNER JOIN reportes_mailcorp ON reportes_mailcorp.id = reportes_mail.mail_corp_id 
        INNER JOIN clientes ON clientes.id = reportes_mail.cliente_id 
        INNER JOIN reportes_clientesemail ON reportes_clientesemail.cliente_id = reportes_mail.cliente_id 
        INNER JOIN auxiliares_type ON auxiliares_type.id = clientes.type_id 
    WHERE 
        reportes_mail.id = mail_id 
        AND reportes_clientesemail.type_id = 1;
END;



CREATE PROCEDURE get_next_mail_to_send()
BEGIN
SELECT id FROM reportes_mailstosend WHERE approved = 1 AND send = 0 ORDER BY date_approved LIMIT 1;
END;



CREATE PROCEDURE get_next_mail_to_send()
BEGIN
SELECT
        reportes_mail.subject, 
        reportes_mail.body, 
        reportes_mail.status, 
        reportes_mail.send_number, 
        reportes_mail.last_send, 
        reportes_mailcorp.name, 
        reportes_mailcorp.email, 
        reportes_mailcorp.password, 
        reportes_mailcorp.smtp, 
        reportes_mailcorp.smtp_port, 
        clientes.salutation, 
        clientes.first_name, 
        clientes.middle_name, 
        clientes.last_name, 
        clientes.lead_name, 
        clientes.source_information, 
        reportes_clientesemail.data, 
        clientes.company_name, 
        clientes.position, 
        auxiliares_type.name, 
        reportes_mailcorp.firma 
    FROM 
        reportes_mail 
        INNER JOIN reportes_mailcorp ON reportes_mailcorp.id = reportes_mail.mail_corp_id 
        INNER JOIN clientes ON clientes.id = reportes_mail.cliente_id 
        INNER JOIN reportes_clientesemail ON reportes_clientesemail.cliente_id = reportes_mail.cliente_id 
        INNER JOIN auxiliares_type ON auxiliares_type.id = clientes.type_id 
    WHERE 
        reportes_mail.id = mail_id 
        AND reportes_clientesemail.type_id = (SELECT mail_id FROM reportes_mailstosend WHERE approved = 1 AND send = 0 ORDER BY date_approved LIMIT 1);
END;


CREATE DEFINER=`iberlot`@`%` PROCEDURE IF NOT EXISTS get_mail_attachment (IN mail_id INT)
    BEGIN
    SELECT * 
    FROM reportes_mail_attachment 
    INNER JOIN reportes_attachment ON reportes_attachment.id = reportes_mail_attachment.attachment_id 
    WHERE mail_id = id_mail;
END;
