CREATE TABLE users (
  userId SERIAL PRIMARY KEY,
  userName  TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE logs (
  logId SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES users(userId),
  date DATE NOT NULL,
  requestType TEXT NOT NULL,
  content TEXT,
  response TEXT
);
