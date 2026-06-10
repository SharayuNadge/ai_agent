from flask import Flask, render_template, request, Response, stream_with_context
from agent import run_agent

app = Flask(__name__)

current_goal = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/research", methods=["POST"])
def research():
    global current_goal
    data = request.get_json(force=True)
    current_goal = request.json.get("goal")
    return {"status": "ok"}

@app.route("/stream")
def stream():
    def generate():
        for update in run_agent(current_goal):
            #yield f"data: {update}\n\n"
            yield f"data: {update.replace(chr(10), '<br>')}\n\n"
    return Response(stream_with_context(generate()), mimetype="text/event-stream")
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)