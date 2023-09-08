# python utility functions that use the vim module
import vim


def info(text):
    ''' print a single line and redraw
        This technique can be particularly useful when you want to display dynamic progress or status updates
        without creating new lines in the command-line area.
    '''
    vim.command(f'echo "{text}"')


def progress(text):
    ''' print a single line and redraw
        This technique can be particularly useful when you want to display dynamic progress or status updates
        without creating new lines in the command-line area.
    '''
    vim.command(f'echo "{text}" | redraw')


def error(text):
    # vim.command('echohl ErrorMsg | echomsg "' + text + '" | echohl None')
    vim.command(f'echohl ErrorMsg | echomsg "{text}" | echohl None')
