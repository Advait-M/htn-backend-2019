# Documentation

## How to Populate the Database
A SQLite database is used to store the data of the users (hackathon attendees/applicants). This database is created and populated by the "populate_database.py" Python script. This script will pull the data from the specified JSON hosted in Firebase and add the data to the SQL database (creates a "htn.db" file if one does not exist already).

## Database Schema
The database consists of two tables: the "users" table and the "skills" table.

The users table contains all associated attributes of each user other than their skills. The user's email is used as a PRIMARY KEY (must be non-NULL and unique). The types of the fields are shown below:

![Users Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/users_table_schema.PNG)

The skills table contains the email associated with the user that has a particular skill (this is a FOREIGN KEY) in addition to the name of the skill and the rating. The types of these fields are shown below:

![Skills Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/skills_table_schema.PNG)

## API Endpoints

### Get all users
Qeurying the /users endpoint will return a list of all users which contains their attributes in the JSON format that was inputted. For example:
Query: "localhost:5000/users"
Example Partial Result:
```json
[
    {
        "company": "Slambda",
        "email": "elizawright@slambda.com",
        "latitude": 48.4862,
        "longitude": -34.7754,
        "name": "Jenna Luna",
        "phone": "+1 (913) 504-2495",
        "picture": "http://lorempixel.com/200/200/sports/8",
        "skills": [
            {
                "name": "JS",
                "rating": "5"
            },
            {
                "name": "Go",
                "rating": "5"
            }
        ]
    },
    {
        "company": "Veraq",
        "email": "jennaluna@veraq.com",
        "latitude": 48.9743,
        "longitude": -34.1247,
        "name": "Dora Schultz",
        "phone": "+1 (949) 580-2608",
        "picture": "http://lorempixel.com/200/200/sports/0",
        "skills": [
            {
                "name": "C",
                "rating": "7"
            },
            {
                "name": "Android",
                "rating": "9"
            },
            {
                "name": "Android",
                "rating": "2"
            }
        ]
    },
    {
        "company": "Zizzle",
        "email": "doraschultz@zizzle.com",
        "latitude": 49.1174,
        "longitude": -35.0231,
        "name": "Sheri Cunningham",
        "phone": "+1 (949) 548-2223",
        "picture": "http://lorempixel.com/200/200/sports/5",
        "skills": [
            {
                "name": "Go",
                "rating": "9"
            },
            {
                "name": "Public Speaking",
                "rating": "5"
            }
        ]
    }
```

