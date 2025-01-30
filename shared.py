import json
import os
import sqlite3
from openai import OpenAI

# Global variables
sqliteCon = None
sqliteCursor = None
openAiClient = None
strategies = None
setupSqlScript = None

def getPath(fname):
    fdir = os.path.dirname(__file__)
    return os.path.join(fdir, fname)

def get_paths():
    return {
        'sqliteDbPath': getPath("aidb.sqlite"),
        'setupSqlPath': getPath("setup.sql"),
        'setupSqlDataPath': getPath("setupData.sql"),
        'configPath': getPath("config.json")
    }

def setup_database(force_new=False):
    global sqliteCon, sqliteCursor
    paths = get_paths()
    
    # Close existing connection if it exists
    if sqliteCon:
        sqliteCursor.close()
        sqliteCon.close()

    # If force_new and database exists, remove it
    if force_new and os.path.exists(paths['sqliteDbPath']):
        os.remove(paths['sqliteDbPath'])

    # Create new connection
    sqliteCon = sqlite3.connect(paths['sqliteDbPath'], check_same_thread=False)
    sqliteCursor = sqliteCon.cursor()
    
    # If new database, initialize schema and data
    if force_new:
        with open(paths['setupSqlDataPath']) as setupSqlDataFile:
            setupSQlDataScript = setupSqlDataFile.read()
            
        sqliteCursor.executescript(setupSqlScript)
        sqliteCursor.executescript(setupSQlDataScript)
        sqliteCon.commit()

def setup_openai():
    global openAiClient
    paths = get_paths()
    with open(paths['configPath']) as configFile:
        config = json.load(configFile)
    openAiClient = OpenAI(api_key=config["openaiKey"])

def setup_strategies():
    global strategies, setupSqlScript
    paths = get_paths()
    
    # Load SQL setup script
    with open(paths['setupSqlPath']) as setupSqlFile:
        setupSqlScript = setupSqlFile.read()
        
    commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
    strategies = {
        "zero_shot": setupSqlScript + commonSqlOnlyRequest,
        "single_domain_double_shot": (setupSqlScript + 
                    " Who doesn't have a way for us to text them? " + 
                    " \nSELECT p.person_id, p.name\nFROM person p\nLEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\nWHERE ph.phone_id IS NULL;\n " +
                    commonSqlOnlyRequest)
    }

def initialize():
    """Initialize all required components"""
    setup_openai()
    setup_strategies()
    setup_database()

def initialize_database():
    """Initialize a fresh database with schema and data"""
    setup_database(force_new=True)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    responseList = [chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content is not None]
    return "".join(responseList)

def sanitizeForJustSql(value):
    gptStartSqlMarker, gptEndSqlMarker = "```sql", "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]
    return value.strip()

def runSql(query):
    try:
        result = sqliteCursor.execute(query).fetchall()
        return result
    except Exception as e:
        return str(e)

def close_connections():
    global sqliteCon, sqliteCursor
    if sqliteCon:
        sqliteCursor.close()
        sqliteCon.close()
        sqliteCon = None
        sqliteCursor = None