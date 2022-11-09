from flask import Flask, render_template 
app = Flask(__name__)

@app.route("/")
def home():
    # should only be visible to logged in users
    return render_template('home.html', contributed_stories=[], new_stories=[]) 

@app.route("/login") # merge with / once Flask session in place
def login():
    return render_template('login.html') 

@app.route("/register")
def register():
    return render_template('register.html') 

@app.route("/stories")
def stories():
    return render_template('stories.html', page_title="read stories", stories=[]) 

@app.route("/new_stories")
def new_stories():
    return render_template('stories.html', page_title="new stories", stories=[]) 

@app.route("/new")
def new():
    return render_template('new_story.html') 

@app.route("/story/<id>")
def story(id):
    # should only be visible to users who contributed to story id
    return render_template('story.html', story_title="test", authors=["ts", "sm"], story="hello world") 

@app.route("/hidden_story/<id>") # merge with /story/<id> once db in place
def hidden_story(id):
    return render_template('hidden_story.html', story_title="test", story_id=id, last_line="hello") 

if __name__ == "__main__":
    app.debug = True
    app.run()