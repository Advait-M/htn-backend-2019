import sqlite3
from flask import Flask, jsonify, request, abort

# Database file name
DB_NAME = "src/htn.db"
# Maps SQLite data types to Python types
SQLITE_TYPES = {"null": None, "integer": int, "real": float, "text": str}

# Initialize Flask app
app = Flask(__name__)


@app.route('/')
def index():
    """Welcome page for the API."""
    return "Welcome to Advait's Hack the North Backend Challenge 2019. Feel free to explore the various endpoints!", 200


@app.route('/users', methods=['GET'])
def get_users():
    """Get all users and their associated information from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        result = []

        for row in c.execute("SELECT * FROM users").fetchall():
            user = dict(zip(row.keys(), tuple(row)))

            user["skills"] = [dict(zip(row_skill.keys(), tuple(row_skill))) for row_skill in c.execute(
                "SELECT name, rating FROM skills WHERE email = ?", [user["email"]]).fetchall()]

            result.append(user)

        return jsonify(result)


@app.route('/users/<user_email>', methods=['GET'])
def get_user(user_email):
    """Get a specific user's details (lookup by email)."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        query_result = c.execute(
            "SELECT * FROM users WHERE email = ?",
            [user_email])

        results = query_result.fetchall()

        if len(results) == 0:
            return jsonify([])
        else:
            row = results[0]
            user = dict(zip(row.keys(), tuple(row)))
            user["skills"] = [dict(zip(row_skill.keys(), tuple(row_skill))) for row_skill in c.execute(
                "SELECT name, rating FROM skills WHERE email = ?", [user["email"]]).fetchall()]

            return jsonify(user)


def check_if_exists(user_email):
    """Check if a user exists (lookup by email)."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        query_result = c.execute(
            "SELECT * FROM users WHERE email = ?",
            [user_email])

        results = query_result.fetchall()

        if len(results) == 0:
            return False
        else:
            return True


@app.route('/users/<user_email>', methods=['PUT'])
def update_user(user_email):
    """
    Update user with specified key-value pairs. Must match appropriate field types.
    Any extra fields are ignored. New skills are added if needed.
    """
    if not check_if_exists(user_email):
        abort(400, "User with email address provided does not exist.")

    given_to_update = request.get_json()

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        keys = {}
        for i in c.execute("PRAGMA table_info(users)").fetchall():
            # Get column names not including primary key (email)
            if i[5] == 0:
                keys[i[1]] = SQLITE_TYPES[i[2]]

        # We ignore any extra fields
        to_update = {}
        for j in given_to_update.items():
            if j[0] in keys:
                if not isinstance(j[1], keys[j[0]]):
                    abort(400, "Type of field '" +
                          j[0] +
                          "' does not match required type of " +
                          keys[j[0]].__name__)
                else:
                    to_update[j[0]] = j[1]

        if "skills" in given_to_update:
            validate_skills(given_to_update)
            for i in given_to_update["skills"]:
                c.execute(
                    "DELETE FROM skills WHERE email = ? AND name = ?", [
                        user_email, i["name"]])
                c.execute(
                    "INSERT INTO skills VALUES (?, ?, ?)", [
                        user_email, i["name"], i["rating"]])

        if len(to_update) > 0:
            update_columns = ",".join(
                [j[0] + " = ? " for j in to_update.items()])
            update_values = [j[1] for j in to_update.items()]
            update_values.append(user_email)
            c.execute(
                "UPDATE users SET " +
                update_columns +
                " WHERE email = ?",
                update_values).fetchall()

        conn.commit()

    return get_user(user_email)


def validate_skills(data):
    """Validates schema of skills array."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        skill_keys = {}
        for i in c.execute("PRAGMA table_info(skills)").fetchall():
            # Get column names not including foreign key (email)
            if i[1] != "email":
                skill_keys[i[1]] = SQLITE_TYPES[i[2]]

        for i in data["skills"]:
            if not isinstance(i, dict):
                abort(
                    400, "Skill information must be provided as nested objects with required fields.")

            for j in skill_keys:
                if j not in i:
                    abort(400, "Skill missing required field: " + j)
                if not isinstance(j, type(i[j])):
                    abort(
                        400, "Skill field of wrong type (must be string): " + j)


@app.route('/users/add_user', methods=['POST'])
def add_user():
    """Add user (must be new, unique email) with specified details."""
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        keys = {}
        for i in c.execute("PRAGMA table_info(users)").fetchall():
            # Get column names including primary key
            keys[i[1]] = SQLITE_TYPES[i[2]]

        for i in keys:
            if i not in data:
                abort(400, "Missing field: " + i)
            if not isinstance(data[i], keys[i]):
                abort(400, "Incorrect type: " + i)
        if not isinstance(data["skills"], list):
            abort(400, "Skills must be a list.")

        validate_skills(data)
        try:
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data["email"],
                 data["name"],
                    data["picture"],
                    data["company"],
                    data["phone"],
                    data["latitude"],
                    data["longitude"]))
        except sqlite3.IntegrityError:
            abort(400, "User already in database: " + data["email"])
        for skill in data["skills"]:
            c.execute("INSERT INTO skills VALUES (?, ?, ?)",
                      (data["email"], skill["name"], skill["rating"]))

        conn.commit()

    return get_user(data["email"])


@app.route('/users/<user_email>', methods=['DELETE'])
def delete_user(user_email):
    """Delete specified user (found by email)."""
    if not check_if_exists(user_email):
        abort(400, "User with specified email does not exist.")
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        c.execute("DELETE FROM users WHERE email = ?", [user_email])
        c.execute("DELETE FROM skills WHERE email = ?", [user_email])

        conn.commit()

    return "Deleted user successfully!", 200


@app.route('/skills', methods=['GET'])
def get_skills():
    """
    Get all skills with their associated skill frequencies.
    Optional parameters to specify minimum/maximum frequency.
    """
    args = request.args
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        try:
            min_freq = int(args["min_freq"]) if "min_freq" in args else 1
        except ValueError:
            abort(400, "Minimum frequency specified must be an integer.")

        condition = "COUNT(*) >= ?"
        values = [min_freq]

        if "max_freq" in args:
            try:
                max_freq = int(args["max_freq"])
            except ValueError:
                abort(400, "Maximum frequency specified must be an integer.")
            condition += " AND COUNT(*) <= ?"
            values.append(max_freq)

        result = []

        for row in c.execute(
                '''SELECT name, COUNT(*) FROM skills
                   GROUP BY name HAVING ''' + condition, values):
            result.append({"name": row[0], "frequency": row[1]})

        return jsonify(result)


@app.route('/skills/<user_email>', methods=['GET'])
def get_skills_user(user_email):
    """Get skills of specific user. Optional parameters to specify minimum/maximum ratings."""
    if not check_if_exists(user_email):
        abort(400, "User with email address provided does not exist.")
    args = request.args
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

        return jsonify([dict(zip(row_skill.keys(), tuple(row_skill))) for row_skill in c.execute(
            "SELECT name, rating FROM skills WHERE email = ?" + additional, values).fetchall()])


@app.route('/skills/frequency/<skill_name>', methods=['GET'])
def get_skill_frequency(skill_name):
    """Get skill frequency (number of users that have the skill) for a specific skill."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        query_result = c.execute(
            "SELECT count(*) FROM skills WHERE name = ?",
            [skill_name])

        return jsonify({"skill_frequency": query_result.fetchone()[0]})


@app.route('/skills/average/<skill_name>', methods=['GET'])
def get_skill_average(skill_name):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row

        query_result = c.execute(
            "SELECT AVG(rating) FROM skills WHERE name = ?",
            [skill_name])

        frequency = query_result.fetchone()[0]

        if frequency is None:
            abort(400, "No skills found with specified name")

        return jsonify({"skill_frequency": frequency})


if __name__ == '__main__':
    app.run(debug=False)
