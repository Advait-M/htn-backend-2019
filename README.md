# Documentation

## How to Populate the Database
A SQLite database is used to store the data of the users (hackathon attendees/applicants). This database is created and populated by the "populate_database.py" Python script. This script will pull the data from the specified JSON hosted in Firebase and add the data to the SQL database (creates a "htn.db" file if one does not exist already).

## Database Schema
The database consists of two tables: the "users" table and the "skills" table.

The users table contains all associated attributes of each user other than their skills. The user's email is used as a PRIMARY KEY (must be non-NULL and unique). The types of the fields are shown below:

![Users Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/users_table_schema.PNG)

The skills table contains the email associated with the user that has a particular skill (this is a FOREIGN KEY) in addition to the name of the skill and the rating. The types of these fields are shown below:

![Skills Schema](https://raw.githubusercontent.com/Advait-M/htn-backend-2019/master/img/skills_table_schema.PNG)

## Dependencies
The following Python libraries are used:
- sqlite3 (built-in)
- urllib (built-in)
- json (built-in)
- flask (pip)

These libraries are primarily used for interacting with the database, pulling data from the JSON and parsing it, and exposing data through a REST API. The language version used is Python 3.

## SQLite data types
- `NULL` - `NULL` value (represented as `None` in Python)
- `INTEGER` - an integer (represented as `int` in Python)
- `REAL` - a floating-point number (represented as `float` in Python
- `TEXT` - a text string (represented as `str` in Python)
- `BLOB` - a blob of data (stored exactly as the input), essentially a bunch of bytes so closest analogy to Python is most likely the `bytes` object

## Querying the API
To start the Flask server, simply run the `flask_queries.py` script. By default, Flask will attempt to host the server on `localhost:5000` but this can be changed. The examples below assume that `localhost:5000` is used. Note that the DB_NAME parameter can be configured at the top of the file. The database file must exist in the same directory and must be populated previously for the script to work correctly.

## API Endpoints with Examples

### Get all users (GET request)
Querying the `/users` endpoint will return a list of all users which contains their attributes in the JSON format that was inputted.

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
Querying the `/users/<user_email>` endpoint with a specific user's email will return the complete details of that user.

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
A POST request with a JSON body can be used to add a new user at the `/users/add_user` endpoint. The new user must have a new, unique email and must follow the specified format with regards to the fields of the JSON. If certain fields aren't specified or do not match the required types, a 400 HTTP error is returned with a short description outlining the reason why the request failed. If the request is successful, a 200 HTTP code is returned along with a JSON representing the user that has just been added.

Examples

Query: `localhost:5000/users/add_user`
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

### Delete user (DELETE request)
Querying the same endpoint for obtaining a specific user's details(`/users/<user_email>`), if we issue an HTTP DELETE request, we can delete the user from the database. If there are no users with the email address provided a 400 error will be returned.

Query: `localhost:5000/users/testexample@zizzle.com`

Example Result:
`Deleted user successfully!`

If we attempt to delete again, we get:
```HTML
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>User with specified email does not exist.</p>
```

### Update user (PUT request)
Again, querying the same endpoint for obtaining a specific user (`/users/<user_email>`), if we issue an HTTP PUT request, we can update certain fields for that user. The user must exist in the database, otherwise a 400 error will be returned. If any of the fields provided are not part of the columns within the `users` table then these key-value pairs are ignored. Any key-value pairs that are meant to update existing fields must match the specified type for that field, otherwise a 400 error will be returned. Note that all skills must adhere to the format specified as well, however, if new skills are specified then these skills will be added to the skills table (in addition to any existing skills being overwritten as needed, with new ratings). The updated user object is returned (all details).

Query: `localhost:5000/users/testexample@zizzle.com`

JSON Body:
```json
{
    "skills": [
    	{
            "name": "Go",
            "rating": "1"
        },
        {
            "name": "Public Speaking",
            "rating": "9"
        },
        {
            "name": "New Skill",
            "rating": "3"
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
            "rating": "1"
        },
        {
            "name": "Public Speaking",
            "rating": "9"
        },
        {
            "name": "New Skill",
            "rating": "3"
        }
    ]
}
```

On the other hand, if we attempt an invalid query such as using a string for a skill as opposed to an object:

Query: `localhost:5000/users/testexample@zizzle.com`
JSON body:
```json 
{
    "skills": [
    	"this_should_break",
    	{
            "name": "Go",
            "rating": "1"
        },
        {
            "name": "Public Speaking",
            "rating": "9"
        },
        {
            "name": "New Skill",
            "rating": "3"
        }
    ]
}
```

Example Result:
```HTML
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Skill information must be provided as nested objects with required fields.</p>
```

### Get skills for a specific user (GET request)
Querying the `/skills/<user_email>` yields a JSON specifying the skills of the user, with their respective names/ratings, if the email is valid (within the database). If it is not valid, a 400 error is returned with a short description. Additionally, a minimum and/or maximum rating can be specified, to restrict which skills are returned.

Query: `localhost:5000/skills/testexample@zizzle.com`

Example Result:
```json
[
    {
        "name": "Go",
        "rating": "1"
    },
    {
        "name": "Public Speaking",
        "rating": "9"
    },
    {
        "name": "New Skill",
        "rating": "3"
    }
]
```

With min_rating/max_rating parameters:

Query: `localhost:5000/skills/testexample@zizzle.com?min_rating=2&max_rating=7`

Example Result:
```json
[
    {
        "name": "New Skill",
        "rating": "3"
    }
]
```

### Get skill frequency (GET request)
Querying `/skills/frequency/<skill_name>` with a specific skill name returns the number of users that have that skill (skill frequency). Skills not within the database will have frequencies of 0.

Query: `localhost:5000/skills/frequency/C++`

Example Result:
```json
{
    "skill_frequency": 190
}
```

### Get skill average rating (GET request)
Querying `/skills/average/<skill_name>` with a specific skill name returns the average rating across all users for that specific skill. The skill must appear in the database at least once otherwise a 400 error will be returned with an appropriate description. 

Query: `localhost:5000/skills/average/C++`

Example Result:
```json
{
    "skill_frequency": 5.515789473684211
}
```


### Get all skills (GET request)
Querying `/skills` returns a JSON with all skills and their frequencies. Optional parameters for minimum and maximum frequencies can be added as well.

Query: `localhost:5000/skills`

Example Result:
```
[
    {
        "frequency": 192,
        "name": "Android"
    },
    {
        "frequency": 192,
        "name": "Angular"
    },
    {
        "frequency": 191,
        "name": "C"
    },
    {
        "frequency": 190,
        "name": "C++"
    },
    {
        "frequency": 180,
        "name": "Go"
    },
    {
        "frequency": 188,
        "name": "HTML/CSS"
    },
    {
        "frequency": 191,
        "name": "JS"
    },
    {
        "frequency": 206,
        "name": "Java"
    },
    {
        "frequency": 1,
        "name": "New Skill"
    },
    {
        "frequency": 196,
        "name": "NodeJS"
    },
    {
        "frequency": 185,
        "name": "Product Design"
    },
    {
        "frequency": 199,
        "name": "Public Speaking"
    },
    {
        "frequency": 223,
        "name": "iOS"
    }
]
```

Now, we can narrow down our range with minimum/maximum frequencies:

Query: `localhost:5000/skills?min_freq=190&max_freq=200`

Example Result:
```json
[
    {
        "frequency": 192,
        "name": "Android"
    },
    {
        "frequency": 192,
        "name": "Angular"
    },
    {
        "frequency": 191,
        "name": "C"
    },
    {
        "frequency": 190,
        "name": "C++"
    },
    {
        "frequency": 191,
        "name": "JS"
    },
    {
        "frequency": 196,
        "name": "NodeJS"
    },
    {
        "frequency": 199,
        "name": "Public Speaking"
    }
]
```








