# ChatBots


Here is a simple example of building a chatbot using OpenAI's GPT model, LlamaIndex, and LangChain. LlamaIndex offers tools for indexing custom content. In this straightforward example, a PDF file (Conflicts of Interest FAQ.pdf) is stored in the 'data' folder. LangChain provides wrappers for OpenAI APIs. The generated embeddings, including indices and graphs, are also saved in the 'data' folder.

You can execute the script by running:

```bash
pip install openai
pip install llama-index 
pip install langchain 

```

```python
python simplebot.py
```

If you want to understand how the different components are integrated, you can run the script with the debug mode as follows:

```python
python simplebot.py debug=true
```

The provided diagram offers a visual explanation.

![Alt Text](https://github.marqeta.com/wli1/ChatBots/blob/main/Bot_flow.png)
