from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

@app.route("/roll/<dice>")
def roll(dice):
    print(f"[MOCK] Request received at {time.time():.2f}")
    time.sleep(5) # Simulated slow boi latency
    result = random.randint(1, 20)
    return jsonify({"dice": dice, "result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, threaded=True)
