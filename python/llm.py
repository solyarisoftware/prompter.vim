# https://docs.litellm.ai/docs/tutorials/azure_openai
# https://docs.litellm.ai/docs/tutorials/text_completion
# !pip install -U litellm

import os

from litellm import text_completion
from typing import Tuple

# custom modules
# import openai_setup
import calculate_latency
import utils

# mandatory OS variables
MODEL = os.getenv('MODEL')

# optional OS variables
MAX_TOKENS = os.getenv('MAX_TOKENS', 1000)
TEMPERATURE = os.getenv('TEMPERATURE', 0.5)
STOP = os.getenv('STOP', '')


def generate(
    prompt: str,
    model: str = MODEL,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
    stop: [str] = STOP
) -> Tuple[str, str]:
    ''' invoke the LLM provider model text completion '''

    start_time = calculate_latency.start_timer()

    response = text_completion(model=model, prompt=prompt, temperature=float(temperature), max_tokens=int(max_tokens), stop=stop)

    latency_str, latency_msecs = calculate_latency.stop_timer(start_time)

    # debug
    # print(response)

    completion_text = response['choices'][0]['text']

    # sometime text-da-vinci-003 insert newlines
    completion_text = completion_text.strip()

    finish_reason = response['choices'][0]['finish_reason']

    completion_report = utils.completion_statistics(latency_str, latency_msecs, response['usage'], completion_text, finish_reason)

    return (completion_text, completion_report)


if __name__ == '__main__':

    print(utils.model_settings(MODEL, TEMPERATURE, MAX_TOKENS, STOP))

    prompt = 'La città soprannominata "la superba", in una parola, è'

    completion, report = generate(prompt=prompt)

    print('' + prompt)
    print('' + completion)
    print('' + report)
    print()
