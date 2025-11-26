from langchain_community.document_loaders import UnstructuredPDFLoader #1ere etape chargement du pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from unidecode import unidecode

import PyPDF2
import os

pdf_file = "./data/simulation_sonars.pdf"
embedding_model_name = "nomic-embed-text"

# chargement du PDF et nettoyage
if os.path.exists(pdf_file):
    texte_complet = ""

    with open(pdf_file, "rb") as fichier:
        lecteur = PyPDF2.PdfReader(fichier)

        for page in lecteur.pages:
            texte = page.extract_text()
            if texte:
                texte_complet += texte + "\n"

    # Nettoyage du texte
    texte_propre = (unidecode(texte_complet.strip().lower().replace(",", "")))

    # Convertir en Document LangChain
    documents = [Document(page_content=texte_propre)]

    print("PDF chargé et nettoyé")

else:
    raise FileNotFoundError("Fichier PDF non trouvé.")
#2eme etape Chuncking

splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
doc_chunks = splitter.split_documents(documents)
print(f"Doc split en {len(doc_chunks)} chunks.")

# intégrer les chunck dans une bas vectorielles

print("Pulling embedding model...")
#ollama.pull(embedding_model_name)


vector_store = Chroma.from_documents(
    documents=doc_chunks,
    embedding=OllamaEmbeddings(model=embedding_model_name),
    collection_name="pca_tutorial_collection",
    persist_directory="./vector_db" #ajout d'un dossier de destination pour les chuncks
)
print("Chunks stocker dans la base")
