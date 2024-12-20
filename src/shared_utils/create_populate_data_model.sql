-- Table: Campaign
CREATE TABLE campaign (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) CHECK (Type IN ('Sponsorship', 'Standard')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    advertiser VARCHAR(255) NOT NULL,
    impressions_delivered BIGINT DEFAULT 0,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the rule was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of when the rule was last updated
);

-- Table: LineItem
CREATE TABLE line_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    type VARCHAR(50) CHECK (Type IN ('Sponsorship', 'Standard')),
    skippable_ad BOOLEAN DEFAULT FALSE,
    impressions_delivered BIGINT DEFAULT 0,
    impression_goal BIGINT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    priority_level INTEGER CHECK (priority_level >= 1 AND priority_level <= 10),
    delivery_type VARCHAR(50) CHECK (delivery_type IN ('Even', 'AFAP')),
    bookies TEXT[],
    cpm NUMERIC(10, 2),
    pacing_osi NUMERIC(5, 2),
    targetting_attributes JSONB,
    creative_dimensions JSONB,
    vast_error_codes JSONB,
    ad_unit_mapping JSONB,
    assets_assigned TEXT[],
    platform VARCHAR(50) CHECK (platform IN ('Youtube', 'SPP')),
    fill_rate NUMERIC(5, 2),
    campaign_id INTEGER NOT NULL REFERENCES campaign(id) ON DELETE CASCADE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the rule was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of when the rule was last updated
);

-- Table: SPP
CREATE TABLE spp (
    id SERIAL PRIMARY KEY,
    spp_partner_name VARCHAR(255) NOT NULL,
    impressions_delivered BIGINT DEFAULT 0,
    ad_requests BIGINT DEFAULT 0,
    fill_rate NUMERIC(5, 2),
    category VARCHAR(255),
    tier VARCHAR(50),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the rule was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of when the rule was last updated
);

CREATE TABLE rule_definitions (
    id SERIAL PRIMARY KEY,           -- Unique identifier for each rule
    type VARCHAR(255) NOT NULL,       -- The category or classification of the rule
    rule JSONB NOT NULL,              -- The actual rule definition stored as a JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the rule was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of when the rule was last updated
);


DO $$ 
DECLARE
    i INT := 1;
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO campaign (name, type, start_date, end_date, advertiser, impressions_delivered)
        VALUES (
            'Campaign ' || i, 
            CASE WHEN i % 2 = 0 THEN 'Sponsorship' ELSE 'Standard' END,
            CURRENT_DATE - (i * 10) % 365, 
            CURRENT_DATE + (i * 15) % 365, 
            'Advertiser ' || i, 
            (i * 1000) % 100000
        );
    END LOOP;
END $$;


DO $$ 
DECLARE
    i INT := 1;
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO line_item (
            order_id, 
            name, 
            status, 
            type, 
            skippable_ad, 
            impressions_delivered, 
            impression_goal, 
            start_date, 
            end_date, 
            priority_level, 
            delivery_type, 
            bookies, 
            cpm, 
            pacing_osi, 
            targetting_attributes, 
            creative_dimensions, 
            vast_error_codes, 
            ad_unit_mapping, 
            assets_assigned, 
            platform, 
            fill_rate, 
            campaign_id
        ) VALUES (
            i, 
            'Line Item ' || i, 
            CASE WHEN i % 2 = 0 THEN 'Active' ELSE 'Inactive' END, 
            CASE WHEN i % 2 = 0 THEN 'Sponsorship' ELSE 'Standard' END, 
            i % 2 = 0, 
            (i * 500) % 100000, 
            (i * 300) % 10000, 
            CURRENT_DATE - (i * 5) % 365, 
            CURRENT_DATE + (i * 10) % 365, 
            (i % 10) + 1, 
            CASE WHEN i % 2 = 0 THEN 'Even' ELSE 'AFAP' END, 
            ARRAY['Bookie' || (i % 5)], 
            RANDOM() * 100, 
            RANDOM() * 10, 
            '{"key": "value"}', 
            '{"dimension": "value"}', 
            '{"error": "none"}', 
            '{"ad_unit": "value"}', 
            ARRAY['Asset' || (i % 3)], 
            CASE WHEN i % 2 = 0 THEN 'Youtube' ELSE 'SPP' END, 
            RANDOM() * 100, 
            (i % 100) + 1
        );
    END LOOP;
END $$;

DO $$ 
DECLARE
    i INT := 1;
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO spp (
			spp_partner_name,
			impressions_delivered,
			ad_requests,
			fill_rate,
			category,
			tier
		) VALUES (
			'SPP Partner ' || i,
			(i * 1000) % 50000,
			(i * 2000) % 60000,
			RANDOM() * 100,  -- Remove unnecessary type casting
			'Category ' || (i % 5),
			CASE WHEN i % 2 = 0 THEN 'Gold' ELSE 'Silver' END
		);
    END LOOP;
END $$;


DO $$
DECLARE
    i INT := 1;
    random_name TEXT;
    random_priority INT;
    random_condition_type TEXT;
    random_field1 TEXT;
    random_field2 TEXT;
    random_operator1 TEXT;
    random_operator2 TEXT;
    random_value1 INT;
    random_value2 INT;
    random_target_field1 TEXT;
    random_expression TEXT;
BEGIN
    FOR i IN 1..20 LOOP
        -- Generate random values for the rule structure
        random_name := 'xpto_' || floor(random() * 1000)::TEXT;
        random_priority := floor(random() * 10)::INT;
        random_condition_type := CASE WHEN random() < 0.5 THEN 'all' ELSE 'any' END;
        random_field1 := CASE floor(random() * 5)
            WHEN 0 THEN 'impressions_delivered'
            WHEN 1 THEN 'impression_goal'
            WHEN 2 THEN 'priority_level'
            WHEN 3 THEN 'pacing_osi'
            WHEN 4 THEN 'delivery_type'
        END;
        random_field2 := CASE floor(random() * 5)
            WHEN 0 THEN 'impressions_delivered'
            WHEN 1 THEN 'impression_goal'
            WHEN 2 THEN 'priority_level'
            WHEN 3 THEN 'pacing_osi'
            WHEN 4 THEN 'delivery_type'
        END;
        random_operator1 := CASE floor(random() * 4)
            WHEN 0 THEN '=='
            WHEN 1 THEN '!='
            WHEN 2 THEN '>'
            WHEN 3 THEN '<'
        END;
        random_operator2 := CASE floor(random() * 4)
            WHEN 0 THEN '=='
            WHEN 1 THEN '!='
            WHEN 2 THEN '>'
            WHEN 3 THEN '<'
        END;
        random_value1 := floor(random() * 100)::INT;
        random_value2 := floor(random() * 100)::INT;
        -- Randomly select a target field
        random_target_field1 := CASE floor(random() * 4)
            WHEN 0 THEN 'impressions_delivered'
            WHEN 1 THEN 'impression_goal'
            WHEN 2 THEN 'priority_level'
            WHEN 3 THEN 'pacing_osi'
        END;

        -- Dynamically construct the expression based on the target field
        random_expression := CASE random_target_field1
            WHEN 'impressions_delivered' THEN 'impressions_delivered - 500'
            WHEN 'impression_goal' THEN 'impression_goal + 100'
            WHEN 'priority_level' THEN 'priority_level + 1'
            WHEN 'pacing_osi' THEN 'pacing_osi + 10'
        END;

        -- Insert the rule into the rule_definitions table
        INSERT INTO rule_definitions (type, rule)
        VALUES (
            'Rule ' || i,
            jsonb_build_object(
                'name', random_name,
                'priority', random_priority,
                'condition', jsonb_build_object(
                    random_condition_type, jsonb_build_array(
                        jsonb_build_object(
                            'field', random_field1,
                            'operator', random_operator1,
                            'value', random_value1
                        ),
                        jsonb_build_object(
                            'field', random_field2,
                            'operator', random_operator2,
                            'value', random_value2
                        )
                    )
                ),
                'actions', jsonb_build_array(
                    jsonb_build_object(
                        'type', 'update',
                        'target_field', random_target_field1,
                        'expression', random_expression
                    ),
                    jsonb_build_object(
                        'type', 'redistribute',
                        'params', jsonb_build_object(
                            'target_campaign', 'current',
                            'redistribute_to', 'line_items',
                            'criteria', jsonb_build_object(
                                'field', 'pacing_osi',
                                'operator', '>',
                                'value', 1
                            ),
                            'amount', 5000
                        )
                    )
                )
            )
        );
    END LOOP;
END $$;

ALTER SEQUENCE rule_definitions_id_seq RESTART WITH 1;
