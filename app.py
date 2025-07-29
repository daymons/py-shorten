import db
import dotenv, flask, os, time

# Config
dotenv.load_dotenv()

app = flask.Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

rateLimitStorage = {}
rateLimitMaxAtt = int(os.getenv("RATE_LIMIT_MAX_ATT"))
rateLimitTime = int(os.getenv("RATE_LIMIT_TIME"))
requestCounter = 0

def cleanupRateLimitStorage():
    now = time.time()
    expiredIpAddr = []
    
    for ipAddr, timestamps in rateLimitStorage.items():
        recentReqs = [_ for _ in timestamps if now - _ < rateLimitTime]
        if recentReqs:
            rateLimitStorage[ipAddr] = recentReqs
        else:
            expiredIpAddr.append(ipAddr)
            
    for ipAddr in expiredIpAddr:
        del rateLimitStorage[ipAddr]

def isRateLimited(ipAddr):
    # Clean up the storage so it doesn't get too heavy
    global requestCounter
    requestCounter += 1
    
    if requestCounter % 100 == 0:
        cleanupRateLimitStorage()

    now = time.time()
    requests = rateLimitStorage.get(ipAddr, [])
    
    # Delete requests older than the time window (5 minutes on default)
    requests = [_ for _ in requests if now - _ < rateLimitTime]
    rateLimitStorage[ipAddr] = requests
    
    if len(requests) >= rateLimitMaxAtt:
        return True
    else:
        requests.append(now)
        rateLimitStorage[ipAddr] = requests
        return False

# Web funnies
@app.route("/<short>")
def short(short):
    original = db.getLinkRow("short", short)
    if not original:
        return "The short code doesn't exist", 404
    else:
        return flask.redirect(original[2])
    
@app.route("/", methods = ["GET", "POST"])
def shorten():
    # Check rate limit
    ipAddr = flask.request.remote_addr
    if isRateLimited(ipAddr):
        return "You're rate limited. Take a break and come back in 5 minutes.", 429
    
    if flask.request.method == "GET":
        return flask.render_template("shorten.html")
    
    elif flask.request.method == "POST":
        original = flask.request.form.get("original")
        try:
            short = db.createEntry(original)
        except ValueError as e:
            return str(e), 400

        return short
    
    else:
        return "Forbidden", 403

if __name__ == "__main__":
    app.run()