from flask import Flask, url_for, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "ab125"

# MongoDB setup       mongodb+srv://admin:<password>@cluster0.fuuvqfk.mongodb.net/
# client = MongoClient("mongodb+srv://admin:imran123@cluster0.mz7q55x.mongodb.net/")
client = MongoClient("mongodb://localhost:27017")

db = client["blog"]
users_collection = db["users"]
collection = db["posts"]

user = ' '
premium_user = False

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form["your_name"]
        password = request.form["your_pass"]
        
        global user
        global premium_user

        user = users_collection.find_one({"username": username, "password": password})
        
        # print(user['is_premium'])
        
        premium_user = user['is_premium']

        if user:
            session["username"] = username
            # user_data = users_collection.find_one({"username": username})
            # if user_data:
            #     session['user_id'] = user_data['_id']
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

        return render_template('home.html')
    
    else:
        return redirect(url_for("login"))


@app.route('/blogs')
def blogs():
    # Retrieve blog posts from MongoDB
    blogs = list(collection.find())  # Convert the cursor to a list of dictionaries
    return render_template('blogs.html', blogs=blogs, premium_user=premium_user)


@app.route('/read_blog/<string:blog_title>')
def read_blog(blog_title):
    blog = collection.find_one({'title': blog_title})
    return render_template('readblog.html', blog=blog)

@app.route('/like_blog/<string:blog_title>', methods=['POST'])
def like_blog(blog_title):
    if "username" not in session:
        return redirect(url_for("login"))

    # Get the current user's username
    username = session["username"]

    # You can implement logic here to record the like by the user for the specified blog post.
    # You might want to create a new collection in MongoDB to track likes or update the existing blog document.

    return redirect(url_for('read_blog', blog_title=blog_title))


@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        content = request.form['content']

        # Insert the blog post into MongoDB
        collection.insert_one({'title': title, 'content': content, 'likes':0, 'liked_by': []})

        return redirect(url_for('blogs'))

    return render_template('add_blog.html')

@app.route('/like_unlike_blog/<string:blog_title>', methods=['POST'])
def like_unlike_blog(blog_title):
    if "username" not in session:
        return redirect(url_for("login"))

    # Get the current user's username
    username = session["username"]

    # Retrieve the blog post
    blog = collection.find_one({'title': blog_title})

    # Check if the user has already liked the blog
    if username in blog.get('liked_by', []):
        # User has already liked the blog, so unlike it
        collection.update_one({'title': blog_title}, {'$pull': {'liked_by': username}})
        # Decrement the likes count
        collection.update_one({'title': blog_title}, {'$inc': {'likes': -1}})
    else:
        # User hasn't liked the blog, so like it
        collection.update_one({'title': blog_title}, {'$push': {'liked_by': username}})
        # Increment the likes count
        collection.update_one({'title': blog_title}, {'$inc': {'likes': 1}})

    # Retrieve the updated blog post to get the current likes count
    updated_blog = collection.find_one({'title': blog_title})

    return render_template('readblog.html', blog=updated_blog)


@app.route('/aboutus')
def about():
    return render_template('about.html')


@app.route('/premium')
def premium():
    return render_template('premium.html')

@app.route('/buy_premium')
def buy_premium(): 
    global user
    global premium_user

    user_id = user['_id']  # Replace with your user ID
    users_collection.update_one({"_id": user_id}, {"$set": {"is_premium": True}})
    
    premium_user = True

    return redirect(url_for('blogs'))


@app.route('/cards')
def card():
    return render_template('card.html')

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
  

if __name__ == '__main__':
    app.run(debug=True)