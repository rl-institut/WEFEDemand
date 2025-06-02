from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def run_script(script, args):
    try:
        result = subprocess.run(
            ["python", f"{script}", *[f"--{k}={v}" for k, v in args.items()]],
            capture_output=True,
            text=True
        )
        return jsonify({"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/preprocessing", methods=["POST"])
def run_preprocessing():
    data = request.json
    script = "preprocessing_demo.py"
    args = data.get("args", {})
    return run_script(script, args)

@app.route("/ramp-simulation", methods=["POST"])
def run_simulation():
    data = request.json
    script = "ramp_simulation_demo.py"
    args = data.get("args", {})
    return run_script(script, args)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
