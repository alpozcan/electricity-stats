# electricity-stats
Pulls solar electricity production and consumption values from a Fronius Primo inverter's JSON API and writes into a PostgreSQL database.

```
├── collector.py : The main script that fetches data and inserts into a database
├── db : Contains SQL Schema files for PostgeSQL / TimescaleDB
│   ├── electricity.sql
│   └── home.sql
└── electricity-stats-collector.service : systemd unit file for running as a service
```

