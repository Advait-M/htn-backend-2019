# Documentation

## How to Populate the Database
A SQLite database is used to store the data of the users (hackathon attendees/applicants). This database is created and populated by the "populate_database.py" Python script. This script will pull the data from the specified JSON hosted in Firebase and add the data to the SQL database (creates a "htn.db" file if one does not exist already).

## Database Schema
The database consists of two tables: the "users" table and the "skills" table.

The users table contains all associated attributes of each user other than their skills. The user's email is used as a PRIMARY KEY (must be non-NULL and unique). The types of the fields are shown below:

![Users Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/users_table_schema.PNG)

The skills table contains the email associated with the user that has a particular skill (this is a FOREIGN KEY) in addition to the name of the skill and the rating. The types of these fields are shown below:

![Skills Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/skills_table_schema.PNG)

## API Endpoints with Examples

### Get all users (GET request)
Querying the /users endpoint will return a list of all users which contains their attributes in the JSON format that was inputted.

Example

Query: `localhost:5000/users`

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
    }
```

### Get specific user (GET request)
Querying the /users/<user_email> endpoint with a specific user's email will return the complete details of that user.

Example

Query: `localhost:5000/users/tonibright@nixelt.com`

Example Result:
```json
{
    "company": "Nixelt",
    "email": "tonibright@nixelt.com",
    "latitude": 49.34,
    "longitude": -35.9086,
    "name": "Puckett Fletcher",
    "phone": "+1 (895) 552-3464",
    "picture": "http://lorempixel.com/200/200/sports/3",
    "skills": [
        {
            "name": "C++",
            "rating": "6"
        }
    ]
}
```

### Add user (POST request)
A POST request with a JSON body can be used to add a new user. The new user must have a new, unique email and must follow the specified format with regards to the fields of the JSON. If certain fields aren't specified or do not match the required types, a 400 HTTP error is returned with a short description outlining the reason why the request failed. If the request is successful, a 200 HTTP code is returned along with a JSON representing the user that has just been added.

Examples

Query: `http://127.0.0.1:5000/users/add_user`
JSON Body:
```json
{
    "company": "TestCompany",
    "email": "testexample@zizzle.com",
    "latitude": 48.9288,
    "longitude": -35.0231,
    "name": "Test Example",
    "phone": "+2 (555) 123 4567",
    "picture": "http://lorempixel.com/200/200/sports/5",
    "skills": [
        {
            "name": "Go",
            "rating": "10"
        },
        {
            "name": "Public Speaking",
            "rating": "5"
        }
    ]
}
```

Example Result:
```json
{
    "company": "TestCompany",
    "email": "testexample@zizzle.com",
    "latitude": 48.9288,
    "longitude": -35.0231,
    "name": "Test Example",
    "phone": "+2 (555) 123 4567",
    "picture": "http://lorempixel.com/200/200/sports/5",
    "skills": [
        {
            "name": "Go",
            "rating": "10"
        },
        {
            "name": "Public Speaking",
            "rating": "5"
        }
    ]
}
```

If we attempt to add the same user (duplicate email) again, we get:
Query: Same as above

Example Result:
```HTML
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>User already in database: testexample@zizzle.com</p>
```





