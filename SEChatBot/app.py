from flask import Flask, request, jsonify, render_template
from faq_utils import find_best_answer

app = Flask(__name__)
app.static_folder = 'static'

# Route for serving the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the FAQ matching request
@app.route('/faq', methods=['POST'])
def process_faq():
    data = request.get_json()
    user_question = data.get('question')
    answer = find_best_answer(user_question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run()
