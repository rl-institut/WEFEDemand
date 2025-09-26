from flask import Flask, request, jsonify
import os
from fastapi import FastAPI, Request
import uvicorn
import logging

from ramp_simulation_demo import main as run_ramp_simulation

app = FastAPI()

@app.get('/')
async def index():
    logging.info("Startup started...")
    return {"message": "Welcome to the WEFEDemand app, please use the /ramp-simulation endpoint to perform simulations"}

@app.post("/ramp-simulation")
async def run_simulation(request: Request):
    data = await request.json()
    args = data.get("args", {})
    survey_id = data.get("survey_id", "")
    os.environ["SURVEY_KEY"] = survey_id
    try:
        agg_mean = run_ramp_simulation(args)
        return {"data": agg_mean.to_dict(orient="list")}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
