from flask import Flask, request, jsonify
import tiktoken

from llama_tokenizer import LLaMaTokenizer

app = Flask(__name__)

openai_tokenizers = {
    'gpt-4': tiktoken.encoding_for_model('gpt-4'),
    'gpt-3.5-turbo': tiktoken.encoding_for_model('gpt-3.5-turbo'),
    'text-davinci-002': tiktoken.encoding_for_model('text-davinci-002')
}

llama_tokenizers = {
    'llama-2-70b': LLaMaTokenizer('models/llama-2-70b.model')
}

def tokenize_openai(text, model):
    tokenizer = openai_tokenizers[model]
    tokens = tokenizer.encode(text)
    tok_list = [tokenizer.decode_single_token_bytes(t) for t in tokens]
    num_tokens = len(tokens)

    final_tokens = []
    for t in tok_list:
        try:
            final_tokens.append(t.decode('ascii'))
        except:
            final_tokens.append('\uFFFD')

    return {
        'num_tokens': num_tokens, 
        'tokens_str': final_tokens,
        'tokens_int': tokens
    }

def tokenize_llama(text, model):

    tokenizer = llama_tokenizers[model]
    tokens = tokenizer.encode(text, False, False)
    tok_list = [tokenizer.decode(t) for t in tokens]

    # this tokenizer strips spaces.
    # we'll let the frontend handle that.
    # ws_tok_list = []
    # curr_text = text
    # space_chr = '\u23b5'
    # for token in tok_list:
    #     temp_tok = token
    #     while len(temp_tok) < len(curr_text) and curr_text[len(temp_tok)] == ' ':
    #         temp_tok += space_chr
    #     while len(temp_tok) < len(curr_text) and curr_text[len(temp_tok)] == '\n':
    #         temp_tok += '\n'

    #     ws_tok_list.append(temp_tok)
    #     curr_text = curr_text[len(temp_tok):]

    return {
        'num_tokens': len(tokens),
        'tokens_str': tok_list,
        'tokens_int': tokens
    }

@app.route('/api/get_tokens', methods=['POST'])
def get_tokens():
    data = request.get_json()
    text = data.get('text', '')
    model = data.get('tokenizer', 'gpt-3.5-turbo')  # Default to tiktoken

    if model in openai_tokenizers:
        response = tokenize_openai(text, model)
    elif model in llama_tokenizers:
        response = tokenize_llama(text, model)
    else:
        return jsonify({"error": "Invalid tokenizer choice"})

    return jsonify(response)
