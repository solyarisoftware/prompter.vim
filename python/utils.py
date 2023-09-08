# utilities to be used by python functions

PLUGIN_NAME = 'prompter.vim'
AUTHOR = 'giorgio.robino@gmail.com'
VERSION = '0.1 (September 2nd, 2023)'


def version():
    return f'{PLUGIN_NAME}, by {AUTHOR}, version {VERSION}'


def help():
    return '\n'.join([
        'Version:',
        version(),
        '',
        'Commands:',
        'PrompterSetup: read OS environment variables',
        'PrompterComplete: complete the prompt',
        'prompterModel: show model attributes'
    ])


def model_settings(
    llm_provider: str,
    model: str,
    completion_mode: str,
    temperature: float,
    max_tokens: int,
    stop: [str],
) -> str:
    ''' print the model configuration parameters '''

    single_line_to_print = (
        f'Current buffer model: {llm_provider}/{model} '
        f'(completion mode: {completion_mode} '
        f'temperature: {temperature}, '
        f'max tokens: {max_tokens}'
    )

    if stop and any(stop):
        single_line_to_print += f', stop: {stop})'
    else:
        single_line_to_print += ')'

    return single_line_to_print


def speed(tokens: int, latency_msecs: int) -> str:
    ''' speed as the tokens/latency ratio where latency is measured in seconds '''

    latency_secs = latency_msecs / 1000
    v = tokens / latency_secs

    # round to an integer
    return str(round(v))


def completion_statistics(
    latency_str: str,
    latency_msecs: int,
    usage: str,
    completion_text: str,
    finish_reason: str,
) -> str:
    ''' print a statistics data report including: latency times, tokens consumption, words and chars counts '''

    completion_tokens = usage['completion_tokens']
    prompt_tokens = usage['prompt_tokens']
    total_tokens = usage['total_tokens']

    tokens_report = f'{total_tokens} (prompt: {prompt_tokens} completion: {completion_tokens})'

    nchars = len(completion_text)

    # rough calculation considering a blank separated words
    nwords = len(completion_text.split())

    nlines = len(completion_text.splitlines())

    text_statistics = f'Words: {nwords} Chars: {nchars}'

    # don't print  number of lines if the completion is just a single line
    if nlines > 1:
        nlines_statistics = f', Lines: {nlines}'
        text_statistics += nlines_statistics

    vel = speed(total_tokens, latency_msecs)

    single_line_to_print = f'Latency: {latency_str} Tokens: {tokens_report} Speed: {vel} {text_statistics}'

    # don't print finish reason if the completion finished normally
    if finish_reason != 'stop':
        output_finish_reason = f', Finish reason: {finish_reason}'
        single_line_to_print += output_finish_reason

    return single_line_to_print


if __name__ == '__main__':
    print(help())
    print()

    usage = {
        'completion_tokens': 30,
        'prompt_tokens': 10,
        'total_tokens': 20
    }
    line = completion_statistics(
        '1200ms (1.2s)',
        1200,
        usage,
        'tanto va la gatta al lardo, che ci lascia lo zampino',
        'stop',
    )
    print('completion_statistics')
    print(line)
    print()

    line = model_settings(
        'azure',
        'text-davinci-003',
        'text',
        0.4,
        2048,
        "a: u:"
    )
    print('model_settings')
    print(line)
    print()

    line = model_settings(
        'azure',
        'text-davinci-003',
        'text',
        0.4,
        2048,
        None
    )
    print('model_settings')
    print(line)
    print()

    print('Speed')
    print(speed(150, 354))
