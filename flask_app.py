from flask import Flask, request, jsonify
import json
import os
import sqlite3
from openai import OpenAI

app = Flask(__name__)

# Setup database connection
fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

sqliteDbPath = getPath("aidb.sqlite")
sqliteCon = sqlite3.connect(sqliteDbPath, check_same_thread=False)
sqliteCursor = sqliteCon.cursor()

# Load OpenAI config
configPath = getPath("config.json")
with open(configPath) as configFile:
    config = json.load(configFile)
openAiClient = OpenAI(api_key=config["openaiKey"])

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

# Strategies
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
with open(getPath("setup.sql")) as setupSqlFile:
    setupSqlScript = setupSqlFile.read()
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript + 
                   " Who doesn't have a way for us to text them? " + 
                   " \nSELECT p.person_id, p.name\nFROM person p\nLEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\nWHERE ph.phone_id IS NULL;\n " +
                   commonSqlOnlyRequest)
}

@app.route("/ask/zero_shot", methods=["POST"])
def ask_zero_shot():
    return ask_question("zero_shot")

@app.route("/ask/single_domain_double_shot", methods=["POST"])
def ask_single_domain_double_shot():
    return ask_question("single_domain_double_shot")

def ask_question(strategy):
    data = request.get_json()
    user_question = data.get("question")
    
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    
    sql_query = getChatGptResponse(strategies[strategy] + " " + user_question)
    sql_query = sanitizeForJustSql(sql_query)
    query_result = runSql(sql_query)
    
    friendly_response_prompt = f"I asked a question '{user_question}' and the response was '{query_result}'. Please provide a concise, friendly response."
    friendly_response = getChatGptResponse(friendly_response_prompt)
    
    return jsonify({
        "strategy": strategy,
        "question": user_question,
        "sql": sql_query,
        "query_result": query_result,
        "friendly_response": friendly_response
    })

if __name__ == "__main__":
    app.run(debug=True)
