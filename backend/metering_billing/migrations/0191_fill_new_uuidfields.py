# Generated by Django 4.0.5 on 2023-02-18 20:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metering_billing", "0190_alter_customer_uuidv5_customer_id_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            """CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""",
        ),
        migrations.RunSQL(
            [
                """
            BEGIN;
            -- Add columns
            ALTER TABLE metering_billing_usageevent ADD COLUMN uuidv5_customer_id UUID NULL;
            ALTER TABLE metering_billing_usageevent ADD COLUMN uuidv5_event_name UUID NULL;
            ALTER TABLE metering_billing_usageevent ADD COLUMN uuidv5_idempotency_id UUID NULL;

            -- Populate uuidv5_customer_id with UUIDv5 hash of cust_id
            UPDATE metering_billing_usageevent
            SET uuidv5_customer_id = uuid_generate_v5('D1337E57-E6A0-4650-B1C3-D6487AFFB8CA'::uuid, cust_id)
            WHERE customer_id IS NOT NULL;

            -- Populate uuidv5_event_name with UUIDv5 hash of event_name
            UPDATE metering_billing_usageevent
            SET uuidv5_event_name = uuid_generate_v5('843D7005-63DE-4B72-B731-77E2866DCCFF'::uuid, event_name)
            WHERE event_name IS NOT NULL;

            -- Populate uuidv5_idempotency_id with UUIDv5 hash of idempotency_id
            UPDATE metering_billing_usageevent
            SET uuidv5_idempotency_id = uuid_generate_v5('904C0FFB-7005-414E-9B7D-8E3C5DDE266D'::uuid,idempotency_id)
            WHERE idempotency_id IS NOT NULL;

            -- Modify columns to be non-nullable
            ALTER TABLE metering_billing_usageevent ALTER COLUMN uuidv5_customer_id SET NOT NULL;
            ALTER TABLE metering_billing_usageevent ALTER COLUMN uuidv5_event_name SET NOT NULL;
            ALTER TABLE metering_billing_usageevent ALTER COLUMN uuidv5_idempotency_id SET NOT NULL;

            -- Create index
            DROP INDEX IF EXISTS metering_billing_usageevent_time_created_idx;
            CREATE INDEX metering_billing_usageevent_time_created_idx ON metering_billing_usageevent (time_created DESC, uuidv5_event_name, uuidv5_customer_id);

            COMMIT;
        """,
            ],
        ),
        migrations.RunSQL(
            [
                """
            CREATE OR REPLACE FUNCTION update_uuid_fields_function() RETURNS TRIGGER AS $$
            BEGIN
                NEW.uuidv5_customer_id := uuid_generate_v5('D1337E57-E6A0-4650-B1C3-D6487AFFB8CA'::uuid, NEW.cust_id);
                NEW.uuidv5_event_name := uuid_generate_v5('843D7005-63DE-4B72-B731-77E2866DCCFF'::uuid, NEW.event_name);
                NEW.uuidv5_idempotency_id := uuid_generate_v5('904C0FFB-7005-414E-9B7D-8E3C5DDE266D'::uuid, NEW.idempotency_id);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """,
            ]
        ),
        migrations.RunSQL(
            """
            CREATE TRIGGER update_uuid_fields_trigger
            BEFORE INSERT OR UPDATE ON metering_billing_usageevent
            FOR EACH ROW
            EXECUTE FUNCTION update_uuid_fields_function();
        """
        ),
    ]
