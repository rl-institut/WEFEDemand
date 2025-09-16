from flask import Flask, request, jsonify
import os

from ramp_simulation_demo import main as run_ramp_simulation

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the WEFEDemand app, please use the /ramp-simulation endpoint to perform simulations"})

@app.route("/ramp-simulation", methods=["POST"])
def run_simulation():
    data = request.get_json()
    args = data.get("args", {})
    survey_id = data.get("survey_id", {})
    os.environ["SURVEY_KEY"] = survey_id
    try:
        agg_mean = run_ramp_simulation(args)
        return jsonify({"data": agg_mean.to_dict(orient="list")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
