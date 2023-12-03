  #https://github.com/openai/openai-cookbook/blob/950246dd0810470291aa9728c404a01aeab5a1e9/examples/How_to_call_functions_for_knowledge_retrieval.ipynb
import logging
import sys
from cb_f_config_agent import Conversation, chat_completion_with_function_execution, arxiv_functions
from rich import print
from rich.markdown import Markdown


logging.basicConfig(level=logging.INFO)

def setup_logging(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

# Rest of your code...

# Check if "debug=true" is provided as a command-line argument
if len(sys.argv) > 1 and sys.argv[1].lower() == "debug=true":
    setup_logging(debug=True)



# Start with a system message
paper_system_message = """You are arXivGPT, a helpful assistant pulls academic papers to answer user questions.
You summarize the papers clearly so the customer can decide which to read to answer their question.
You always provide the article_url and title so the user can understand the name of the paper and click through to access it.
Begin!"""
logging.info("---1. start conversation with:  "+paper_system_message)
paper_conversation = Conversation()
paper_conversation.add_message("system", paper_system_message)


# Add a user message
paper_conversation.add_message("user", "Hi, how does PPO reinforcement learning work?")
logging.info("\n---2. call chat_completion_with_function_execution with functions=arxiv_functions")
logging.info("\n---2. functions="+str(arxiv_functions))

chat_response = chat_completion_with_function_execution(
    paper_conversation.conversation_history, functions=arxiv_functions
)
assistant_message = chat_response["choices"][0]["message"]["content"]
paper_conversation.add_message("assistant", assistant_message)
print(Markdown(assistant_message))


# Add another user message to induce our system to use the second tool
paper_conversation.add_message(
    "user",
    "Can you read the PPO sequence generation paper for me and give me a summary",
)
logging.info("\n---3. call chat_completion_with_function_execution ")
updated_response = chat_completion_with_function_execution(
    paper_conversation.conversation_history, functions=arxiv_functions
)
print(Markdown(updated_response["choices"][0]["message"]["content"]))

