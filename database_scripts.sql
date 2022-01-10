CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS events (
    name VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    inserted_at timestamp DEFAULT now()
);

CREATE OR REPLACE FUNCTION fnsavestore()
    RETURNS trigger AS
$BODY$
BEGIN
    IF NEW.name='SaveStore' THEN
        INSERT INTO core_store (id, name, owner, balance, created_at, updated_at) 
            VALUES(uuid_generate_v4(), NEW.data->>'name', NEW.data->>'owner', (NEW.data->>'balance')::int, now(), now());
    ELSEIF NEW.name='SaveCNAB' THEN
        INSERT INTO core_cnabdocumentation (id, type, date, value, cpf, card, store_owner, store_name, created_at, updated_at)
            VALUES (
                uuid_generate_v4(),
                (NEW.data->>'type')::int,
                to_timestamp(NEW.data->>'date', 'YYYYMMDDHH24MISS'),
                (NEW.data->>'value')::int,
                NEW.data->>'cpf',
                NEW.data->>'card',
                NEW.data->>'store_owner',
                NEW.data->>'store_name',
                now(),
                now()
            );
    ELSEIF NEW.name='SaveFile' THEN
        UPDATE core_file SET status = (NEW.data->>'status')::int, updated_at = now()
        WHERE id = uuid(NEW.data->>'id');
    END IF;
        RETURN NEW;
EXCEPTION
    WHEN unique_violation THEN
    UPDATE core_store
        SET owner = NEW.data->>'owner', balance = balance + (NEW.data->>'balance')::int, updated_at = now()
        WHERE name = NEW.data->>'name';
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;

CREATE EXISTS TRIGGER savestore
    AFTER INSERT
    ON events
    FOR EACH ROW
    EXECUTE PROCEDURE fnsavestore();