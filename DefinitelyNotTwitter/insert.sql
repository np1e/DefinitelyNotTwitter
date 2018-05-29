INSERT INTO user (name, password, admin, restricted)
VALUES
  ('admin', 'pbkdf2:sha256:50000$57uFc0vw$fabbfeaf3c249988a82d39e1a879af019c0de327a0fcf25dfe2a98050456e89b', 1, 0),
  ('test', 'pbkdf2:sha256:50000$57uFc0vw$fabbfeaf3c249988a82d39e1a879af019c0de327a0fcf25dfe2a98050456e89b', 0, 0),
  ('test1', 'pbkdf2:sha256:50000$57uFc0vw$fabbfeaf3c249988a82d39e1a879af019c0de327a0fcf25dfe2a98050456e89b', 0, 1),
  ('test2', 'pbkdf2:sha256:50000$57uFc0vw$fabbfeaf3c249988a82d39e1a879af019c0de327a0fcf25dfe2a98050456e89b', 0, 0);

INSERT INTO post (uid, content, reviewed)
VALUES
  (2, "Dies ist ein Testpost. Lorem ipsum blablabla.", 0),
  (3, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel. Iusto ludus pro ad. Consequat prodesset no eum, eu quis alienum usu. Id nam wisi ceteros democritum, nec tation ignota ad. An per appetere liberavisse.", 0),
  (3, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 1),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 1),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (3, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (2, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (2, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (2, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (1, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (2, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 1),
  (2, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (1, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0),
  (4, "Lorem ipsum dolor sit amet, vim ne vidisse intellegam honestatis, quo et dico lucilius. Nonumy malorum persequeris cu mel.", 0);

INSERT INTO follows (fid, uid)
VALUES
  (1,2),
  (1,3),
  (1,4),
  (2,3),
  (3,4),
  (2,1),
  (4,2);
