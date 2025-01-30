from flask import Flask, request, jsonify
import shared

app = Flask(__name__)
shared.initialize()

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
    
    sql_query = shared.getChatGptResponse(shared.strategies[strategy] + " " + user_question)
    sql_query = shared.sanitizeForJustSql(sql_query)
    query_result = shared.runSql(sql_query)
    
    friendly_response_prompt = f"I asked a question '{user_question}' and the response was '{query_result}'. Please provide a concise, friendly response."
    friendly_response = shared.getChatGptResponse(friendly_response_prompt)
    
    return jsonify({
        "strategy": strategy,
        "question": user_question,
        "sql": sql_query,
        "query_result": query_result,
        "friendly_response": friendly_response
    })

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        shared.close_connections()