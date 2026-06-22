"""
Backend for Resonance Nullification simulation.
Provides REST API to compute time series of alternating resonance.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    A = data.get('A', 1.0)
    gamma = data.get('gamma', 0.1)
    T = data.get('T', 2.0)        # period of sign switching
    duration = data.get('duration', 10.0)
    num_points = int(data.get('num_points', 500))

    t = np.linspace(0, duration, num_points)
    square_wave = np.sign(np.sin(2 * np.pi * t / T))
    Xi = A * np.exp(gamma * t) * square_wave

    # Compute moving average with window = T
    dt = t[1] - t[0]
    window = int(T / dt)
    if window > 1:
        cumsum = np.cumsum(np.insert(Xi, 0, 0))
        moving_avg = (cumsum[window:] - cumsum[:-window]) / window
        t_avg = t[window-1:]
    else:
        moving_avg = Xi
        t_avg = t

    result = {
        't': t.tolist(),
        'Xi': Xi.tolist(),
        't_avg': t_avg.tolist(),
        'moving_avg': moving_avg.tolist()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
