from typing import List, Tuple
import json

from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage
from langchain.chains import LLMChain

from exceptions import NoApiKeyError, NoIngredientsError, NoRecipesFound


def suggest_recipe(ingredients: List[str], api_key: str) -> Tuple[str, str]:
    """
    Ask AI for recipe suggestions based on the given ingredients.

    :param ingredients: list of ingredients
    :param api_key: API key for OpenAI
    :returns: a tuple of dish name and recipe
    :raises NoRecipesFound: if no recipes are found for the given ingredients

    """
    if not api_key.strip():
        raise NoApiKeyError()

    if not list(filter(lambda x: x, list(map(lambda x: x != None and x.strip(), ingredients)))):
        raise NoIngredientsError()

    chat_template_dish_name = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content='You are an assistant chef who can suggest dishes based on ingredients provided.'),
            HumanMessagePromptTemplate.from_template(
                '''
                Suggest me the recipe of a dish that can be prepared using the following ingredients.
                INGREDIENTS: {ingredients}

                If a recipe is found return the output in the following JSON format
                OUTPUT JSON FORMAT: {{"dish_name": "name of the dish", "recipe": "recipe for the dish"}}

                else, output should be in the following JSON format
                OUTPUT JSON FORMAT: {{"error": "NO_RECIPES_FOUND", "message": "funny AI response"}}
                '''
            )
        ]
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.5, api_key=api_key, verbose=True)

    recipe_chain = LLMChain(llm=llm, prompt=chat_template_dish_name, verbose=True)

    ai_output_raw = recipe_chain.run(ingredients=', '.join(ingredients))
    ai_output_json = json.loads(ai_output_raw)

    err = ai_output_json.get('error')
    if err:
        raise NoRecipesFound(ai_output_json.get('message'))

    dish_name = ai_output_json.get('dish_name')
    recipe = ai_output_json.get('recipe')

    return dish_name, recipe
