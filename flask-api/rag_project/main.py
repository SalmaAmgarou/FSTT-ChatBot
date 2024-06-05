import argparse
from query_model import query_rag
from langchain_community.llms.ollama import Ollama
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model(model_type="rag"):
    
    if model_type == "fine_tuned":
        model_name = "hamza08456098/Fine-tuning-MISTRAL"
        hf_auth = "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"
        tokenizer = AutoTokenizer.from_pretrained(model_name,use_auth_token=hf_auth , trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_auth , trust_remote_code=True)
        return model, tokenizer
    else:
        from langchain_community.llms.ollama import Ollama
        model = Ollama(model='mistral')
        return model, None

def parse_args(args_list):
       parser = argparse.ArgumentParser()
       parser.add_argument("--model_type", type=str, default="rag", choices=["rag", "fine_tuned"], help="Model type to use.")
       parser.add_argument("query_text", type=str, help="The query text.")
       args = parser.parse_args(args_list)
       return args

if __name__ == "__main__":
    # Capture command-line arguments using sys.argv
    args = parse_args(sys.argv[1:])

    model, tokenizer = load_model(args.model_type)
    query_rag(args.query_text, model, tokenizer)

