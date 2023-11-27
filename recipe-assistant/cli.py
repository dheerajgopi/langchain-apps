import click

from openai import AuthenticationError, RateLimitError
from exceptions import NoIngredientsError, NoRecipesFound

from app import suggest_recipe


@click.command()
@click.option('--ingredients', default='', help='Separate each ingredients by a comma')
@click.option('--api_key', default='', help='OpenAI API key')
def cli_app(ingredients: str, api_key: str):
    if not ingredients.strip():
        click.echo("`ingredients` cannot be blank", err=True)
        return

    if not api_key.strip():
        click.echo("`api_key` cannot not be blank", err=True)
        return

    try:
        ingredient_list = list(map(lambda x: x.strip(), ingredients.split(',')))
        dish, recipe = suggest_recipe(ingredient_list, api_key)
        click.echo(f"\n{dish}\n\n{recipe}")
    except NoRecipesFound as nrf:
        click.echo(str(nrf), err=True)
    except AuthenticationError:
        click.echo("OpenAI authentication failed. Please provide a valid API key", err=True)
    except RateLimitError:
        click.echo("You have exceeded your quota in OpenAI. Please check your OpenAI plan and billing details", err=True)
    except Exception as e:
        click.echo("Something went wrong at our end. Please re-try later", err=True)


if __name__ == '__main__':
    cli_app()
