from flask import Flask, url_for, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "ab125"

# MongoDB setup       mongodb+srv://admin:<password>@cluster0.fuuvqfk.mongodb.net/
client = MongoClient("mongodb+srv://admin:imran123@cluster0.mz7q55x.mongodb.net/")
db = client["blog"]
users_collection = db["users"]
collection = db["posts"]

@app.route('/', methods=['GET','POST'])

def login():
    if request.method == "POST":
        username = request.form["your_name"]
        password = request.form["your_pass"]
        
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid credentials!"
    return render_template('login.html')
    
    
@app.route('/signup', methods=['GET','POST'])

def signup():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]
        
        # Check if the username already exists
        if users_collection.find_one({"username": username}):
            return "Username already exists!"
        
        users_collection.insert_one({"username": username, "email": email, "password": password})
        return redirect(url_for("login"))
    return render_template('signup.html')


@app.route("/home")

def home():
    if "username" in session:
        username = session["username"]
        # return f"Welcome, {username}!"
        return render_template('index.html')
    
    else:
        return redirect(url_for("login"))


@app.route('/blogs')
def blogs():
    # Retrieve blog posts from MongoDB
    blogs = list(collection.find())  # Convert the cursor to a list of dictionaries
    return render_template('blogs.html', blogs=blogs)


@app.route('/read_blog/<string:blog_title>')
def read_blog(blog_title):
    blog = collection.find_one({'title': blog_title})
    return render_template('readblog.html', blog=blog)


@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        content = request.form['content']

        # Insert the blog post into MongoDB
        collection.insert_one({'title': title, 'content': content})

        return redirect(url_for('blogs'))

    return render_template('add_blog.html')

@app.route('/aboutus')
def about():
    return render_template('about.html')


@app.route('/premium')
def premium():
    return render_template('premium.html')

@app.route('/cards')
def card():
    return render_template('card.html')

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
  

if __name__ == '__main__':
    app.run(debug=True)