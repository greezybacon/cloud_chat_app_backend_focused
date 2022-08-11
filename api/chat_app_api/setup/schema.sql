CREATE SCHEMA IF NOT EXISTS chat;

CREATE TABLE IF NOT EXISTS chat.user (
    id SERIAL,
    username TEXT,
    PRIMARY KEY (id),
    UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS chat.room (
    id SERIAL,
    name TEXT NOT NULL,
    creator INT REFERENCES chat.user(id),
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS chat.message (
    id          SERIAL,
    poster      INT REFERENCES chat.user(id),
    room        INT REFERENCES chat.room(id),
    posted_at   TIMESTAMPTZ,
    content     TEXT,
    PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS messages_for_room ON chat.message (room, posted_at DESC);