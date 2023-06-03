# Main function for running smart_monitoring
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from .load_model import load_model
from .load_indexes import load_indexes
from .prompts import PROMPT_TEMPLATE, REFINE_TEMPLATE, QUERY1, QUERY2
import time

def main(args, config):

    documents = load_indexes()
    
    # Load embeddings model
    embeddings = HuggingFaceEmbeddings(model_name=config["embeddings_model"])

    #Load LLM
    llm = load_model(config)

    # Create Chroma db and retriever
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever()

    # Create chain
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    # Run test
    output = qa.run(QUERY1)

    print(f"Prompt:\n{QUERY1}\n")
    print(f"Response:\n{output}\n")

    time.sleep(3)

    print("Relevant Confluence documents:")
    output_src = []
    i = 1
    for doc in retriever.get_relevant_documents(QUERY1):
        src = doc.metadata['source']
        if src not in output_src:
            print(f"{i}. {src}")
            output_src.append(src)
            i += 1
