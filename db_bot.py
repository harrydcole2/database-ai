from shared import SharedFunctionality
import json
from time import time

print("Running db_bot.py!")

shared = SharedFunctionality()
shared.initialize_database()  # This version needs a fresh DB each time

questions = [
    "Which jobs have the best ratings?",
    "Which universities have the best rated jobs?",
    "What user(s) have the most extensive work history?",
    "What jobs have the most benefits?",
    "Which departments have the best pay?",
    "What ratings might be untrustworthy?",
    "What job tags are reused across multiple ratings?",
    "What users experienced the worst work conditions?"
]

for strategy in shared.strategies:
    responses = {
        "strategy": strategy, 
        "prompt_prefix": shared.strategies[strategy]
    }
    questionResults = []
    
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = shared.getChatGptResponse(shared.strategies[strategy] + " " + question)
            sqlSyntaxResponse = shared.sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            
            queryRawResponse = str(shared.runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            
            friendlyResultsPrompt = f"I asked a question \"{question}\" and the response was \"{queryRawResponse}\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            friendlyResponse = shared.getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
            
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question, 
            "sql": sqlSyntaxResponse, 
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(shared.getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent=2)

shared.close_connections()
print("Done!")