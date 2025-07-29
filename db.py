import datetime, dotenv, os, secrets, sqlite3, string, validators

# Config
dotenv.load_dotenv()
maxGenAtt = int(os.getenv("MAX_GEN_ATT"))
codeLength = int(os.getenv("CODE_LENGTH"))
baseUrl = str(os.getenv("ORIGINAL_URL"))

pathToDb = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static", "sqlite.db")

def initializeDb():
    os.makedirs(os.path.dirname(pathToDb), exist_ok = True)
    if not os.path.exists(pathToDb):
        with sqlite3.connect(pathToDb) as con:
            cur = con.cursor()
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS links (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            short TEXT NOT NULL UNIQUE,
                            original TEXT NOT NULL UNIQUE,
                            created_at TEXT NOT NULL
                        );
                        """)
            con.commit()

def getLinkRow(type, data):
    if type not in {"short", "original"}:
        raise Exception("This shouldn't happen... (5_100)")
    
    with sqlite3.connect(pathToDb) as con:
        cur = con.cursor()
        query = "SELECT * FROM links WHERE short = ?" if type == "short" else "SELECT * FROM links WHERE original = ?"
        cur.execute(query, (data,))
        row = cur.fetchone()
        
        return row

def createEntry(original):
    # First we check if the URL has https://
    if not original.startswith(("http://", "https://")):
        original = "https://" + original
        
    # Then we check if the link is valid
    if not validators.url(original):
        raise ValueError("The original URL must be a valid one.")
    
    # We check if the original URL is already in the database
    existing = getLinkRow("original", original)
    if existing:
        return existing[1]
    
    # We generate a short code and check to see if it already exists in the database
    for _ in range(maxGenAtt):
        short = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(codeLength))
        if not getLinkRow("short", short):
            break
    else:
        raise Exception("Couldn't generate a short code. Try again later.") 

    # We get the time of creation (analytics purpose)
    time = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S")

    # We save the code to the database
    with sqlite3.connect(pathToDb) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO links (short, original, created_at) VALUES (?,?,?)", (short, original, time))
        con.commit()
        
    # We return the short code
    return baseUrl + short

if __name__ == "__main__":
    initializeDb()