# LLamaWikiChatbot
This project is a local conversational Retrieval-Augmented Generation (RAG) chatbot that uses LlamaIndex integrated with Ollama to answer questions based on Wikipedia content.

![image](https://github.com/user-attachments/assets/dc0fe891-c976-471e-89b4-2ddc3ec9271d)
![image](https://github.com/user-attachments/assets/01dc7191-2746-4439-b12d-6323f1cf45e9)
![image](https://github.com/user-attachments/assets/7d33a1a0-bbac-4cf1-a340-8ddf6f354eec)

## Features

- **Local, private and API-key-free**: No OpenAI or cloud dependencies.
- **Chat UI**: Powered by [Chainlit](https://www.chainlit.io/).
- **Customizable**: Choose your Ollama model and Wikipedia pages to index.
- **Fast vector search**: Uses Ollama embeddings for Wikipedia document retrieval.
- **ReAct agent**: Uses LlamaIndex’s ReActAgent for context-aware Q&A.

## How It Works

- **`chat_agent.py`**: Launches a chat UI where you select an Ollama model and Wikipedia pages. It indexes those pages and lets you ask questions, answering using only the indexed content.
- **`index_wikipages.py`**: Standalone script to build a Wikipedia vector index from a list of page titles.

## Setup

1. **Install Ollama** and pull required models (e.g., `llama3`, `nomic-embed-text`).
2. **Install dependencies**.
3. **Run the chat app**.
