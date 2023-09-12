import openai
from typing import Tuple

# custom modules
import openai_setup
import calculate_latency
import utils


def generate(
    prompt: str,
    llm_provider: str,
    model_or_deployment: str,
    completion_mode: str,
    temperature: float = openai_setup.TEMPERATURE,
    max_tokens: int = openai_setup.MAX_TOKENS,
    stop: [str] = openai_setup.STOP
) -> Tuple[str, str]:
    ''' call the openai chat completion service or text completion service '''

    if completion_mode == openai_setup.CHAT_COMPLETION_MODE:
        return openai_chat_completion(
            prompt=prompt,
            llm_provider=llm_provider,
            model_or_deployment=model_or_deployment,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )
    else:
        return openai_text_completion(
            prompt=prompt,
            llm_provider=llm_provider,
            model_or_deployment=model_or_deployment,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )


def openai_chat_completion(
    prompt: str,
    llm_provider: str,
    model_or_deployment: str,
    temperature: float = openai_setup.TEMPERATURE,
    max_tokens: int = openai_setup.MAX_TOKENS,
    stop: [str] = openai_setup.STOP
) -> Tuple[str, str]:
    ''' call the openai chat completion service using it just as a prompt completion '''

    start_time = calculate_latency.start_timer()

    # parameters tht are common for both openai and Openai through Azure
    params = {
        'temperature': temperature,
        'max_tokens': max_tokens,
        'stop': stop,

        # TODO: stuffing the prompt in the SYSTEM is the correct way?
        'messages': [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': ''}
        ]
    }

    # WARNING:
    # if llm_provider is Azure must be specified the DEPLOYMENT name (corresponding one-to-one to a specific Openai model)
    # if llm_provider is Openai must be specified INSTEAD the real openai MODEL name
    # https://github.com/openai/openai-python#microsoft-azure-endpoints
    # https://github.com/openai/openai-cookbook/blob/main/examples/azure/completions.ipynb
    if llm_provider == openai_setup.AZURE_LLM_PROVIDER:
        params['deployment_id'] = model_or_deployment
    else:
        params['model'] = model_or_deployment

    response = openai.ChatCompletion.create(**params)

    latency_str, latency_msecs = calculate_latency.stop_timer(start_time)

    # debug
    # print(response)

    completion_text = response['choices'][0]['message']['content']
    finish_reason = response['choices'][0]['finish_reason']
    completion_report = utils.completion_statistics(latency_str, latency_msecs, response['usage'], completion_text, finish_reason)

    return (completion_text, completion_report)


def openai_text_completion(
    prompt: str,
    llm_provider: str,
    model_or_deployment: str,
    temperature: float = openai_setup.TEMPERATURE,
    max_tokens: int = openai_setup.MAX_TOKENS,
    stop: [str] = openai_setup.STOP
) -> Tuple[str, str]:
    ''' call the openai chat completion service (warning: this is the old completion (until text-davinci-003, NO chat) '''

    start_time = calculate_latency.start_timer()

    # parameters tht are common for both openai and Openai through Azure
    params = {
        'temperature': temperature,
        'max_tokens': max_tokens,
        'stop': stop,
        'prompt': prompt
    }

    # WARNING:
    # if llm_provider is Azure must be specified the DEPLOYMENT name (corresponding one-to-one to a specific Openai model)
    # if llm_provider is Openai must be specified INSTEAD the real openai MODEL name
    # https://github.com/openai/openai-python#microsoft-azure-endpoints
    # https://github.com/openai/openai-cookbook/blob/main/examples/azure/completions.ipynb
    if llm_provider == openai_setup.AZURE_LLM_PROVIDER:
        params['deployment_id'] = model_or_deployment
    else:
        params['model'] = model_or_deployment

    response = openai.Completion.create(**params)

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
    ''' unit test '''

    # llm_provider, completion_mode, model_chat_completion, model_text_completion = setup()
    defaults = openai_setup.setup()
    print(f'{defaults.llm_provider}, {defaults.completion_mode}, {defaults.model_chat_completion}, {defaults.model_text_completion}')
    print()

    prompt = 'La città soprannominata "la superba", in una parola, è'

    '''
    completion, report = openai_text_completion(
        prompt=prompt,
        llm_provider=defaults.llm_provider,
        model_or_deployment=defaults.model_text_completion
    )

    print('' + prompt)
    print('' + completion)
    print('' + report)
    print()
    '''

    completion, report = openai_chat_completion(
        prompt=prompt,
        llm_provider=defaults.llm_provider,
        model_or_deployment=defaults.model_chat_completion
    )

    print('' + prompt)
    print('' + completion)
    print('' + report)
    print()
