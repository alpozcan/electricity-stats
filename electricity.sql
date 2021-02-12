\c home;

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- table: electricity
CREATE TABLE electricity
(
    "time" timestamp with time zone NOT NULL,
    "prod" smallint NOT NULL,
    "load" smallint NOT NULL,
    CONSTRAINT electricity_pkey PRIMARY KEY ("time", ticker)
);

-- ALTER TABLE electricity OWNER to electricity;
SELECT create_hypertable('electricity', 'time');
ALTER TABLE electricity SET (timescaledb.compress);
SELECT add_compression_policy('electricity', INTERVAL '7 days');
