from flask import Flask, render_template, request, jsonify
from Nirma import GradePredictor

app = Flask(__name__)
gp = GradePredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        from_grade = request.args.get('from_grade', 'C')
        till_grade = request.args.get('till_grade', 'O')

        if not data:
            return jsonify({'error': 'No data received'}), 400

        gp.fit(data)
        result = gp.predict(from_grade=from_grade, till_grade=till_grade)
        return jsonify(result.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host = "0.0.0.0" , port = 5000 )
