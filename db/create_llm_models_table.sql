CREATE TABLE llm_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    config_json JSON NOT NULL,
    description TEXT
);
