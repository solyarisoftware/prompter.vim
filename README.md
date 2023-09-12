# prompter.vim

Use vim as a tool for efficiently design, debug and save your LLMs prompts.

Transform the Vim editor into an efficient prompt engineering environment,
effectively replacing proprietary providers Large Language Models (LLMs) web playgrounds like:

- [Azure OpenAI Service Playground](https://oai.azure.com/portal/)
- [OpenAI Playground](https://platform.openai.com/playground)
- Other platforms planned for inclusion in future versions of this plugin.

> ⚠ prompter.vim is not primarily designed as a code completion tool, 
> although you can use it for that purpose. 
> Instead, this plugin aims to be a general-purpose replacement for web text completion playgrounds, 
> intended for prompt engineers who want to test and debug natural language prompts.

## Usage 

1. Install and set your variable environment to configure model and settings
2. Press `<F9>` (`:PrompterSetup`) 
3. Edit your prompt
4. Press `<F12>`  (`:Promptergenerate`) to get the LLM completion
5. Goto step 3 to adjust your prompt
6. Save your prompt (and completions) into a snapshot file

![alt text](screens/screenshot.1.png)


## Features

- **Instant LLM Completion**: 
  trigger LLM completions with a simple keystroke.
- **Prompt Interaction**:
  generate prompts directly in the editor and save them on the fly.
- **Run-time statistics**:
  measure completions in terms of latency, used tokens, throughput, etc.
- **Focused Workflow**:
  maintain undivided focus within the editor, and seamlessly save all your work to local files.
- **Completion Highlight**:
  support last completion color highlight.


## Backstory

The idea emerged as I was writing LLM prompts, experimenting with some
prompt engineering techniques, using a simple "text completion" approach where 
you write your text prompt corpus and then request a Large Language Model (LLM) completion. 

My initial approach was to utilize the web playgrounds offered by LLM providers.
However, I encountered numerous issues especially while interacting
with Azure OpenAI web playgrounds.

For reasons I do not yet comprehend, 
the web interaction on the Azure web playground slow down considerably after a
certain point.I suspect a bug within the completion boxes. 
Furthermore, I am not fond of the Azure web interface for the "chat completion" mode.
A total mess! Instead, the original OpenAI playground is better implemented, 
and I did not encounter the aforementioned issues.

Nevertheless, both web playgrounds permit only one prompt per browser tab.
Therefore, when dealing with multiple active prompts (developing a composite
application composed of nested/chained template prompts), 
you must maintain multiple playgrounds open in distinct tabs.
When you achieve certain (intermediate) noteworthy outcomes,
you must copy all text boxes and save them in versioned files.

Undertaking all of this with web playgrounds is a cumbersome and error-prone process.
The final thought was: what if I could run my completion directly inside mt vim editor?


## `text` completion or `chat` completion?
There are two common "completion modes" foreseen in OpenAI or similar current LLMs:

- **`text` completion**

  Completion mode set as `text` means that LLM completes,
  the given context window prompt text with a completion text (text in -> text out).
  An example of such a model setting is the `text-da-vinci-003` OpenAI model.
  To use a text completion mode, the model must support that mode through a specific API.
  
- **`chat` completion**

  Completion mode set as `chat` means that LLM s fine-tuned for chat "roles" 
  (user say, assistant say, ...). 
  Fore details, please read [this](https://platform.openai.com/docs/guides/gpt/chat-completions-api).
  The context window prompt is in fact made by 
  - a "system prompt" and 
  - a list of "user" and "assistant" messages.
  An example of such a model setting is the `gpt3.5-turbo` OpenAI model.
  To use a chat completion mode, the model must support that mode, trough specific API.

> ⚠️ Prompter.vim plugin is conceived to work as text completer fast prototyping playground, 
> avoiding the complications of the chat roles. 
> So a model that works only in chat mode (as the `gpt3.5-turbo`) is behind the scenes "simulates" 
> to be a text completion model, just inserting the prompt text you are editing, as "system" role prompt.
> See also this 
> [discussion](https://community.openai.com/t/achieving-text-completion-with-gpt-3-5-or-gpt-4-best-practices-using-azure-deployment/321503).
> I'm aware that using a chat-based model as a text-based model, as described above, 
> is not the optimal usage, but it's a compromise between the simplicity of 
> having a single text completion playground and the complexity of managing chat roles.


## 📦 Install

This pluguin is made in Python3. Check if your vim installation support Python3 

```bash
vim --version | grep "+python3"
```

Install the plugin using your preferred plugin manager, e.g. using vim-plug plug-in manager, 
insert in your `.vimrc` file:
```viml
Plug 'solyarisoftware/prompter.vim'
```


## 🔑 Environment Variables Setup 

### OpenAI Provider
In the example here below, you set the secret API key, the completion mode as `chat` and you specify the model to be used

```bash
# MANDATORY SETTINGS: 
# WARNING: KEEP YOU API KEY SECRETS.
export AZURE_OPENAI_API_KEY="YOUR OPENAI API KEY"

export OPENAI_COMPLETION_MODE="chat"
export OPENAI_MODEL_NAME_CHAT_COMPLETION="gpt-3.5-turbo"

# export OPENAI_COMPLETION_MODE="text"
# export OPENAI_MODEL_TEXT_COMPLETION="text-davinci-003"

# OPTIONAL SETTINGS
export LLM_PROVIDER="openai"

export OPENAI_TEMPERATURE=0.7
export OPENAI_MAX_TOKENS=100
export OPENAI_STOP=""
```

### Azure OpenAI Provider
In the example here below, you set the secret API key, the completion mode as `chat` and you specify the model to be used.

```bash
# MANDATORY VARIABLES: 
# WARNING: KEEP YOU API KEY SECRETS.

export LLM_PROVIDER="azure"
export AZURE_OPENAI_API_VERSION="2023-05-15"

export AZURE_OPENAI_API_KEY="YOUR AZURE OPENAI API KEY"
export AZURE_OPENAI_API_ENDPOINT="YOUR AZURE OPENAI ENDPOINT"

export OPENAI_COMPLETION_MODE="chat"
export AZURE_DEPLOYMENT_NAME_CHAT_COMPLETION="gpt-35-turbo"

# export OPENAI_COMPLETION_MODE="text"
# export AZURE_DEPLOYMENT_NAME_TEXT_COMPLETION="text-davinci-003"

# OPTIONAL SETTINGS
export OPENAI_TEMPERATURE=0.5
export OPENAI_MAX_TOKENS=1000
export OPENAI_STOP="a:"
```

> 💡 A good idea is to edit and keep all variables above in a hidden file, e.g. `vi ~/.prompter.vim`,
> and execute it with `source ~/.prompter.vim`


## 👊 Commands
In vim command mode (:) these commands are available:

### `PrompterSetup`

When you enter vim, to activate the Prompter playground environment, first of all run in command mode:
```viml
PrompterSetup
```
Following the environment settings, if successful, the command print in the status line the model configurations:
```
Model: azure/gpt-35-turbo completion mode: chat temperature: 0.7 max_tokens: 100
```
Explanation of values in the status line report:
```
                               temperature preset value ───────────────────────────┐
                                                                                   │
                                max_tokens preset value ──────────┐                │
                                                                  │                │
      ┌─────┐ ┌────────────┐                 ┌────┐             ┌─┴─┐            ┌─┴─┐
Model:│azure│/│gpt-35-turbo│ completion mode:│chat│ temperature:│0.7│ max_tokens:│100│
      └──┬──┘ └─────┬──────┘                 └──┬─┘             └───┘            └───┘
         │          │                           │
         │          │                           └─ chat or text, depending on the model
         │          │
         │          └── name of the Azure deployment
         │
         └───────────── name of the LLM provider
```

### `PrompterGenerate`

Edit your prompt on a vim windows, and to run the LLM completion just  
```viml
PrompterGenerate
```
the status line report some statistics:
```
Latency: 1480ms (1.5s) Tokens: 228 (prompt: 167 completion: 61) Throughput: 154 Words: 28 Chars: 176, Lines: 7
```
Explanation of values in the status line report:
```
          ┌─ latency in milliseconds and seconds
          │
          │                     ┌───────────────────────────────── total nr. of tokens
          │                     │
          │                     │            ┌──────────────────── nr. of tokens in prompt
          │                     │            │
          │                     │            │               ┌──── nr. of tokens in completion
          │                     │            │               │
        ┌─┴───────────┐       ┌─┴─┐        ┌─┴─┐           ┌─┴┐             ┌───┐      ┌──┐      ┌───┐       ┌─┐
Latency:│1480ms (1.5s)│Tokens:│228│(prompt:│167│completion:│61│) Throughput:│154│Words:│28│Chars:│176│ Lines:│7│
        └─────────────┘       └───┘        └───┘           └──┘             └─┬─┘      └─┬┘      └─┬─┘       └┬┘
                                                                              │          │         │          │
                                                                              │          │         │          │
                                      Latency / Tokens ───────────────────────┘          │         │          │
                                                                                         │         │          │
                                                                 nr. of words ───────────┘         │          │
                                                                                                   │          │
                                                            nr. of characters ─────────────────────┘          │
                                                                                                              │
                                                                 nr. of lines ────────────────────────────────┘
```

The statistics reports these variables:
- **Latency**: bot in milliseconds and second approximations
- **Tokens**: the total tokens amount, the prompt subtotal and the completion subtotal
- **Throughput**: this is the completion Tokens / latency ratio (in seconds)
- **Words**, the number of words generated in the completion
- **Chars**, the number of character in the completions
- **Lines**: the number of lines generated in the completion 

> 🚀 By default the command is assigned to the function key `F12`. 
> In such a way you can run the completion just pressing the single keystroke `F12`.


### `PrompterInfo`

Reports the current plugin version, the list of plugin commands, the current model settings.


## 🛠 Variables Settings

- get and set completion background and foreground colors:
  ```viml
  echo g:prompter_completion_ctermbg
  echo g:prompter_completion_ctermfg

  let g:prompter_completion_ctermbg = 3
  let g:prompter_completion_ctermfg = 0
  ```

  > 💡 If you don't like the default highlight colors, 
  > you can replace `ctermbg` and `ctermfg` values using a subset of cterm/xterm 256 colors.
  > To show all colors available you can use the command `:HighlightColors` part of my plugin: 
  > [Highlight](https://github.com/solyarisoftware/Highlight.vim).

- To modify the temperature value
  ```viml
  let g:temperature = 0.2
  ```

- To modify the max tokens value
  ```viml
  let g:max_tokens = 2000

- To modify the stop sequence(s) 
  ```viml
  let g:stop = ['x:', 'y:', 'z:']
  ```


## 🛠 Other useful vim settings

- To read all statistics print of your completions:
  ```viml
  messages
  ```
  vim will show last completion statistics info. By example, if you just run 3 completions: 
  ```
  Model: azure/gpt-35-turbo completion mode: chat temperature: 0.5 max_tokens: 1500 stop: u:
  Latency: 961ms (1.0s) Tokens: 616 (prompt: 577 completion: 39) Throughput: 641 Words: 21 Chars: 134
  Model: azure/gpt-35-turbo completion mode: chat temperature: 0.5 max_tokens: 1500 stop: u:
  Latency: 368ms (0.4s) Tokens: 648 (prompt: 642 completion: 6) Throughput: 1761 Words: 2 Chars: 15
  Model: azure/gpt-35-turbo completion mode: chat temperature: 0.5 max_tokens: 1500 stop: u:
  Latency: 4227ms (4.2s) Tokens: 775 (prompt: 660 completion: 115) Throughput: 183 Words: 60 Chars: 377, Lines: 5
  ```

- Enabling Soft Wrap
  ```viml
  set wrap linebreak nolist
  ```

- How to see what mapping for a particular key, e.g. `F12`:
  ```viml
    map <F12>
  ```

- You can assign the commands like `:PrompterGenerate` to any key mappings of your preference, by example:
  ```vim
  map <F2> :PrompterGenerate<CR>
  ```

- mark placeholders
  ```viml
  syntax region CustomBraces start=/{/ end=/}/
  highlight link CustomBraces Statement
  au BufRead,BufNewFile *.{your-file-extension} set syntax=custom_braces
  ```


## 💡 Dialogues as part of the text prompt

A technique I'm using to prototype dialog prompts, is to insert a dialog turns block 
as in the follwing example, where the dialog block terminates with the "stop sequence" (e.g. `a:`)
triggering LLM to complete the assistant role:

```
TASK
You (a:) are a customer care assistant and you are assisting a user (u:).
...
...

DIALOG
a: Hello! How can I assist you today?
u: I want to open a report.
a: Fantastic! First, could you provide me with a detailed description of the issue you're experiencing?
u: The computer monitor won't turn on.
a: Thank you for the description. What is the name or model of the product or system you're having trouble with?
u: I can't read the brand. It's the company's PC monitor.
a: Thank you for the information. What is your preferred method of contact?
u: via email at g.angelotti@gmail.com
a: Thank you. Please confirm the provided email address: g.angelotti@gmail.com
u: that's correct!
a:
```

In the above case, to set the LLM stop waiting for user input, 
you could set the stop sequence as `u:` with command: 

```viml
let g:stop = ['u:']
```

These vim comands could be useful:

- Add a new line beginning with `u: `, just pressing  the key `F9`:
  ```viml
  map <F9> :normal ou: <CR> 
  ```
- Add a new line beginning with `a: `, just pressing  the key `F10`:
  ```viml
  map <F10> :normal oa: <CR> 
  ```


## Features to do in future releases

- [ ] **Support template prompts**

  You are designing "template prompts"
  comprised of various parts that can be dynamically constructed at run-time.
  Consider, for instance, that you wish to prototype a "template prompt"
  containing placeholder variables, that are references to certain variables
  filled by other prompts or files, like so:

  ```
  TASK
  {some_task_description}

  DATA
  {some_yaml}

  DIALOG
  {dialog_history}
  ```

  In the example above, when using web playgrounds, you function as a copy-paste intermediary. 
  You are required to open four web tabs, execute text completions in each, 
  and finally manually paste completions, substituting variables such as `{some_data}`, `{dialog_history}`. 
  Additionally, you might need to load a file into a variable, like `{some_yaml}`.

  The idea is to support template prompts editing allowing to replace on the fly (with a keystroke) 
  the variable placeholders, with the content of other buffers/windows.

- [ ] **Use LiteLLM as a LLM provider abstraction layer**

  So far prompter.vim support interface with Azure OpenAI or OpenAI native providers.

  [LiteLLM](https://github.com/BerriAI/litellm) could be a better option to use openai API directly.
  It is a lightweight package to simplify LLM API calls with Azure, OpenAI, Cohere, Anthropic, etc.


- [ ] **Improve highligt colorizing**

  So far just the last completion is colorized.
  The highlight  could forsee all completions or it could be avoided optionally.

- [ ] **Streaming support**

  So far streaming completion is not take in consideration. 


## 🙄 Similar projects

- [vim-ai](https://github.com/madox2/vim-ai)
  Very similar to prompter.vim. Nevertheless it's focused on code completion allowing small prompts from the command line.
- [llm.nvim](https://github.com/gsuuon/llm.nvim) 
  Just for neovim. Pretty similar to prompter.vim in the concept, but more oriented to code completions 
- [llm.nvim](https://github.com/huggingface/llm.nvim)
  just for neovim. It works with huggingface inference APis. 
- [copilot.vim](https://github.com/github/copilot.vim)
  Neovim plugin for GitHub Copilot


## 👏 Acknowledgements

- [David Shapiro](https://github.com/daveshap) for his huge dissemination work on LLMs and generative AI. 
  I have followed with enthusiasm especially his LLM prompt engineering live coding [youtube videos](https://www.youtube.com/@4IR.David.Shapiro)! 

- [Vivian De Smedt](https://vi.stackexchange.com/users/23502/vivian-de-smedt) 
  vim expert for his help solving an [issue](https://vi.stackexchange.com/questions/43001/how-can-i-match-a-regexp-containing-newlines/43002#43002)
  encountered when devloping this plugin.

## 🙏 Status / How to contribute

This project is work-in-progress proof-of-concept alfa version!

I'm not a vimscript expert, so any contribute or suggestion is welcome.
For any proposal and issue, please submit here on github issues for bugs, suggestions, etc.
You can also contact me via email (giorgio.robino@gmail.com).

**IF YOU LIKE THE PROJECT, PLEASE ⭐️STAR THIS REPOSITORY TO SHOW YOUR SUPPORT!**


## MIT LICENSE
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
