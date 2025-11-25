import requests
from fastmcp import FastMCP
from search_tools import SearchTools
from minsearch import AppendableIndex

mcp = FastMCP("Search 🚀")
def initialise_index():
    docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    documents = []

    for course in documents_raw:
        course_name = course['course']

        for doc in course['documents']:
            doc['course'] = course_name
            documents.append(doc)
    index = AppendableIndex(
        text_fields=["question", "text", "section"],
        keyword_fields=["course"]
    )

    index.fit(documents)
    return index

index = initialise_index()
tools = SearchTools(index)

mcp.tool(tools.search)
mcp.tool(tools.add_entry)
if __name__ == "__main__":
    mcp.run(transport="sse")


