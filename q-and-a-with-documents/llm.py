import io

from langchain.llms.openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA

from exceptions import NoApiKeyError, NoTxtDocUploadedError

def generate_answer(uploaded_doc: io.BytesIO, question: str, api_key: str) -> str:
    if not api_key.strip():
        raise NoApiKeyError()

    if not uploaded_doc:
        raise NoTxtDocUploadedError()

    documents = uploaded_doc.read().decode()
    txt_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = txt_splitter.create_documents([documents])
    embeddings = OpenAIEmbeddings(api_key=api_key)
    db = Chroma.from_documents(docs, embeddings)
    retriever = db.as_retriever()
    qna = RetrievalQA.from_chain_type(llm=OpenAI(api_key=api_key), chain_type='stuff', retriever=retriever)

    return qna.run(question)

