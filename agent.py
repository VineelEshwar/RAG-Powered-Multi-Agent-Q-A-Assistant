# agent.py

from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.utilities import WikipediaAPIWrapper
import os


# Logging function
def log_decision(tool_name, query, result):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"Query: {query}\nUsed Tool: {tool_name}\nResult: {result}\n\n")


# Load FAISS index
def load_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 3})


retriever = load_retriever()


# Set up local LLM
llm = Ollama(model="llama3")


# RAG Chain
prompt_template = """
You are a helpful assistant. Use the following context to answer the question.
If you cannot find the answer in the context, say so clearly.

Context:
{context}

Question:
{question}

Answer:
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)


def rag_query(q):
    result = rag_chain.run(q)
    log_decision("RAG QA", q, result)
    return result


# Calculator tool
def calculate_func(input_str):
    try:
        result = str(eval(input_str))
        log_decision("Calculator", input_str, result)
        return result
    except Exception as e:
        error_msg = f"Error evaluating expression: {e}"
        log_decision("Calculator", input_str, error_msg)
        return error_msg


# Dictionary tool
def dictionary_lookup(word):
    from PyDictionary import PyDictionary
    try:
        meaning = PyDictionary().meaning(word)
        if meaning:
            result = "\n".join([f"{k}: {', '.join(v)}" for k, v in meaning.items()])
        else:
            result = "Word not found."
    except Exception as e:
        result = f"Error looking up word: {e}"
    log_decision("Dictionary", word, result)
    return result


# Wikipedia tool
try:
    wiki = WikipediaAPIWrapper()
    wikipedia_tool = Tool(name="Wikipedia", func=wiki.run, description="Useful for general knowledge")
except Exception as e:
    wikipedia_tool = None


# Tools list
tools = [
    Tool(name="Calculator", func=calculate_func, description="Useful for calculations like math problems"),
    Tool(name="Dictionary", func=dictionary_lookup, description="Useful for word definitions and meanings"),
    Tool(name="RAG QA System", func=rag_query, description="Useful for answering questions using internal documents"),
]

if wikipedia_tool:
    tools.append(wikipedia_tool)

# Initialize agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)
