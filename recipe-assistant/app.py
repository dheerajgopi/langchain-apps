import logging
from typing import Tuple

import streamlit as st
from streamlit_tags import st_tags
from openai import AuthenticationError, RateLimitError

from exceptions import NoApiKeyError, NoIngredientsError, NoRecipesFound
from llm import suggest_recipe


logging.basicConfig(level=logging.INFO)

def init():
    st.set_page_config(page_title='Recipe Assistant')
    st.title('Recipe Assistant')

    # sidebar with text input for entering OpenAI API key
    openai_api_key = st.sidebar.text_input('OpenAI API Key:', type='password')

    # form for entering the ingredients and asking the AI assistant for recipe suggestions
    with st.form('ingredients-form'):
        ingredients = st_tags(label='Enter your ingredients', maxtags=10, key='ingredients')
        submitted = st.form_submit_button('Suggest')
        dish = recipe = warning = ""

        # form submission logic
        if submitted:
            with st.spinner("Thinking..."):
                dish, recipe, warning = ask_for_recipes(ingredients, openai_api_key)

    # displaying the output
    if dish:
        st.info(dish + "\n\n" + recipe)
    elif warning:
        st.warning(warning)

def ask_for_recipes(ingredients: str, api_key: str) -> Tuple[str, str, str]:
    """
    Helper function for getting the recipe from AI, and extract the text to be shown in UI.
    Various exception scenarios are also handled here, so that proper message can be shown in the UI.

    :param ingredients: list of ingredients
    :param api_key: API key for OpenAI
    :returns: a tuple of dish name, recipe and a error message.
    """

    try:
        dish, recipe = suggest_recipe(ingredients, api_key)
        return dish, recipe, ""
    except NoApiKeyError:
        return "", "", "Please enter your OpenAI API key"
    except NoIngredientsError:
        return "", "", "Please provide the ingredients"
    except NoRecipesFound as nrf:
        return "", "", str(nrf)
    except AuthenticationError:
        return "", "", "OpenAI authentication failed. Please provide a valid API key"
    except RateLimitError:
        return "", "", "You have exceeded your quota in OpenAI. Please check your OpenAI plan and billing details"
    except Exception as e:
        logging.error(f"Unknown error: {e}", exc_info = True)
        return "", "", "Something went wrong at our end. Please re-try later"


if __name__ == '__main__':
    init()
