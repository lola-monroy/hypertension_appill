from flask import Flask, jsonify
import random
import argparse

app = Flask(__name__)
normal_means = {
    'blood_pressure': 120,
    'heart_rate': 70,
    'heart_rate_variability': 0.1,
    'steps': 10
}

danger_means = {
    'blood_pressure': 160,
    'heart_rate': 90,
    'heart_rate_variability': 0.2,
    'steps': 50
}

danger = False
count = 0

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--danger', action='store_true')
    return parser.parse_args()

@app.route('/smartwatch', methods=['GET'])
def query():
    global count, danger, normal_means, danger_means
    if not danger:
        count = 0
    means = {
        key: normal_mean + (danger_mean - normal_mean) * min(1, count / 10)
        for (key, normal_mean), (_, danger_mean) in zip(normal_means.items(), danger_means.items())
    }
    blood_pressure = random.normalvariate(means['blood_pressure'], 10)
    heart_rate = random.normalvariate(means['heart_rate'], 5)
    ecg = 0 if not danger or count < 5 else 1 if count < 10 else 2
    heart_rate_variability = random.normalvariate(means['heart_rate_variability'], 0.05)
    steps = random.randint(int(means['steps']) - 3, int(means['steps']) + 3)
    count += 1
    return jsonify({
        'blood_pressure': blood_pressure,
        'heart_rate': heart_rate,
        'ecg': ecg,
        'heart_rate_variability': heart_rate_variability,
        'steps': steps
    })

# Run the app on a local port
if __name__ == '__main__':
    args = parse_args()
    if args.danger:
        danger = True
    app.run(host='0.0.0.0', port=5000)