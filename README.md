# Movies UGC service

## Major components

- Event storage - kafka
- Event API - loads events to event storage
- Database - Clickhouse
- ETL - loads events from event storage to database for analytical purposes (Kafka Table Engine)

## How to start app

Project uses makefiles to boot apps. There are mulltiple boot configurations: production and development.
The difference is that dev has open ports and separate volumes. Tests boot on dev environment.

### Production commands

- Up+build `make up-prod`
- Down `make down-prod`

### Development commands

- Up+build `make up-local`
- Down + remove volumes `make down-local`

## Contributors

- Vladimir Nikishov - T1rax - @nikishov.va
- Victoria Axentii - wiky-avis - @wikyavis
- Oleg Podryadov - opodryadov - @oleg_podryadov

test
