from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

def run_script(script, args):
    try:
        args_list = []
        for k, v in args.items():
            if isinstance(v, list):
                args_list.append(f"--{k}")
                args_list.extend(str(x) for x in v)
            else:
                args_list.append(f"--{k}={v}")
        print(script, args_list)
        result = subprocess.run(
            ["python", script, *args_list],
            capture_output=True,
            text=True
        )
        return jsonify({"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/preprocessing", methods=["POST"])
def run_preprocessing():
    data = request.get_json()
    script = "demo/preprocessing_demo.py"
    args = data.get("args")
    survey_id = data.get("survey_id")
    os.environ["SURVEY_KEY"] = survey_id
    res = run_script(script, args)
    return res

@app.route("/ramp-simulation", methods=["POST"])
def run_simulation():
    data = request.get_json()
    script = "demo/ramp_simulation_demo.py"
    args = data.get("args", {})
    survey_id = data.get("survey_id", {})
    os.environ["SURVEY_KEY"] = survey_id
    return run_script(script, args)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
