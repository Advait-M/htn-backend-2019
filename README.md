# Documentation

## How to Populate the Database
A SQLite database is used to store the data of the users (hackathon attendees/applicants). This database is created and populated by the "populate_database.py" Python script. This script will pull the data from the specified JSON hosted in Firebase and add the data to the SQL database (creates a "htn.db" file if one does not exist already).

## Database Schema
The database consists of two tables: the "users" table and the "skills" table.

The users table contains all associated attributes of each user other than their skills. The user's email is used as a PRIMARY KEY (must be non-NULL and unique). The types of the fields are shown below:

![Users Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/users_table_schema.PNG)

The skills table contains the email associated with the user that has a particular skill (this is a FOREIGN KEY) in addition to the name of the skill and the rating. The types of these fields are shown below:

![Skills Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/skills_table_schema.PNG)
