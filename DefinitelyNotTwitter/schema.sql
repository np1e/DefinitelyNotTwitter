DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS flags;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS follows;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  descrip TEXT,
  password TEXT NOT NULL,
  admin INTEGER DEFAULT 0,
  registered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  avatar INTEGER DEFAULT 0
);

CREATE TABLE post (
  pid INTEGER PRIMARY KEY AUTOINCREMENT,
  uid INTEGER NOT NULL,
  content TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES user (id)
);

CREATE TABLE follows (
  fid INTEGER NOT NULL,
  uid INTEGER NOT NULL,
  PRIMARY KEY (fid, uid),
  FOREIGN KEY (fid) REFERENCES user (id),
  FOREIGN KEY (uid) REFERENCES user (id)
);

CREATE TABLE flags (
  uid INTEGER NOT NULL,
  flag TEXT NOT NULL,
  PRIMARY KEY (uid, flag),
  FOREIGN KEY (uid) REFERENCES user (id)
);
