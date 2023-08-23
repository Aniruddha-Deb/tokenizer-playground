import tiktoken
from transformers import AutoTokenizer

import os
from typing import List

from sentencepiece import SentencePieceProcessor

class LLaMaTokenizer:
    def __init__(self, model_path: str):
        # reload tokenizer
        assert os.path.isfile(model_path), model_path
        self.sp_model = SentencePieceProcessor(model_file=model_path)

        # BOS / EOS token IDs
        self.n_words: int = self.sp_model.vocab_size()
        self.bos_id: int = self.sp_model.bos_id()
        self.eos_id: int = self.sp_model.eos_id()
        self.pad_id: int = self.sp_model.pad_id()
        assert self.sp_model.vocab_size() == self.sp_model.get_piece_size()

    def encode(self, s: str, bos: bool, eos: bool) -> List[int]:
        assert type(s) is str
        t = self.sp_model.encode(s)
        if bos:
            t = [self.bos_id] + t
        if eos:
            t = t + [self.eos_id]
        return t

    def decode(self, t) -> str:
        return self.sp_model.decode(t)

openai_tokenizers = {
    'gpt-4': tiktoken.encoding_for_model('gpt-4'),
    'gpt-3.5-turbo': tiktoken.encoding_for_model('gpt-3.5-turbo'),
    'text-davinci-002': tiktoken.encoding_for_model('text-davinci-002')
}

llama_tokenizers = {
    'llama-2-70b': LLaMaTokenizer('models/llama-2-70b.model')
}

hf_tokenizers = {
    'muril': AutoTokenizer.from_pretrained('google/muril-base-cased'),
    'mbert': AutoTokenizer.from_pretrained('bert-base-multilingual-cased'),
    'afro-xlmr': AutoTokenizer.from_pretrained('Davlan/afro-xlmr-large'),
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

    return {
        'num_tokens': len(tokens),
        'tokens_str': tok_list,
        'tokens_int': tokens
    }

def tokenize_hf(text, model):

    tokenizer = hf_tokenizers[model]
    tokens = tokenizer.encode(text)
    tok_list = [tokenizer.decode(t) for t in tokens]

    return {
        'num_tokens': len(tokens),
        'tokens_str': tok_list,
        'tokens_int': tokens
    }
