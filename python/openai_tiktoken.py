import tiktoken


def num_tokens(text: str, model_name: str) -> int:
    ''' Returns the number of tokens in a text string.
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    '''
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens


if __name__ == "__main__":
    ''' unit test '''

    prompt = 'La città soprannominata "la superba", in una parola, è'
    print(f'prompt: {prompt}')

    model_name = 'gpt-3.5-turbo'
    print(f'model: {model_name} => tokens: {num_tokens(prompt, model_name)}')

    model_name = 'text-davinci-003'
    print(f'model: {model_name} => tokens: {num_tokens(prompt, model_name)}')
