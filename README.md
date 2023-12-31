# prompter.vim

Use vim as a tool for efficiently design and run, debug and save your Large Language Models (LLMs) prompts.

- Prompter.vim transforms the Vim editor into an efficient prompt engineering environment,
  effectively replacing LLM proprietary providers web playgrounds like:
  [Azure OpenAI Service Playground](https://oai.azure.com/portal/) or [OpenAI Playground](https://platform.openai.com/playground).

- From version 0.2, the plugin uses [LiteLLM](https://github.com/BerriAI/litellm) as a LLM provider abstraction layer.  
  LiteLLM calls all LLM APIs using the OpenAI format: 
  Bedrock, Azure, OpenAI, Cohere, Anthropic, Ollama, Sagemaker, HuggingFace, Replicate (100+ LLMs).
  So you can use prompter.vim with a vast list of different LLM providers!

## How it works 

1. Install and set your variable environment to configure model and settings
2. Press `<F9>` (key shortcut for `:PrompterSetup`) 
3. Edit your prompt
4. Press `<F12>`  (key shortcut for `:PrompterGenerate`) to get the LLM completion
5. Goto step 3 to maybe review your prompt
6. Save your prompt (and completions) into a snapshot text file (e.g. `myexperiment.prompt`)

| ![demo screenshot](screens/screenshot.3.png) |
|:--:|
| prompter.vim in action: editing/interacting with a prompt that simulate a phone conversation (with a technique below described as "dialogues as part of the text prompt")|

## ⚠ A Tool for Prompt Engineers, Not Coders!

Prompter.vim is not primarily designed as a code completion tool, although you can use it also for that purpose.   
Instead, this plugin aims to be a general-purpose replacement for web text completion playgrounds, 
intended for prompt engineers who want to test and debug natural language prompts.


## Features

- [x] **Use almost all available LLMs**  
  Using LiteLLM as a LLM abstraction layer, you can use a huge list of different LLM providers supported by LiteLLM.
- [x] **Instant LLM Completion**  
  trigger LLM completions with a simple keystroke.
- [x] **Run-time statistics**  
  Measure completions in terms of latency, used tokens, throughput, etc.
- [x] **Exploit all vim editor commodities (other plugins, etc.)**  
  Generate prompts inside the editor and seamlessly save all your work to local files.
- [x] **Completion Highlight**  
  Support basic completions color highlight

## Backstory

The idea emerged  in the Spring 2023 while I was writing LLM prompts 
and experimenting with prompt engineering techniques. 
I was using a straightforward "text completion" approach, 
where you input your text prompt corpus and request a completion from a Large Language Model (LLM).

My initial approach was to utilize the web playgrounds offered by LLM providers.
However, I encountered numerous issues especially while interacting
with [Azure OpenAI web playgrounds](https://oai.azure.com/portal/).

For reasons I do not yet comprehend, the web interaction on the Azure web playground slow down considerably
after a certain point. I suspect a bug within the completion boxes. 
Furthermore, I am not fond of the Azure web interface for the "chat completion" mode.
A total mess! Instead, the original [OpenAI playground](https://platform.openai.com/playground) is better implemented, 
and I did not encounter the aforementioned issues.

Nevertheless, both web playgrounds mentioned, permit only one prompt per browser tab.
Therefore, when dealing with multiple active prompts (developing a composite
application composed of nested/chained template prompts), 
you must maintain multiple playgrounds open in distinct tabs.
When you achieve certain (intermediate) noteworthy outcomes,
you must copy all text boxes and save them in versioned files.

Undertaking all of this with web playgrounds is a cumbersome and error-prone process.
The final thought was: what if I could run my completion directly inside my vim editor?


## 🙄 `text` or `chat` completion?
There are two common "completion modes" foreseen in OpenAI or similar current LLMs:

- **`text` completion**

  Completion mode set as `text` means that LLM completes,
  the given context window prompt text with a completion text (text in -> text out).
  An example of such a model setting is the `text-da-vinci-003` OpenAI model.
  To use a text completion mode, the model must support that mode through a specific API.
  ```
                    ┌────────────────────────┐
                ┌─  │                        │ ─┐
     context    │   │ bla bla bla            │  │
     window     │   │ bla bla                │  │
        =       │   │ bla bla bla bla        │  │ prompt
      prompt    │   │ bla                    │  │
        +       │   │ bla bla                │  │
    completion  │   │                        │ ─┘
                │   └────────────────────────┘
                │               |
                │         LLM generation
                │               |
                │               v
                │   ┌────────────────────────┐
                │   │                        │ ─┐
                │   │ bla bla                │  │ 
                │   │ bla bla bla            │  │ text completion
                │   │ bla                    │  │
                └─  │                        │ ─┘
                    └────────────────────────┘
  ```
  
- **`chat` completion**

  Completion mode set as `chat` means that LLM s fine-tuned for chat "roles" 
  (user say, assistant say, ...). 
  Fore details, please read [this](https://platform.openai.com/docs/guides/gpt/chat-completions-api).
  The context window prompt is in fact made by 
  - a "system prompt"  
  - a list of "user" and "assistant" messages.
  An example of such a model setting is the `gpt3.5-turbo` OpenAI model.
  To use a chat completion mode, the model must support that mode, trough specific API.
  ``` 
                    ┌────────────────────────┐
                ┌─  │ bla bla bla bla        │ ─┐
                │   │ bla bla bla            │  │
                │   │ bla bla                │  │ system
                │   │ bla bla bla bla        │  │ prompt
     context    │   │ bla                    │  │
     window     │   │ bla bla                │ ─┘
        =       │   └────────────────────────┘
  system prompt │   ┌────────────────────────┐
        +       │   │ user: blablabla        │ ─┐
      chat      │   ├────────────────────────┤  │
        +       │   │ assistant: bla bla bla │  │
    completion  │   ├────────────────────────┤  │ chat
                │   │ user: bla bla bla      │  │ prompt
                │   ├────────────────────────┤  │
                │   │ assistant: blabla bla  │  │
                │   ├────────────────────────┤  │
                │   │ user: blabla bla       │ ─┘
                │   └────────────────────────┘
                │               |
                │         LLM generation
                │               |
                │               v
                │   ┌────────────────────────┐
                │   │                        │ ─┐
                └─  │ assistant: bla bla bla │  │ chat completion
                    │                        │ ─┘
                    └────────────────────────┘
  ```

⚠️ Warning  
Prompter.vim plugin is conceived to work as text completer fast prototyping playground, 
avoiding the complications of the chat roles. 

So if a model that works only in *chat* mode (e.g. OpenAI `GPT3.5-Turbo`) is used, 
behind the scenes (through a LiteLLM `text_completion()` method) the editor text content (the prompt) 
is inserted as "system" role prompt. See also: 
[discussion](https://community.openai.com/t/achieving-text-completion-with-gpt-3-5-or-gpt-4-best-practices-using-azure-deployment/321503).

>
> I'm aware that using a chat-based model as a text-based model, as described above, 
> is not the optimal usage, but it's a compromise between the simplicity of 
> having a single text completion playground and the complexity of managing chat roles.
>

## 📦 Install

1. This plugin is made in Python3. 
   Check if your vim installation support Python3: 

   ```bash
   vim --version | grep "+python3" | awk '{print $3}'
   ```

   In my case I got `+python3`. That's the main prerequisite.

2. Check also which is the Python version which is compiled vim. 
   Extract the precise Python version with command: 

   ```bash
     vim --version | grep -o -P '(?<=/python)[0-9]+\.[0-9]+'
     ```

     In my case I got `3.8`. 

     > Note that vim can ONLY use the Python version (and related packages) wich is compiled.
     > By example if your system Python current version (`python3 --version` == `Python 3.11.6`)
     > differs from the vim python version, say `Python 3.8`, remember vim will see ONLY `Python 3.8` packages.
     > To use `Python 3.11.6` packages, you must recompile vim.

  3. Install Python package `litellm`.
     You must install `litellm` using `pip` of the corresponding Python version, e.g. `pip3.8`.

     ```bash
     pip3.8 install -U litellm 
     ```

  4. Install the plugin using your preferred plugin manager, 
     e.g. using vim-plug plug-in manager, insert in your `.vimrc` file:

     ```viml
     Plug 'solyarisoftware/prompter.vim'
     ```


  ## 🔑 Environment Variables Setup 

  ```bash
  # PROVIDER DEPENDENT SETTINGS USING LiteLLM CONFIGURATION 
  # https://docs.litellm.ai/docs/providers
  # https://docs.litellm.ai/docs/providers/azure

  # LLM PROVIDER MANDATORY SETTINGS
  export AZURE_API_VERSION=2023-09-01-preview
  export AZURE_API_BASE="https://XXXXXXXXXXXXXXX.openai.azure.com/"
  export AZURE_API_KEY="YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

  export MODEL="azure/your_deployment-name"

  # LLM PARAMETERS OPTIONAL SETTINGS
  # translated OpenAI model parameters 
  # https://docs.litellm.ai/docs/completion/input#translated-openai-params
  export TEMPERATURE=0.3
  export MAX_TOKENS=3000
  export OPENAI_STOP=""
  ```

  💡 A good idea is to edit and keep all variables above in a hidden file, 
  e.g. `vi ~/.prompter_azure.vim`, and execute it with `source ~/.prompter_azure.vim`


  ## 👊 Commands

  You can run commands in vim command mode (`:`) or the associated key:

  | Command              | Key 🚀 | Action                                    |
  |----------------------|--------|-------------------------------------------|
  | `:PrompterSetup`     | `<F9>` | Model setup and initial configurations    |
  | `:PrompterGenerate`  | `<F12>`| Run the LLM text completion               |
  | `:PrompterInfo`      | `<F10>`| Report current configuration              |

  ### `:PrompterSetup`

  When you enter vim, to activate the Prompter playground environment, first of all run in command mode:
  ```viml
  :PrompterSetup
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

  ### `:PrompterGenerate`

  Edit your prompt on a vim windows, and to run the LLM completion just  
  ```viml
  :PrompterGenerate
  ```
  The status line report some statistics:

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

  The statistics reports these metrics:

  | Metric     | Description                                                    | Example            |
  |------------|----------------------------------------------------------------|--------------------|
  | Latency    | Bot in milliseconds and second approximation                   | `1480ms (1.5s)`    |
  | Tokens     | Total tokens amount, prompt subtotal, and completion subtotal  | `228`              |
  | Throughput | Completion Tokens / latency ratio (in seconds). See discussion about the concept of throughput [here](https://github.com/BerriAI/litellm/issues/306)                | `154`              |
  | Words      | Number of words generated in the completion                    | `28`               |
  | Chars      | Number of characters in the completion                         | `176`              |
  | Lines      | Number of lines generated in the completion                    | `7`                |

> By default the command is assigned to the function key `F12`. 
> In such a way you can run the completion just pressing the single keystroke `F12`.


### `:PrompterInfo`

Reports the current plugin version, the list of plugin commands, the current model settings.

```viml
:PrompterInfo
```
the command print these info:
```
Version:
prompter.vim, by giorgio.robino@gmail.com, version 0.2 (November 28, 2023)

Model:
Model: azure/gpt-35-turbo completion mode: chat temperature: 0.5 max_tokens: 1500

Commands:
PrompterGenerate   <F12>
PrompterInfo       <F10>
PrompterSetup      <F9>
```

## 🛠 Variables Settings

- get and set completion background and foreground colors:
  ```viml
  echo g:prompter_completion_ctermbg
  echo g:prompter_completion_ctermfg

  let g:prompter_completion_ctermbg = 3
  let g:prompter_completion_ctermfg = 0
  ```

  > If you don't like the default highlight colors, 
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

- Commands are associated to function keys with this default setting:

  ```viml
  let g:prompter_setup_keystroke = '<F9>'
  let g:prompter_info_keystroke = '<F10>'
  let g:prompter_generate_keystroke =  '<F12>'
  let g:prompter_regenerate_keystroke =  '<F8>'
  ```

  Even if in vim you can assign a command to a key mapping of your preference, by example:
  `map <F2> :PrompterGenerate<CR>` and you can see what mapping for a particular key, 
  e.g. `F2`, you can use the vim command: `map <F12>`, the suggested way to proceed is to modify 
  one or more of the above mentioned variables and run `:PrompterSetup` again. 
  

## 🛠 Other useful vim settings

- Use (vim-included) spell checker

  When you write a LLM prompt it's very very important to avoid typos! 
  I many time experienced that LLM completion worst if you mistake just a verb.

  Things go even worst if you are writing prompts in more than one languages.
  Personally I usually write conversational prompts in English, for some reasons described in my article
  [Non-English Languages Prompt Engineering Trade-offs](https://convcomp.it/non-english-languages-prompt-engineering-trade-offs-7e529866faba),
  but the target language of the chat prompt is my native language: Italian. 
  All in all the prompt contains text in both English and Italian. In this case I run this small vimscript function:

  ```viml
  function! Spell() 
     set spelllang=en_us,it
     setlocal spell
     echom "Spell check set for Italian and English languages"
  endfunction  
  com! SPELL call Spell()
  ```

- Read all your previous completion statistics

  ```viml
  messages
  ```
  vim will show last completion statistics info. By example, if you just run 3 completions: 
  ```
  Latency: 961ms (1.0s) Tokens: 616 (prompt: 577 completion: 39) Throughput: 641 Words: 21 Chars: 134
  Latency: 368ms (0.4s) Tokens: 648 (prompt: 642 completion: 6) Throughput: 1761 Words: 2 Chars: 15
  Latency: 4227ms (4.2s) Tokens: 775 (prompt: 660 completion: 115) Throughput: 183 Words: 60 Chars: 377, Lines: 5
  ```

- Enabling lines soft wrap

  I usually work with a full-screen vim setting. That helps me to maximize my attention.
  Nevertheless having very long lines (after a `PrompterGenerate`) doesn't help the reading.  
  Unfortunately, in vim is not easy to configure a fixed column width soft wrap. 
  See [discussion](https://vi.stackexchange.com/questions/43028/how-to-soft-wrap-text-at-column-number-lower-than-window-width).
  You can set set soft warp with following command:
  ```viml
  set wrap linebreak nolist
  ```


## 💡 Dialogues as part of the text prompt

A technique I'm using to prototype dialog prompts, is to insert a dialog turns block 
as in the following example, where the dialog block terminates with the "stop sequence" (e.g. `a:`)
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

⚠ In the above case, to set the LLM stop waiting for user input, 
you could set the stop sequence as `u:` with command: 

  ```viml
let g:stop = ['u:']
```

💡 Please note if you do not set the stop sequence as described above,
the LLM will try to complete the entire conversation. 
This is in general not wanted because you want to write the sentence following `u:`.
Nevertheless it's sometime useful to unset the `g:stop` 
just to see how the LLM imagine the conversation flow. 

Other vim commands that could be useful:

- Add a new line beginning with `u: `, just pressing  the key `F6`:
  ```viml
  map <F6> :normal ou: <CR> 
  ```
- Add a new line beginning with `a: `, just pressing  the key `F7`:
  ```viml
  map <F7> :normal oa: <CR> 
  ```

## Dev/Test Environment

- [x] Vim version: VIM - Vi IMproved 9.0
- [x] I developed on WLS (Window Linux Subsystem) on a Windows 10 operating system, using an Ubuntu 20.04 distribution.
- [x] I tested the plugin using (vim compiled for) Python 3.8.10
- [x] As LLM provider, I tested only my Azure OpenAI account (through LiteLLM library).
- [ ] I didn't tested using an OpenAI account or other LLMs.


## Change log
- Version 0.1  
  First release. Only OpenAI/Azure OpenAI models are supported via OpenAI version 0.28 Python module.

- Version 0.2  
  LLMs completions are done through LiteLLM, LLMs abstraction layer python package, 
  allowing to use a multitude of different LLM providers. 

## Features to do in future releases

- [ ] **Support all LLM input parameters**  
  So far prompter.vim support only `temperature`, `max_tokens`, `stop` arguments.  
  LiteLLM accepts and translates the [OpenAI Chat Completion params](https://docs.litellm.ai/docs/completion/input#common-params) across all providers. 
  
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

- [ ] **Asynchronous LLM completion**  
  Currently, the  LLM completion command `PrompterGenerate` is a synchronous command: 
  the editor is blocked until the LLM API returns a completion text. 
  It could be tedious for very complex and long prompts that require many many seconds to complete (e.g. >> 10).
  In this cases it could be better if the command could be asynchrous, allowing the developer to use the vim editor
  with the completion is on-going.

- [ ] **Streaming support**  
  So far streaming completion is not take in consideration. 


## Known issues

- in command Promptergenerate, some characters (to be defined) broke the highlight matchadd regexp. 
  This imply that highlight doesn't work and/or a runtime error is generated. 
  Nevertheless the generation is done. To be investigated.


## Similar projects

- [vim-ai](https://github.com/madox2/vim-ai)
  Very similar to prompter.vim, nevertheless it's focused on code completion allowing small prompts from the command line.
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
  encountered when developing this plugin.

 - [LiteLLM creators](https://github.com/BerriAI/litellm) for having integrated some [suggested features](https://github.com/BerriAI/litellm/issues?q=solyarisoftware), as the [Text Completion Format](https://docs.litellm.ai/docs/tutorials/text_completion)!


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
