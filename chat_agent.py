import chainlit as cl
from chainlit.input_widget import Select, TextInput
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from llama_index.core.agent.react import ReActAgent


# Setting Ollama as the default LLM and embed model for all of LlamaIndex
Settings.llm = Ollama(model="llama3", request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", request_timeout=120.0)

index = None
agent = None

@cl.on_chat_start
async def on_chat_start():
    await cl.ChatSettings(
        [
            Select(
                id="model_select",
                label="Choose Ollama Model",
                values=["llama3", "llama2", "mistral"],  # List your local models here
                initial_index=0,
            ),
            TextInput(
                id="wiki_query",
                label="Wikipedia page(s) (comma-separated)",
                initial_value="",
            ),
        ]
    ).send()

def wikisearch_engine(index):
    return index.as_query_engine()

def create_react_agent(MODEL, index):
    query_engine_tool = QueryEngineTool.from_defaults(
        query_engine=wikisearch_engine(index),
        description="Wikipedia search tool for answering questions based on indexed Wikipedia pages.",
        name="WikipediaSearch"
    )
    llm = Ollama(model=MODEL, request_timeout=120.0)
    agent = ReActAgent.from_tools(
    tools=[query_engine_tool],
    llm=llm,
    verbose=True,
)
    return agent

@cl.on_settings_update
async def setup_agent(settings):
    global agent
    global index
    query = settings["wiki_query"]
    if not query or not query.strip():
        await cl.Message(author="Agent", content="Please enter at least one Wikipedia page to index.").send()
        return
    pages = [p.strip() for p in query.split(",") if p.strip()]
    if not pages:
        await cl.Message(author="Agent", content="No valid Wikipedia pages provided.").send()
        return
    reader = WikipediaReader()
    documents = await cl.make_async(reader.load_data)(pages=pages)
    index = VectorStoreIndex.from_documents(documents)
    MODEL = settings["model_select"]
    agent = create_react_agent(MODEL, index)
    await cl.Message(
        author="Agent", content=f"""Wikipage(s) "{query}" successfully indexed"""
    ).send()

@cl.on_message
async def main(message: cl.Message):
    if agent:
        agent_response = await agent.achat(message.content)
        # Extract the text from the response object
        if hasattr(agent_response, "response"):
            response_text = agent_response.response
        elif hasattr(agent_response, "message"):
            response_text = agent_response.message
        elif hasattr(agent_response, "text"):
            response_text = agent_response.text
        else:
            response_text = str(agent_response)  # fallback

        # Remove Markdown code block formatting if present
        if response_text.strip().startswith("```"):
            response_text = "\n".join(response_text.strip().split('\n')[1:-1]).strip()
        await cl.Message(author="Agent", content=response_text).send()


