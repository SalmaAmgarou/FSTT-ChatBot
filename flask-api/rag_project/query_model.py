from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from .embeddings import embedding_function

CHROMA_PATH = "chroma"
prompt = PromptTemplate(
    template="""Vous êtes un assistant pour les tâches de réponse aux questions. Utilisez les éléments de contexte récupérés suivants pour répondre à la question. Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas.
    Utilisez trois phrases maximum et restez concis.

    utilisateur

    Voici le document récupéré :

    {document}

    ---
    Voici la question de l'utilisateur :

    {question}

    assistant""",
    input_variables=["question", "document"],
)


def query_rag(query_text: str, model, tokenizer=None):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_function()
    )
    retriever = db.as_retriever()
    docs = retriever.invoke(query_text)
    
    #results = db.similarity_search_with_score(query_text)
    def format_docs(docs):
        return "\n\n---\n\n".join([doc.page_content for doc in docs])
        
        
    formatted_docs=format_docs(docs)
    prompt_text = prompt.format(document=formatted_docs, question=query_text)

    if tokenizer:
           inputs = tokenizer(prompt_text, return_tensors="pt")
           outputs = model.generate(**inputs)
           response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    else:
           generation = model.generate([prompt_text], max_length=5000, num_return_sequences=1)
           response_text = generation.generations[0][0].text if generation.generations and generation.generations[0] else "No response generated."

    if "assistant" in response_text:
        response_text = response_text.split("assistant")[-1].strip()
    formatted_response = f"""
    --> Réponse de l'Assistant

    ✨Question de l'utilisateur :
    {query_text}

    -->
    
     📄Contexte :
    {formatted_docs}

    -->

    ✅Réponse :
    {response_text} 
    """
    
    print(formatted_response)
    return formatted_response.replace('\n', ' ')
