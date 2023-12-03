import os
import sys
import pypdf

from langchain.chat_models import ChatOpenAI
from llama_index import LLMPredictor, PromptHelper, SimpleDirectoryReader, GPTVectorStoreIndex
import openai


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

import logging

def setup_logging(debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
#   else:
#       logging.basicConfig(level=logging.INFO)

# Rest of your code...

# Check if "debug=true" is provided as a command-line argument
if len(sys.argv) > 1 and sys.argv[1].lower() == "debug=true":
    setup_logging(debug=True)
else:
    setup_logging(debug=False)




def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap_ratio = 0.2
    # set chunk size limit
    chunk_size_limit = 600 

    # define LLM

    logging.debug("\n call LLMPredictor")
    #llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name='gpt-3.5-turbo', max_tokens=num_outputs))
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name='gpt-4-0613', max_tokens=num_outputs))

    logging.debug("\n call prompt_helper")
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap_ratio, chunk_size_limit=chunk_size_limit)
 
    logging.debug("\n call SimpleDirectoryReader")
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    logging.debug("\n call PTVectorStoreIndex.from_documents")   # Request to OpenAI API' method=post path=https://api.openai.com/v1/embeddings
    index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    #index.save_to_disk('index.json')

    logging.debug("\n call index.storage_context.persist")
    index.storage_context.persist(persist_dir=directory_path)  # generate docstore.json, index_store.json, vector_store.json, graph_sstore.json

    return index



def ask_ai():
    #index = GPTSimpleVectorIndex.load_from_disk('index.json')
    index = construct_index("./data")
    while True: 
        prompt = input("What do you want to ask? (Type 'exit' to quit) ")
        
        # Check if the input is 'exit'
        if prompt.lower() == 'exit':
            break

        logging.debug("\n call index.as_query_engine")
        query_engine = index.as_query_engine(response_mode="compact")

        logging.debug("\n --------------------call query_engine.query")

        response = query_engine.query(prompt)    #  method=post path=https://api.openai.com/v1/embeddings, # method=post path=https://api.openai.com/v1/completion
        print(f"Response: {response.response}")


if __name__ == "__main__":
    ask_ai()