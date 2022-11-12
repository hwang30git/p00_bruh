from flask import Flask, render_template, request, session, redirect, flash
import secrets
from db import auth, stories

app = Flask(__name__)

@app.route("/")
def home():
    if 'username' in session:
        return render_template('home.html', contributed_stories=stories.get_contributed(session["user_id"]), uncontributed_stories=stories.get_uncontributed(session["user_id"])) 
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if 'username' in session:
            return redirect("/")
        return render_template('register.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

        available = auth.check_username(username)
        if not available:
            return render_template('register.html', message="username not available")

        auth.register_user(username, password)

        session['username'] = request.form['username']
        session['user_id'] = auth.get_user_id(username)
        return redirect('/') 
    
@app.route("/stories")
def contributed_stories():
    if 'username' not in session:
        return redirect("/")
    return render_template('stories.html', page_title="read stories", stories=[]) 

@app.route("/new_stories")
def new_stories():
    if 'username' not in session:
        return redirect("/")
    return render_template('stories.html', page_title="new stories", stories=[]) 

@app.route("/new", methods=["GET", "POST"])
def new():
    if 'username' not in session:
        return redirect("/")
    if request.method == "GET":
        return render_template('new_story.html')
    else:
        stories.create_story(request.form["title"], request.form["story"], session['user_id'])
        return redirect('/') 

@app.route("/story/<id>")
def story(id):
    if 'username' not in session:
        return redirect("/")

    if session["username"] in stories.get_contributors(id):
        return render_template('story.html', story_title=stories.get_title(id), authors=stories.get_contributors(id), story=stories.get_story(id)) 
    
    return render_template('hidden_story.html', story_title=stories.get_title(id), last_line=stories.get_story(id)[-1]) 

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    info_correct = auth.check_creds(username, password)

    if info_correct:
        session['username'] = username
        session['user_id'] = auth.get_user_id(username)
    else:
        flash("invalid username or password")

    return redirect("/")

@app.route("/home")
def back_home():
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("logged out")
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    # app.secret_key = secrets.token_hex()
    app.secret_key = "."
    
    auth.create_table()
    stories.create_tables()

    app.run()