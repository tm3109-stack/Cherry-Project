from flask import Flask, request, redirect, render_template
import json, os, random, string

app = Flask(__name__)

DB_FILE = "db.json"

# Create db.json if missing
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"urls": []}, f)

def read_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    db = read_db()
    urls = db["urls"]

    if request.method == "POST":
        long_url = request.form.get("longUrl")
        if long_url:
            short_id = generate_short_id()
            urls.append({"shortId": short_id, "longUrl": long_url, "clicks": 0})
            write_db(db)

    return render_template("index.html", urls=urls)

@app.route("/<shortId>")
def redirect_url(shortId):
    db = read_db()
    for entry in db["urls"]:
        if entry["shortId"] == shortId:
            entry["clicks"] += 1
            write_db(db)
            return redirect(entry["longUrl"])
    return "❌ URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
