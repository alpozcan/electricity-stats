\c home;

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- table: electricity
CREATE TABLE electricity
(
    "time" integer NOT NULL,
    "prod" smallint NOT NULL,
    "load" smallint NOT NULL,
    CONSTRAINT electricity_pkey PRIMARY KEY ("time")
);

-- ALTER TABLE electricity OWNER to electricity;
SELECT create_hypertable('electricity', 'time', chunk_time_interval => 2592000);
ALTER TABLE electricity SET (timescaledb.compress);
SELECT add_compression_policy('electricity', INTERVAL '90 days');
