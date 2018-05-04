# CREATE TABLE statements of the database

CREATE TABLE Account (

	id INTEGER PRIMARY KEY, 

	date_created DATETIME, 

	date_modified DATETIME, 

	name VARCHAR(50) NOT NULL, 

	username VARCHAR(50) NOT NULL, 

	password VARCHAR(50) NOT NULL, 

	role VARCHAR(50), 

);

CREATE TABLE Question (

	id INTEGER PRIMARY KEY,

	account_id INTEGER NOT NULL, 
 
	date_created DATETIME, 

	date_modified DATETIME, 

	name VARCHAR(200) NOT NULL, 

	category VARCHAR(20) NOT NULL, 

	difficulty VARCHAR(10) NOT NULL, 

	active BOOLEAN NOT NULL, 

	FOREIGN KEY(account_id) REFERENCES Account (id)

);

CREATE TABLE Quiz (

	id INTEGER PRIMARY KEY, 

	account_id INTEGER NOT NULL, 

	date_created DATETIME, 

	date_modified DATETIME, 

	name VARCHAR(200) NOT NULL, 

	category VARCHAR(20) NOT NULL, 

	active BOOLEAN NOT NULL, 

	automatic BOOLEAN NOT NULL, 

	FOREIGN KEY(account_id) REFERENCES Account (id)

);

CREATE TABLE Option (

	id INTEGER PRIMARY KEY,

	quest_id INTEGER NOT NULL,

	date_created DATETIME, 

	date_modified DATETIME, 

	name VARCHAR(200) NOT NULL, 

	correct BOOLEAN NOT NULL, 

	FOREIGN KEY(quest_id) REFERENCES Question (id)

);

CREATE TABLEPparticipation (

	id INTEGER PRIMARY KEY, 

	quiz_id INTEGER NOT NULL, 

	account_id INTEGER NOT NULL, 

	date_created DATETIME, 

	date_modified DATETIME, 

	FOREIGN KEY(quiz_id) REFERENCES Quiz (id), 

	FOREIGN KEY(account_id) REFERENCES Account (id)

);

CREATE TABLE Report (

	id INTEGER PRIMARY KEY, 

	account_id INTEGER NOT NULL, 

	question_id INTEGER NOT NULL, 

	date_created DATETIME, 

	date_modified DATETIME, 

	comment VARCHAR(200) NOT NULL, 

	checked BOOLEAN NOT NULL,

	FOREIGN KEY(account_id) REFERENCES Account (id), 

	FOREIGN KEY(question_id) REFERENCES Question (id)

);

CREATE TABLE Quiz_Question (

	id INTEGER PRIMARY KEY, 

	quiz_id INTEGER NOT NULL, 

	question_id INTEGER NOT NULL, 

	FOREIGN KEY(quiz_id) REFERENCES Quiz (id), 

	FOREIGN KEY(question_id) REFERENCES Question (id)

);

CREATE TABLE Users_Choice (

	id INTEGER PRIMARY KEY, 

	account_id INTEGER NOT NULL, 

	option_id INTEGER NOT NULL, 

	date_created DATETIME, 

	FOREIGN KEY(account_id) REFERENCES Account (id), 

	FOREIGN KEY(option_id) REFERENCES Option (id)

