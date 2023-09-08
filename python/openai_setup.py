import os
import openai
from collections import namedtuple
from typing import NamedTuple

#
# LLM_PROVIDER
#
# openai python module allows to use original Openai models, trough two different llm providers:
# 1. 'openai' itself
# 2. 'azure' if the openai models are supplied from Microsoft Azure
#
OPENAI_LLM_PROVIDER = 'openai'
AZURE_LLM_PROVIDER = 'azure'

#
# COMPLETION_MODE
#
# openai has two different types of create completion API endpoints:
# - TEXT_COMPLETION
#   this is the old way, suitable for models until text-davinci-003
#
# - CHAT_COMPLETION
#   this is the new model that have 'roles (syst / user / assistant)
#   this mode is mandatory for new models like gpt-3.5 or pt4
#
#   WARNING
#   is up to you to know is a given model or deployment_id is suitable for the COMPLETION_TYPE
#
CHAT_COMPLETION_MODE = 'chat'
TEXT_COMPLETION_MODE = 'text'

# other model parameters default
MAX_TOKENS = 100
TEMPERATURE = 0.7

STOP = None
TOP_P = 0.5
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0


def setup() -> NamedTuple:
    ''' check required OS variables and setup defaults '''

    llm_provider = os.getenv('OPENAI_LLM_PROVIDER').lower()

    if llm_provider == AZURE_LLM_PROVIDER:
        #
        # Azure is a pain in the ass
        #
        openai.api_type = AZURE_LLM_PROVIDER

        # Your Azure OpenAI resource's endpoint value.
        openai.api_base = os.getenv('AZURE_OPENAI_API_ENDPOINT')

        # set default values
        openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        openai.api_version = os.getenv('AZURE_OPENAI_API_VERSION')  # '2023-05-15'

        # WARNING in azure it's the DEPLOYMENT name (that correspond to an Openai model)
        model_chat_completion = os.getenv('AZURE_DEPLOYMENT_NAME_CHAT_COMPLETION')  # 'gpt-35-turbo', or soon 'gpt-35-turbo-0613'
        model_text_completion = os.getenv('AZURE_DEPLOYMENT_NAME_TEXT_COMPLETION')  # 'text-davinci-003'

    elif llm_provider == OPENAI_LLM_PROVIDER:
        #
        # Openai
        #
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # set default values
        model_chat_completion = os.getenv('OPENAI_MODEL_NAME_CHAT_COMPLETION')  # 'gpt-3.5-turbo'
        model_text_completion = os.getenv('OPENAI_MODEL_NAME_TEXT_COMPLETION')  # 'text-davinci-003'

    else:
        raise Exception('OPENAI_LLM_PROVIDER valid values: \'azure\' or \'openai\'')

    # common settings
    completion_mode = os.getenv('OPENAI_COMPLETION_MODE')  # 'chat' or 'text'
    temperature = float(os.getenv('OPENAI_TEMPERATURE'))  # 0.7
    max_tokens = int(os.getenv('OPENAI_MAX_TOKENS'))  # 100
    stop = os.getenv('OPENAI_STOP').split()  # "a: u:"

    GlobalDefaults = namedtuple('GlobalDefaults', [
        'llm_provider',
        'completion_mode',
        'model_chat_completion',
        'model_text_completion',
        'temperature',
        'max_tokens',
        'stop'
    ])

    return GlobalDefaults(
        llm_provider,
        completion_mode,
        model_chat_completion,
        model_text_completion,
        temperature,
        max_tokens,
        stop
    )


if __name__ == '__main__':
    ''' unit test '''

    # llm_provider, completion_mode, model_chat_completion, model_text_completion = setup()
    try:
        defaults = setup()
        print(
            f'{defaults.llm_provider}, '
            f'{defaults.completion_mode}, '
            f'{defaults.model_chat_completion}, '
            f'{defaults.model_text_completion}, '
            f'{defaults.temperature}, '
            f'{defaults.max_tokens}, '
            f'{defaults.stop}'
        )
    except Exception as e:
        print(f'ERROR: {e}')
