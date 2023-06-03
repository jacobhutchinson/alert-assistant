# Load the LLM model for smart_monitoring
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

def load_model(config):
    # Load callback manager
    #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # Load model using llama.cpp
    llm = LlamaCpp(
        model_path=f"./models/{config['llm_model']}", n_ctx=2048
    )

#    llm = LlamaCpp(
#        model_path=f"./models/{config['model']}", callback_manager=callback_manager, n_ctx=2048
#    )

    return llm
