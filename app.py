from flask import Flask, request, jsonify
import util

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')


@app.route('/api/get_tokens', methods=['POST'])
def get_tokens():
    data = request.get_json()
    text = data.get('text', '')
    model = data.get('tokenizer', 'gpt-3.5-turbo')  # Default to tiktoken

    if model in util.openai_tokenizers:
        response = util.tokenize_openai(text, model)
    elif model in util.llama_tokenizers:
        response = util.tokenize_llama(text, model)
    elif model in util.hf_tokenizers:
        response = util.tokenize_hf(text, model)
    else:
        return jsonify({"error": "Invalid tokenizer choice"})

    return jsonify(response)
