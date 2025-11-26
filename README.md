1-EXTRACTION PDF <br>
<br>
PDF --> Extraction texte (PyPDF2) --> Nettoyage (unidecode, lower)--> Document LangChain<br>
<br>
<br>
2-CHUNKING <br>
<br>
Document --> Découpage (RecursiveCharacterTextSplitter)--> Liste de chunks<br>
<br>
<br>
3-INDEXATION VECTORIELLE <br>
<br>
Chunks --> Embeddings (Ollama - nomic-embed-text)--> Stockage dans ChromaDB (vector_db)<br>
<br>
<br>
4-RETRIEVAL (MULTI-QUERY)br>
<br>
Question utilisateur<br>
        --> Génération de 5 reformulations (LLM)<br>
        --> Chroma Retriever (similarité vectorielle)<br>
        --> Documents pertinents<br>
<br>
<br>
5-CHAÎNE RAG <br>
<br>
Documents pertinents<br>
        --> format_docs (concaténation texte)<br>
<br>
format_docs + question utilisateur<br>
        --> Prompt (contexte + question)<br>
        --> LLM ChatOllama (deepseek-r1:8b)<br>
        --> Réponse finale<br>



