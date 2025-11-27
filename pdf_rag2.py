
from langchain_ollama import OllamaEmbeddings, ChatOllama

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embedding_model_name = "nomic-embed-text"
llm_model_name = "qwen:7b"




vector_store = Chroma(
    embedding_function=OllamaEmbeddings(model=embedding_model_name),
    collection_name="simulation",
    persist_directory="./vector_db"
)

print("Base vectorielle chargée")



#LLM + Multi requêtes
 
llm = ChatOllama(model=llm_model_name)

multi_query_prompt = PromptTemplate(input_variables=["question"],template=(
        #"Ignore les conversation précédente. Voici une nouvelle demande:"
        "Tu es un assistant IA spécialisé dans la recherche documentaire. "
        "Génère 5 reformulations différentes et pertinentes de la question suivante "
        "afin d'améliorer la récupération d'informations dans une base vectorielle.\n\n"
        "Question d'origine : {question}"
    ),
)

retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(), #retriever sémantique classique (similarité de vecteurs)
    llm=llm,
    prompt=multi_query_prompt,
)

print("config multirequete activé")



#fonction pour transformer les documents en texte
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

#prompt pour le RAG
context_prompt = ChatPromptTemplate.from_template(
    "Répondez à la question en utilisant UNIQUEMENT le contexte ci-dessous:\n"
    "{context}\n\n"
    "Question: {question}"
)

#chaîne RAG complète
rag_chain = (
    {
        "context": retriever | format_docs,  # retriever -> docs -> texte
        "question": RunnablePassthrough(),   # la question passe telle quelle
    }
    | context_prompt
    | llm
    | StrOutputParser()
)

#question
user_question = "comment est simulé le LIDAR"
response = rag_chain.invoke(user_question)

print("Reponse RAG")
print(response)
