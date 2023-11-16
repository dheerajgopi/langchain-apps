from langchain.llms.openai import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

from exceptions import NoApiKeyError


def summarize_text(txt: str, api_key: str) -> str:
    """
    Generates a summary for the long text provided as the input.
    """
    if not api_key.strip():
        raise NoApiKeyError()

    llm = OpenAI(temperature=0, api_key=api_key)
    txt_splitter = CharacterTextSplitter()
    split_txt = txt_splitter.split_text(txt)
    docs = [Document(page_content=t) for t in split_txt]
    chain = load_summarize_chain(llm, chain_type='map_reduce')

    return chain.run(docs)