import json
import os
import sqlite3
from openai import OpenAI

class SharedFunctionality:
    def __init__(self):
        self.fdir = os.path.dirname(__file__)
        self.setup_paths()
        self.setup_openai()
        self.setup_strategies()
        self.setup_database()

    def getPath(self, fname):
        return os.path.join(self.fdir, fname)

    def setup_paths(self):
        self.sqliteDbPath = self.getPath("aidb.sqlite")
        self.setupSqlPath = self.getPath("setup.sql")
        self.setupSqlDataPath = self.getPath("setupData.sql")
        self.configPath = self.getPath("config.json")

    def setup_database(self, force_new=False):
        """Setup database connection, optionally creating a new database"""
        if hasattr(self, 'sqliteCon') and self.sqliteCon:
            self.sqliteCursor.close()
            self.sqliteCon.close()

        if force_new and os.path.exists(self.sqliteDbPath):
            os.remove(self.sqliteDbPath)

        self.sqliteCon = sqlite3.connect(self.sqliteDbPath, check_same_thread=False)
        self.sqliteCursor = self.sqliteCon.cursor()
        
        if force_new:
            with open(self.setupSqlDataPath) as setupSqlDataFile:
                setupSQlDataScript = setupSqlDataFile.read()
                
            self.sqliteCursor.executescript(self.setupSqlScript)
            self.sqliteCursor.executescript(setupSQlDataScript)
            self.sqliteCon.commit()

    def setup_openai(self):
        with open(self.configPath) as configFile:
            config = json.load(configFile)
        self.openAiClient = OpenAI(api_key=config["openaiKey"])

    def setup_strategies(self):
        with open(self.setupSqlPath) as setupSqlFile:
            self.setupSqlScript = setupSqlFile.read()
            
        commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
        self.strategies = {
            "zero_shot": self.setupSqlScript + commonSqlOnlyRequest,
            "single_domain_double_shot": (self.setupSqlScript + 
                        " Who doesn't have a way for us to text them? " + 
                        " \nSELECT p.person_id, p.name\nFROM person p\nLEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\nWHERE ph.phone_id IS NULL;\n " +
                        commonSqlOnlyRequest)
        }

    def getChatGptResponse(self, content):
        stream = self.openAiClient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
            stream=True,
        )
        responseList = [chunk.choices[0].delta.content for chunk in stream if chunk.choices[0].delta.content is not None]
        return "".join(responseList)

    def sanitizeForJustSql(self, value):
        gptStartSqlMarker, gptEndSqlMarker = "```sql", "```"
        if gptStartSqlMarker in value:
            value = value.split(gptStartSqlMarker)[1]
        if gptEndSqlMarker in value:
            value = value.split(gptEndSqlMarker)[0]
        return value.strip()

    def runSql(self, query):
        try:
            result = self.sqliteCursor.execute(query).fetchall()
            return result
        except Exception as e:
            return str(e)

    def close_connections(self):
        if hasattr(self, 'sqliteCon') and self.sqliteCon:
            self.sqliteCursor.close()
            self.sqliteCon.close()

    def initialize_database(self):
        """Initialize a fresh database with schema and data"""
        self.setup_database(force_new=True)