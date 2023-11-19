from typing import List

from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage

from exceptions import NoApiKeyError, NoIngredientsError


def suggest_recipe(ingredients: List[str], api_key: str) -> str:
    if not api_key.strip():
        raise NoApiKeyError()

    if not list(filter(lambda x: x, list(map(lambda x: x != None and x.strip(), ingredients)))):
        raise NoIngredientsError()

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content='You are an assistant chef who can suggest recipes based on ingredients provided.'),
            HumanMessagePromptTemplate.from_template(
                '''
                Suggest a recipe based on the following ingredients.

                INGREDIENTS: {ingredients}
                '''
            )
        ]
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.5, api_key=api_key, verbose=True)
    return llm(chat_template.format_messages(ingredients=', '.join(ingredients))).content
