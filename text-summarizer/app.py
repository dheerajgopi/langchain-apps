import logging

import streamlit as st
from openai import AuthenticationError, RateLimitError

from exceptions import NoApiKeyError
from llm import summarize_text


logging.basicConfig(level=logging.INFO)

def init():
    st.set_page_config(page_title="Text Summarization App")

    st.title("Text Summarization App")

    summary = ""
    warning = ""
    txt_input = st.text_area("Enter your text", '', height=200)
    with st.form('summarize-form'):
        open_api_key = st.text_input("Open API Key", type='password', disabled=not txt_input)
        submitted = st.form_submit_button("Submit")

        if submitted:
            with st.spinner("Summarizing..."):
                try:
                    summary = summarize_text(txt_input, open_api_key)
                except NoApiKeyError:
                    warning = "Please enter your OpenAI API key"
                except AuthenticationError:
                    warning = "OpenAI authentication failed. Please provide a valid API key"
                except RateLimitError:
                    warning = "You have exceeded your quota in OpenAI. Please check your OpenAI plan and billing details"
                except Exception as e:
                    logging.error(f"Unknown error: {e}", exc_info = True)
                    warning = "Something went wrong at our end. Please re-try later"

    if summary:
        st.info(summary)
    elif warning:
        st.warning(warning)
    else:
        st.info("Sorry..unable to generate summary..")


if __name__ == '__main__':
    init()