import os
from langchain.document_loaders import ConfluenceLoader
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def check_config(config, key, fields):
    return all([(config[key][field] and config[key][field].len() != 0) for field in fields])

def load_indexes(config, docs=[]):
    if check_config(config, "confluence", ["username", "api_key", "url", "confluences_spaces"]):
        confluence_loader = ConfluenceLoader(
            url=config["confluence"]["url"],
            username=config["confluence"]["username"],
            api_key=config["confluence"]["api_key"]
        )
        for space in config["confluence"]["confluence_spaces"]:
            docs.extend(confluence_loader.load(space_key=space)

    if check_config(config, "jira", ["url", "username", "api_key"]):
        # TODO: Load Jira documents here
        raise NotImplementedError

    if check_config(config, "local_files", ["csv"]):
        for file in os.listdir(config["local_files"]["csv"]):
            if file.endswith(".csv"):
                csv_loader = CSVLoader(
                    file_path=os.path.join(config["local_files"]["csv"], file)
                )
                docs.extend(csv_loader.load())

    if check_config(config, "local_files", ["txt"]):
        for file in os.listdir(config["local_files"]["txt"]):
            if file.endswith(".txt"):
                txt_loader = TextLoader(
                    file_path=os.path.join(config["local_files"]["txt"], file)
                )
                docs.extend(txt_loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["text_chunk_size"],
        chunk_overlap=config["text_chunk_overlap_size"]
    )

    return text_splitter.split_documents(documents)
