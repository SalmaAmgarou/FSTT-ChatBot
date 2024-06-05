from langchain_community.embeddings import HuggingFaceEmbeddings
from torch import cuda

def embedding_function():
    embed_model_id = 'sentence-transformers/distilbert-base-nli-mean-tokens'
    device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

    embed_model = HuggingFaceEmbeddings(
        model_name=embed_model_id,
        model_kwargs={'device': device},
        encode_kwargs={'device': device, 'batch_size': 32}
    )
    return embed_model
