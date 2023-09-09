" Ensure python3 is available
if !has('python3')
  echohl ErrorMsg | echomsg "Error: Required vim compiled with +python3" | echohl None
  finish
endif

"
"~/.vim/
"└── pack/
"    └── my_plugin/
"        └── start/
"            └── my_plugin/
"                ├── plugin/
"                │   ├── llm_playground.vim
"                │   └── ...
"                └── python/
"                    ├── openai_setup.py
"                    ├── openai_completions.py
"                    └── ...
"
let s:python_path = expand('<sfile>:p:h:h') . '/python'

function! Info()
python3 << EOF
import vim
import sys
sys.path.append(vim.eval('s:python_path'))
from openai_setup import CHAT_COMPLETION_MODE
from vim_utils import echo, error
from utils import model_settings

echo(utils.help())
echo('\nModel:')

try:
    llm_provider = vim.eval('g:llm_provider')
    model_or_deployment = vim.eval('g:model_or_deployment')
    completion_mode = vim.eval('g:completion_mode')
    temperature = float(vim.eval('g:temperature'))
    max_tokens = int(vim.eval('g:max_tokens'))
    stop = vim.eval('g:stop')
except:
    error('prompter.vim setup not done! Run in command line :PrompterSetup')

echo(model_settings(llm_provider, model_or_deployment, completion_mode, temperature, max_tokens, stop))
EOF
endfunction


function! Setup()
python3 << EOF
import vim
import sys
sys.path.append(vim.eval('s:python_path'))
from openai_setup import setup, CHAT_COMPLETION_MODE
from vim_utils import info, error

# set completion highlight default colors,  
vim.command('let g:prompter_completion_ctermbg = 3')
vim.command('let g:prompter_completion_ctermfg = 0')

global_defaults = None

try:
    global_defaults = setup()
except Exception as e:
    error(e)

if global_defaults:
  vim.command(f'let g:llm_provider = "{global_defaults.llm_provider}"')
  vim.command(f'let g:completion_mode = "{global_defaults.completion_mode}"')
  vim.command(f'let g:temperature = "{global_defaults.temperature}"')
  vim.command(f'let g:max_tokens = "{global_defaults.max_tokens}"')
  vim.command(f'let g:stop = {global_defaults.stop}')

  if global_defaults.completion_mode == CHAT_COMPLETION_MODE:
      vim.command(f'let g:model_or_deployment = "{global_defaults.model_chat_completion}"')
      info_text = (
          f'Model: {global_defaults.llm_provider}/{global_defaults.model_chat_completion} '
          f'completion mode: {global_defaults.completion_mode} '
          f'temperature: {global_defaults.temperature} max_tokens: {global_defaults.max_tokens}'
      )
      if global_defaults.stop:
          info_text += f' stop: {global_defaults.stop}'
      info(info_text)
  else:
      vim.command(f'let g:model_or_deployment = "{global_defaults.model_text_completion}"')
      info_text = (
          f'Model: {global_defaults.llm_provider}/{global_defaults.model_text_completion} '
          f'completion mode: {global_defaults.completion_mode} '
          f'temperature: {global_defaults.temperature} max_tokens: {global_defaults.max_tokens}'
      )
      if global_defaults.stop:
          info_text += f' stop: {global_defaults.stop}'
      info(info_text)
EOF
endfunction


function! Completion()
python3 << EOF
import vim
import sys
sys.path.append(vim.eval('s:python_path'))
from utils import model_settings
from vim_utils import info, progress, error
import openai_completions

# take the current buffer as prompt
# the buffer is a list of separated strings
prompt = '\n'.join(vim.current.buffer[:])

# removes both the leading and trailing newlines along with any extra spaces.
prompt = prompt.strip()

try:
  llm_provider = vim.eval('g:llm_provider')
  model_or_deployment = vim.eval('g:model_or_deployment')
  completion_mode = vim.eval('g:completion_mode')
  temperature = float(vim.eval('g:temperature'))
  max_tokens = int(vim.eval('g:max_tokens'))
  stop = vim.eval('g:stop')
  settings_available = True
except:
    error('Run in command line :PrompterSetup')
    settings_available = False

# Awful conditional management, but caused by some vimscript/python limits (impossible to return/exit
if settings_available:

  #  show model settings as a work in progress message. 
  #  visible only if latency is greater than hundreds of millisecond 
  progress(model_settings(llm_provider, model_or_deployment, completion_mode, temperature, max_tokens, stop))

  completion_text, completion_statistics = openai_completions.complete(
      prompt,
      llm_provider,
      model_or_deployment,
      completion_mode,
      temperature,
      max_tokens,
      stop
  )

  # completion tokens are great than max_tokens 
  if 'length' in completion_statistics:
      error(completion_statistics)
  else:
      info(completion_statistics)

  # vim buffer requires a list of lines (no newlines)
  # completion_text = completion_text.strip().split('\n')
  # append the LLM completion to the current buffer, without an initial newline
  # vim.current.buffer.append(completion_text)

  # Replace the buffer content with the concatenated text without an initial newline
  current_buffer = '\n'.join(vim.current.buffer[:]) + completion_text
  vim.current.buffer[:] = current_buffer.split('\n')

  # highlight completion 
  vim.command('let g:last_completion_text = "' + completion_text.replace('"', '\\"') + '"')

  # highlight completion (multiline) text
  # https://vi.stackexchange.com/questions/43001/how-can-i-match-a-regexp-containing-newlines/43002#43002
  ctermbg = vim.eval('g:prompter_completion_ctermbg')
  ctermfg = vim.eval('g:prompter_completion_ctermfg')
  vim.command(f'highlight PrompterCompletion ctermbg={ctermbg} ctermfg={ctermfg}')
  vim.command("execute 'match PrompterCompletion /' . substitute(g:last_completion_text, \"[\\n\\<C-m>]\", '\\\\n', 'g') . '/' ")

  # show the end of completion (go to the end of the buffer)
  vim.command('$')
EOF
endfunction


"
" PLUGIN COMMANDS
"
command! PrompterSetup call Setup()
command! PrompterInfo call Info()
command! PrompterComplete call Completion()
