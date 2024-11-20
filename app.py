from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up the MongoDB URI
app.config["MONGO_URI"] = os.getenv("MONGODB_URI") + "/mydb"  # Replace 'mydb' with your database name
mongo = PyMongo(app)

# Home route to display form and handle queries
@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.args.get('search', '')
    search_results = []
    
    if search_query:
        # Search the database across all fields (first_name, last_name, dob, address, mobile)
        search_results = mongo.db.users.find({
            "$or": [
                {"first_name": {"$regex": search_query, "$options": "i"}},
                {"last_name": {"$regex": search_query, "$options": "i"}},
                {"dob": {"$regex": search_query, "$options": "i"}},
                {"address": {"$regex": search_query, "$options": "i"}},
                {"mobile": {"$regex": search_query, "$options": "i"}}
            ]
        })
    
    if request.method == "POST":
        # Get form data for new entry
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        address = request.form["address"]
        mobile = request.form["mobile"]
        
        # Insert the data into the MongoDB database
        mongo.db.users.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob,
            "address": address,
            "mobile": mobile
        })
        return redirect(url_for("index"))
    
    return render_template("index.html", search_results=search_results, search_query=search_query)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port = 3000)
