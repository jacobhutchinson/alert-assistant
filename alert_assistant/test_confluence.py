from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import TextLoader, ConfluenceLoader, DirectoryLoader

query = """The Salesforce Data Extensions pipeline ran into the following error:

```
ERROR - __main__ - salesforce_data_extensions_run.extension_preprocessing - 
Extension Activation_SMB_CRB_GotRate_AWS was not found at location 
s3://upstart/env/production/partner/salesforce/extensions/
Activation_SMB_CRB_GotRate_AWS/Activation_SMB_CRB_GotRate_AWS_20221107.csv
```

Can you summarize the issue and suggest resolutions?"""

with open('./keys/confluence_key', 'r') as file:
    confluence_key = file.read().rstrip()

confluence_loader = ConfluenceLoader(
    url="https://upstartnetwork.atlassian.net/wiki/",
    username="jacob.hutchinson@upstart.com",
    api_key=confluence_key,
    
)
documents = confluence_loader.load(space_key="DE", include_attachments=False, limit=50)

text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

#txt_loader = DirectoryLoader('./data/', glob="**/*.txt")
#txt_loader = TextLoader('./data/state_of_the_union.txt', encoding='utf8')

embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

db = Chroma.from_documents(texts, embeddings)

#index = VectorstoreIndexCreator(
#    vectorstore_cls=Chroma, 
#    embedding=embeddings,
#    text_splitter=CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
#).from_documents(documents)

#retriever = index.vectorstore.as_retriever()

retriever = db.as_retriever()

docs = retriever.get_relevant_documents(query)
print(docs)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="./models/wizard-vicuna-13B.ggml.q5_1.bin", callback_manager=callback_manager, verbose=True, n_ctx=2048
)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

qa.run(query)
