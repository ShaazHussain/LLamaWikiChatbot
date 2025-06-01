from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# Setting Ollama as the default LLM and embedding model
Settings.llm = Ollama(model="llama3", request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", request_timeout=120.0)

def wikipage_list(query):
    return [p.strip() for p in query.split(",") if p.strip()]

def create_wikidocs(wikipage_requests):
    reader = WikipediaReader()
    documents = []
    for page in wikipage_requests:
        try:
            wiki_docs = reader.load_data(pages=[page])  # returns a list
            documents.extend(wiki_docs)
        except Exception as e:
            print(f'Error loading "{page}": {e}')
    return documents

def create_index(query):
    wikipage_requests = wikipage_list(query)
    documents = create_wikidocs(wikipage_requests)
    index = VectorStoreIndex.from_documents(documents)
    return index

if __name__ == "__main__":
    query = "paris, lagos, lao"
    index = create_index(query)
    print("INDEX CREATED:", index)
