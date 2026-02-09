CREATE TABLE IF NOT EXISTS flass.tickets (
    id SERIAL PRIMARY KEY,
    chat_id TEXT NOT NULL,
    chat_name TEXT NOT NULL,
    route_from TEXT NOT NULL,
    route_to TEXT NOT NULL,
    date_start TIMESTAMP NOT NULL,
    date_end TIMESTAMP,
    price FLOAT NOT NULL,
    currency TEXT NOT NULL,
    airline TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
