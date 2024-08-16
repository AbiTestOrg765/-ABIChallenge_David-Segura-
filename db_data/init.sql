CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  user_name  TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE logs (
  log_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(userId),
  date DATE NOT NULL,
  end_point TEXT NOT NULL,
  request_type TEXT NOT NULL,
  content TEXT,
  response TEXT
);

INSERT INTO users (user_name, password)
VALUES ('david', 'just_password');

INSERT INTO users (user_name, password)
VALUES ('some_one', 'just_password2');