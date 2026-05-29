from flask import Flask, render_template, request, redirect,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'groomers'

conn = sqlite3.connect("shop.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        if email == "" or password == "":
            flash("Please fill all fields")
            return redirect("/")

        conn = sqlite3.connect("shop.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect("/homepage")

        else:
            flash("Invalid email or password")
            return render_template(
                "index.html",
                email=email
            )

    return render_template("index.html")

@app.route("/createaccount", methods=["GET", "POST"])
def createaccount():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username == "" or email == "" or password == "" or confirm_password == "":
            flash("Please fill all fields")
            return redirect("/createaccount")

        if len(username) < 8:
            flash("Username must be at least 8 characters long")
            return redirect("/createaccount")

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect("/createaccount")

        conn = sqlite3.connect("shop.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user:
            conn.close()
            flash("Username already exists")
            return redirect("/createaccount")

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        email_check = cur.fetchone()

        if email_check:
            conn.close()
            flash("Email already exists")
            return redirect("/createaccount")

        cur.execute(
            "INSERT INTO users(username, email, password) VALUES(?,?,?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        flash("Account created successfully")
        return redirect("/homepage")

    return render_template("createacc.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)