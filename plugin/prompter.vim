" Ensure python3 is available
if !has('python3')
  echohl ErrorMsg | echomsg "Error: Required vim compiled with +python3" | echohl None
  finish
endif

" set default key mappings
" they will be activated by command PrompterSetup
let g:prompter_setup_keystroke = '<F9>'
let g:prompter_info_keystroke = '<F10>'
let g:prompter_generate_keystroke =  '<F12>'
let g:prompter_regenerate_keystroke =  '<F8>'

" immediate shortcut for PrompterSetup itself
execute 'map ' . g:prompter_setup_keystroke . ' :PrompterSetup<CR>'

" set completion highlight default colors,  
" orange = 3. green = 10
let g:prompter_completion_ctermbg = 3
let g:prompter_completion_ctermfg = 0

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
from utils import model_settings, help

echo(help())

try:
    llm_provider = vim.eval('g:llm_provider')
    model_or_deployment = vim.eval('g:model_or_deployment')
    completion_mode = vim.eval('g:completion_mode')
    temperature = float(vim.eval('g:temperature'))
    max_tokens = int(vim.eval('g:max_tokens'))
    stop = vim.eval('g:stop')
except:
    error('prompter.vim setup not done! Run in command line :PrompterSetup')

echo('\nModel:')
echo(
    model_settings(
        llm_provider,
        model_or_deployment,
        completion_mode,
        temperature,
        max_tokens,
        stop
    )
)

echo('\nCommands:')
echo('PrompterGenerate   ' + vim.eval('g:prompter_generate_keystroke'))
echo('PrompterRegenerate ' + vim.eval('g:prompter_regenerate_keystroke'))
echo('PrompterInfo       ' + vim.eval('g:prompter_info_keystroke'))
echo('PrompterSetup      ' + vim.eval('g:prompter_setup_keystroke'))

EOF
endfunction


function! Setup()
python3 << EOF
import vim
import sys
sys.path.append(vim.eval('s:python_path'))
from openai_setup import setup, CHAT_COMPLETION_MODE
from vim_utils import info, error

# set default key mappings
vim.command("execute 'map ' . g:prompter_generate_keystroke . ' :PrompterGenerate<CR>'")
vim.command("execute 'map ' . g:prompter_regenerate_keystroke . ' :PrompterRegenerate<CR>'")
vim.command("execute 'map ' . g:prompter_info_keystroke . ' :PrompterInfo<CR>'")
vim.command("execute 'map ' . g:prompter_setup_keystroke . ' :PrompterSetup<CR>'")

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


function! Generate()
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
    setting = model_settings(
        llm_provider,
        model_or_deployment,
        completion_mode,
        temperature,
        max_tokens,
        stop
    )
    progress(f'generating using: {setting}')

    completion_text, completion_statistics = openai_completions.generate(
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
    vim.command(f'highlight PrompterGenerateGroup ctermbg={ctermbg} ctermfg={ctermfg}')

    # highlighy just the last completion
    #vim.command("execute 'match PrompterGenerateGroup /' . substitute(g:last_completion_text, \"[\\n\\<C-m>]\", '\\\\n', 'g') . '/' ")

    # highlight all completions
    text_to_highlight = "substitute(g:last_completion_text, \"[\\n\\<C-m>]\", '\\\\n', 'g')"
    vim.command(f'let mid = matchadd(\"PrompterGenerateGroup\", {text_to_highlight})')

    # show the end of completion (go to the end of the buffer)
    vim.command('$')
EOF
endfunction


"
" PLUGIN COMMANDS
"
command! PrompterSetup call Setup()
command! PrompterInfo call Info()
command! PrompterGenerate call Generate()
command! PrompterRegenerate :execute 'normal u' | PrompterGenerate 
