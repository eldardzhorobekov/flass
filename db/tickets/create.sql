CREATE TABLE IF NOT EXISTS flass.tickets (
    id SERIAL PRIMARY KEY,
    chat_id TEXT NOT NULL,
    chat_name TEXT NOT NULL,
    message_id TEXT NOT NULL,
    route_from TEXT NOT NULL,
    posted_at timestamp with time zone,
    route_to TEXT NOT NULL,
    date_start timestamp with time zone NOT NULL,
    date_end timestamp with time zone,
    price FLOAT NOT NULL,
    currency TEXT NOT NULL,
    airline TEXT,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);