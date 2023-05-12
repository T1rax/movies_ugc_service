CREATE DATABASE IF NOT EXISTS ugc;

CREATE TABLE IF NOT EXISTS ugc.user_progress
(
    user_id String,
	film_id String,
	viewed_frame Int32,
	event_time String
) ENGINE = MergeTree ORDER BY (user_id, film_id);

CREATE TABLE IF NOT EXISTS ugc.user_progress_queue
(
    user_id String,
    film_id String,
    viewed_frame Int32,
	event_time String
) ENGINE = Kafka('localhost:9092', 'my_topic', 'my_group', 'JSONEachRow');

CREATE MATERIALIZED VIEW ugc.user_progress_mv TO ugc.user_progress AS
SELECT *
FROM ugc.user_progress_queue;