import sqlite3
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

#TODO: Add user functionality - done
#TODO: Delete user functionality - done
# TODO: Advanced skills querying


DB_NAME = "example8.db"
SQLITE_TYPES = {"null": None, "integer": int, "real": float, "text": str}

# conn = sqlite3.connect(DB_NAME)

# c = conn.cursor()
# c.row_factory = sqlite3.Row

# dict(zip([1,2,3,4], [a,b,c,d]))

# print(c.execute("SELECT * FROM users"))
# for i in c.execute("SELECT * FROM users"):
#     print(i.keys())
#     print(tuple(i))
#     print(dict(zip(i.keys(), tuple(i))))



# cursor = conn.cursor()
# cursor.row_factory = sqlite3.Row
# result = []
# for row in c.execute("SELECT * FROM users"):
#     user = dict(zip(row.keys(), tuple(row)))
#     skills = []
#     print(user["email"])
#     # print(tuple(user["email"]))
#     for row_skill in cursor.execute("SELECT name, rating FROM skills WHERE email = ?", [user["email"]]):
#         skills.append(tuple(row_skill))
#     user["skills"] = skills
#     result.append(user)
#
# print("RES", result)

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


## REFACTOR TO USE FOREIGN KEY
@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        result = []
        # print(c.execute("SELECT * FROM users"))
        # print([i for i in c.execute("SELECT * FROM users")])
        # all_users = c.execute("SELECT * FROM users").fetchall()
        # print([i for i in all_users])
        for row in c.execute("SELECT * FROM users").fetchall():
            user = dict(zip(row.keys(), tuple(row)))
            skills = []
            # print(user["email"])
            # print(tuple(user["email"]))
            skills = [dict(zip(row_skill.keys(), tuple(row_skill))) for row_skill in c.execute("SELECT name, rating FROM skills WHERE email = ?", [user["email"]]).fetchall()]

            # for row_skill in c.execute("SELECT name, rating FROM skills WHERE email = ?", [user["email"]]):
            #     skills.append(tuple(row_skill))
            user["skills"] = skills
            result.append(user)
        return jsonify(result)

@app.route('/users/<user_email>', methods=['GET'])
def get_user(user_email):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        query_result = c.execute("SELECT * FROM users WHERE email = ?", [user_email])
        # print(query_result.fetchall())
        results = query_result.fetchall()
        print("rc", query_result.rowcount)
        if len(results) == 0:
            return jsonify([])
        else:
            row = results[0]
            user = dict(zip(row.keys(), tuple(row)))
            user["skills"] = [dict(zip(row_skill.keys(), tuple(row_skill))) for row_skill in c.execute("SELECT name, rating FROM skills WHERE email = ?", [user["email"]]).fetchall()]
            return jsonify(user)

def check_if_exists(user_email):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        query_result = c.execute("SELECT * FROM users WHERE email = ?", [user_email])
        # print(query_result.fetchall())
        results = query_result.fetchall()
        print("rc", query_result.rowcount)
        if len(results) == 0:
            return False
        else:
            return True

# TODO: add skills
@app.route('/users/<user_email>', methods=['PUT'])
def update_user(user_email):
    print(user_email)
    print(request.get_json())
    print(request.get_data())
    if not check_if_exists(user_email):
        abort(400, "User with email address provided does not exist.")
    given_to_update = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        keys = {}
        for i in c.execute("PRAGMA table_info(users)").fetchall():
            print("i222", tuple(i))
            # Get column names not including primary key (email)
            if i[5] == 0:
                keys[i[1]] = SQLITE_TYPES[i[2]]
        print(keys)
        print([(j[0], type(j[1])) for j in given_to_update.items()])
        to_update = {}
        for j in given_to_update.items():
            print("j", j)
            if j[0] in keys:
                if type(j[1]) != keys[j[0]]:
                    print(j, "errror")
                    print(j[1], keys[j[0]])
                    abort(400, "Type of field '" + j[0] + "' does not match required type of " + keys[j[0]].__name__)
                    # return "ERROR"
                else:
                    to_update[j[0]] = j[1]
        # to_update = dict([j for j in given_to_update.items() if (j[0], type(j[1])) in keys])
        print(to_update)
        print("here")
        print(",".join([j[0] + " = ? " for j in to_update.items()]))
        print([j[1] for j in to_update.items()])

        if len(to_update) > 0:
            update_columns = ",".join([j[0] + " = ? " for j in to_update.items()])
            update_values = [j[1] for j in to_update.items()]
            update_values.append(user_email)
            c.execute("UPDATE users SET " + update_columns + " WHERE email = ?", update_values).fetchall()
        conn.commit()
    print(get_user(user_email) == [])
    return get_user(user_email)

# TODO: type checking - done
@app.route('/users/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        keys = {}
        for i in c.execute("PRAGMA table_info(users)").fetchall():
            print("i222", tuple(i))
            # Get column names including primary key
            keys[i[1]] = SQLITE_TYPES[i[2]]
        print(keys)
        for i in keys:
            if i not in data:
                abort(400, "Missing field: " + i)
            if keys[i] != type(data[i]):
                abort(400, "Incorrect type: " + i)
        if type(data["skills"]) != list:
            abort(400, "Skills must be a list.")

        skill_keys = {}
        for i in c.execute("PRAGMA table_info(skills)").fetchall():
            print("i222", tuple(i))
            # Get column names not including foreign key (email)
            if i[1] != "email":
                skill_keys[i[1]] = SQLITE_TYPES[i[2]]
        print("sk", skill_keys)
        for i in data["skills"]:
            if type(i) != dict:
                abort(400, "Skill information must be provided nested dictionaries.")

            for j in skill_keys:
                if j not in i:
                    abort(400, "Skill missing required field: " + j)
                if type(j) != type(i[j]):
                    abort(400, "Skill field of wrong type (must be string): " + j)

        try:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (data["email"], data["name"], data["picture"], data["company"], data["phone"], data["latitude"], data["longitude"]))
        except sqlite3.IntegrityError:
            abort(400, "User already in database: " + data["email"])
        for skill in data["skills"]:
            c.execute("INSERT INTO skills VALUES (?, ?, ?)", (data["email"], skill["name"], skill["rating"]))
    return get_user(data["email"])

@app.route('/users/<user_email>', methods=['DELETE'])
def delete_user(user_email):
    if not check_if_exists(user_email):
        abort(400, "User with specified email does not exist.")
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        c.execute("DELETE FROM users WHERE email = ?", [user_email])
        c.execute("DELETE FROM skills WHERE email = ?", [user_email])
    return "Deleted user successfully!", 200


@app.route('/skills', methods=['GET'])
def get_skills():
    args = request.args
    print(args)
    skill_name = None
    min_rating = None
    min_freq = None
    if "skill_name" in args:
        pass

    return jsonify([])

@app.route('/skills/<user_email>', methods=['GET'])
def get_skills_user(user_email):
    if not check_if_exists(user_email):
        abort(400, "User with email address provided does not exist.")
    args = request.args
    print(args)
    print(args["min_rating"])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        additional = ""
        values = [user_email]
        if "min_rating" in args:
            try:
                values.append(int(args["min_rating"]))
            except ValueError:
                abort(400, "min_rating must be an integer")
            additional += " AND rating >= ?"
        if "max_rating" in args:
            try:
                values.append(int(args["max_rating"]))
            except ValueError:
                abort(400, "max_rating must be an integer")
            additional += " AND rating <= ?"
        # final_result = []
        # for i in c.execute("SELECT name, rating FROM skills WHERE email = ?" + additional, values).fetchall()
        #     final_result.append()
        return jsonify([dict(zip(row_skill.keys(), tuple(row_skill))) for row_skill in c.execute("SELECT name, rating FROM skills WHERE email = ?" + additional, values).fetchall()])




@app.route('/skills/<skill_name>', methods=['GET'])
def get_skill_frequency(skill_name):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        query_result = c.execute("SELECT count(*) FROM skills WHERE name = ?", [skill_name])
        print(query_result)
        # print(query_result.fetchone()[0])
        return jsonify({"skill_frequency": query_result.fetchone()[0]})


if __name__ == '__main__':
    app.run(debug=True)

