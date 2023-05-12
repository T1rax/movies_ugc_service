# Movies UGC service

## Major components

- Event storage - kafka
- Event API - loads events to event storage
- Database - Clickhouse
- ETL - loads events from event storage to database for analytical purposes (Kafka Table Engine)

## How to start app

Project uses makefiles to boot apps. Each makefile command relates to specific part off the app

- Start everything - `make docker-up-all`
- Event storage - `make docker-up-events`
- Database - `make docker-up-db`
- Event API - `make docker-up-api`

## Contributors

- Vladimir Nikishov - T1rax - @nikishov.va
- Victoria Axentii - wiky-avis - @wikyavis
- Oleg Podryadov - opodryadov - @oleg_podryadov
