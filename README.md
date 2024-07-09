# form-collect
A user-friendly system for form submission and aggregation, deployed across frontend and backend, allowing users to submit common data types like text, images, and signatures. Signatures are combined with a standardized agreement template and stored securely on the server.
## database deployment
use mysql database  
`CREATE DATABASE form;`  
`USE form;`  
```
CREATE TABLE `users` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`username` CHAR(64),
	`password` CHAR(64),
	PRIMARY KEY(`id`)
);
```
```
CREATE TABLE `submissions` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`text` TEXT(65535),
	`photoUuid` CHAR(128),
	`signUuid` CHAR(128),
	`username` CHAR(64),
	PRIMARY KEY(`id`)
);
```
initialize users table  
```INSERT INTO users (username, password) VALUES ('test', 'test');```

## front-end deployment
change `.env.example`in `form-collection-website` folder into `.env` and modify the content accordingly  
`cd form-collection-website`  
`npm install`  
`npm run serve`

## backend deployment
change `.env.example`in root directory into `.env` and modify the content accordingly  
`cd form-flask`    
`pip install -r requirements.txt`  
`python app.py`

## use
visit the url from front-end.The default username and password are both 'test'


