from flask import Flask, request, jsonify
import sys
sys.path.append('/home/sasamg/Desktop/NLP_CHATBOT/rag_project')
from rag_project.query_model import query_rag  
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__)
CORS(app)

# Global variables to store the loaded model and tokenizer

global model
global tokenizer
model = None
tokenizer = None

# This function is now used in the 'load_model_route'
def load_fine_tuned_model():
    model_name = "hamza08456098/FineTunedMistral"
    hf_auth = "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"
    tokenizer = AutoTokenizer.from_pretrained(model_name,use_auth_token=hf_auth , trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_auth , trust_remote_code=True)
    return model, tokenizer

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data['query']
    
    if model and tokenizer:
        pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=800)
        gen_text = pipe(query_text)
        response = gen_text[0]['generated_text'][len(query_text):]
        return jsonify({"response": response})
    else:
        # Fallback for other model types (RAG)
        response = query_rag(query_text, model, tokenizer) 
        return jsonify({"response": response})
@app.route('/load_model', methods=['POST'])
def load_model_route():
    global model, tokenizer
    data = request.get_json()
    model_type = data.get('model_type', 'rag')

    # Load the appropriate model based on 'model_type'
    if model_type == "fine_tuned":
        model, tokenizer = load_fine_tuned_model()  # Use the function here
    else:
        from langchain_community.llms.ollama import Ollama
        model = Ollama(model='mistral')
        tokenizer = None  

    return jsonify({"message": "Model loaded successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)