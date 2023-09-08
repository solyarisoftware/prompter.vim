# prompter.vim
vim as a perfect large language models prompts playground

![alt text](screens/screenshot.1.png)

Transform the Vim editor into an efficient prompt engineering environment,
effectively replacing proprietary providers Large Language Models (LLMs) web playgrounds like:

- [Azure OpenAI Service Playground](https://oai.azure.com/portal/)
- [OpenAI Playground](https://platform.openai.com/playground)
- Other platforms planned for inclusion in future versions of this plugin.


## Goals

- **Instant LLM Completion**: 
  trigger LLM completions with a simple keystroke.
- **Prompt Interaction**:
  generate prompts directly in the editor and save them on the fly.
- **Run-time statistics**:
  measure completions in terms of latency, used tokens, speed, etc.
- **Focused Workflow**:
  maintain undivided focus within the editor, and seamlessly save all your work to local files.


## Backstory

The idea emerged as I was writing some LLM prompts, experimenting with some
prompt engineering techniques, using a simple "text completion" approach. 
You write your text prompt and then request a Large Language Model (LLM) completion. 

My initial approach was to utilize the web playgrounds offered by LLM providers.
However, I encountered numerous issues especially while interacting
with Azure OpenAI web playgrounds. For reasons I do not yet comprehend, the
web interaction on the Azure web playground slow down considerably after a
certain point.  I suspect a bug within the completion boxes. 
Furthermore, I am not fond of the Azure web interface for the "chat completion" mode. 
A total mess! Instead, the original OpenAI playground is better implemented, 
and I did not encounter the aforementioned issues.

Nevertheless, both web playgrounds permit only one prompt per browser tab.
Therefore, when dealing with multiple active prompts (developing a composite
application composed of nested/chained template prompts), you must maintain
multiple playgrounds open in distinct tabs.


When you achieve certain (intermediate) noteworthy outcomes, you must copy all text boxes and save them in versioned files.
Undertaking all of this with web playgrounds is a cumbersome and error-prone process.


## Install

This pluguin is made in Python3. Check if your vim installation support Python3 

```bash
vim --version | grep "+python3"
```

Install the plugin using your preferred plugin manager, e.g. using vim-plug, in your `.vimrc` file:
```viml
  Plug 'solyarisoftware/prompter.vim'
```
 
## Environment Setup 

### Openai Provider
```bash
# MANDATORY VARIABLES: 
# WARNING: KEEP YOU API KEY SECRETS.
export AZURE_OPENAI_API_KEY="YOUR OPENAI API KEY"

export OPENAI_COMPLETION_MODE="chat"

export OPENAI_MODEL_NAME_CHAT_COMPLETION="gpt-3.5-turbo"
export OPENAI_MODEL_TEXT_COMPLETION="text-davinci-003"

# OPTIONAL
# specify the LLM provider. Default is just "openai"
export LLM_PROVIDER="openai"

export OPENAI_TEMPERATURE=0.7
export OPENAI_MAX_TOKENS=100
export OPENAI_STOP=""
```

### Azure Openai Provider
```bash
# MANDATORY VARIABLES: 
# WARNING: KEEP YOU API KEY SECRETS.

# specify the LLM provider
export LLM_PROVIDER="azure"
export AZURE_OPENAI_API_VERSION="2023-05-15"

export AZURE_OPENAI_API_KEY="YOUR AZURE OPENAI API KEY"
export AZURE_OPENAI_API_ENDPOINT="YOUR AZURE OPENAI ENDPOINT"

export OPENAI_COMPLETION_MODE="chat"

export AZURE_DEPLOYMENT_NAME_CHAT_COMPLETION="gpt-35-turbo"
export AZURE_DEPLOYMENT_NAME_TEXT_COMPLETION="text-davinci-003"

export OPENAI_TEMPERATURE=0.7
export OPENAI_MAX_TOKENS=100
export OPENAI_STOP="a: u:"
```


## Commands

### `:PrompterSetup`
When you enter vim, to activate the Prompter playground environment, first of all run in command mode:
```viml
:PrompterSetup
```
Following the environment settings, if successful, the command print in the status line the model configurations:
```
chat completion model: azure/gpt-35-turbo (temperature: 0.7 max_tokens: 100)
```

### `:PrompterComplete`
Edit your prompt on a vim windows, and to run the LLM completion just  
```viml
:PrompterComplete
```
the status line report some statistics:
```
Latency: 1480ms (1.5s) Tokens: 228 (prompt: 167 completion: 61) Speed: 154 Words: 28 Chars: 176, Lines: 7
```

The statistics report these magnitudes:
- Latency: bot in milliseconds and second approximations
- Tokens: the total tokens amount, the prompt subtotal and the completion subtotal
- Speed: this is the Tokens / latency (in seconds) ratio, say the "speed"
- Words, the number of words generated in the completion
- Chars, the number of character in the completions
- Lines: the number of lines generated in the completion 

### `:Prompter`
Just reports:
- the current plugin version
- the current model attributes
- the list of plugin commands


## Keyboard shortcuts

💡Tip: You can use vim key map to assign a command to a key. Examples:

- Must to have (to run completion with a single keystroke): 
  **assign the command `:PrompterComplete` to the key `F12`:
  ```vim
  map <F12> :PrompterComplete<CR>
  ```

- Maybe useful:
  Add a new line beginning with `a: `, just pressing  the key `F9`:
  ```viml
  map <F9> :normal oa: <CR> 
  ```

- Maybe useful:
  Add a new line beginning with `u: `, just pressing  the key `F10`:
  ```viml
  map <F10> :normal ou: <CR> 
  ```

## Variables Settings

- get and set completion background and foreground colors:
  ```viml
  echo g:prompter_completion_ctermbg
  echo g:prompter_completion_ctermfg

  let g:prompter_completion_ctermbg = 3
  let g:prompter_completion_ctermfg = 0
  ```

- To modify the temperature value
  ```viml
  let g:temperature = 0.2
  ```

- To modify the max tokens value
  ```viml
  let g:max_tokens = 2000

- To modify the stop sequence(s) 
  ```viml
  let g:stop = ['a:', 'u:']
  ```


## Useful vim settings

- Enabling Soft Wrap
  ```viml
  :set wrap linebreak nolist
  ```

- mark placeholders
  ```viml
  syntax region CustomBraces start=/{/ end=/}/
  highlight link CustomBraces Statement
  au BufRead,BufNewFile *.{your-file-extension} set syntax=custom_braces
  ```

## Features to do

### Support template prompts
Things become interesting when you design "template prompts"
comprised of various parts that can be dynamically constructed at run-time.
Consider, for instance, that you wish to prototype a "template prompt"
containing placeholder variables, that are references to certain variables
filled by other prompts or files, like so:

```jinja2
TASK
{{some_task_description}}

DATA
{{some_yaml}}

DIALOG
{{dialog_history}}
```

In the example above, when using web playgrounds, you function as a copy-paste intermediary. 
You are required to open four web tabs, execute text completions in each, 
and finally manually paste completions, substituting variables such as {{some_data}}, {{dialog_history}}. 
Additionally, you might need to load a file into a variable, like {{some_yaml}}.

The idea is to support template prompts editing allowing to replace on the fly (with a keystroke) 
the variable placeholders, with the content of other buffers/windows.


### Use LiteLLM as a LLM provider abstraction layer

https://github.com/BerriAI/litellm is a lightweight package to simplify LLM API calls 
- Azure, OpenAI, Cohere, Anthropic, Replicate. Manages input/output translation.

So far prompter.vim support interface with Azure Openai or Openai native providers.
LiteLLM could be a better option to use openai APis.


## Similar projects

- https://github.com/madox2/vim-ai


## How to contribute

This project is work-in-progress proof-of-concept alfa version.
I'm not a vimscript expert, so any contribute or suggestion is welcome.

For any proposal and issue, please submit here on github issues for bugs, suggestions, etc.
You can also contact me via email (giorgio.robino@gmail.com).

**If you like the project, please ⭐️star this repository to show your support! 🙏**

## LICENSE

MIT License
```
Copyright (c) 2023 Giorgio Robino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

[top](#)
