import logging

import streamlit as st
from openai import AuthenticationError, RateLimitError

from llm import generate_answer
from exceptions import NoApiKeyError, NoTxtDocUploadedError


logging.basicConfig(level=logging.INFO)

def init():
    st.set_page_config(page_title="QnA With Documents")
    st.title("QnA With Documents")

    uploaded_doc = st.file_uploader("Upload a text document", type='txt')
    question = st.text_input("Ask your question", disabled=not uploaded_doc)
    answer = ""
    warning = ""

    with st.form("qna-form"):
        openai_api_key = st.text_input("OpenAI API Key", type="password", disabled=not question)
        submitted = st.form_submit_button("Submit", disabled=not(uploaded_doc and question))

        if submitted:
            with st.spinner("Thinking..."):
                try:
                    answer = generate_answer(uploaded_doc, question, openai_api_key)
                except NoApiKeyError:
                    warning = "Please enter your OpenAI API key"
                except AuthenticationError:
                    warning = "OpenAI authentication failed. Please provide a valid API key"
                except RateLimitError:
                    warning = "You have exceeded your quota in OpenAI. Please check your OpenAI plan and billing details"
                except Exception as e:
                    logging.error(f"Unknown error: {e}", exc_info = True)
                    warning = "Something went wrong at our end. Please re-try later"

            if answer:
                st.info(answer)
            elif warning:
                st.warning(warning)
            else:
                st.info("Sorry..unable to answer your question..")


if __name__ == "__main__":
    init()
