"""
:function: printColor module
:synopsis: processes HTTP access and error logs into MySQL or MariaDB for logFiles2MySQL application.
:author: Will Raymond <farmfreshsoftware@gmail.com>
"""
# Terminal color definitions - 02/06/2025
# Loops to display colors - 03/24/2025
class color:
  END = '\033[0m'
  class fg:
    # Regular Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    # High Intensty
    REDI = '\033[91m'
    GREENI = '\033[92m'
    YELLOWI = '\033[93m'
    BLUEI = '\033[94m'
    PURPLEI = '\033[95m'
    CYANI = '\033[96m'
    WHITEI = '\033[97m'
  class bg:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
  class style:
    NORMAL = '\033[22m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    NEGATIVE = '\033[7m'
    CROSSED = '\033[9m'

if __name__ == '__main__':
    print('\n', '*** -- Normal --', '*** -- Bright --', '*** -- Dim --', '*** -- Italic --', '*** -- Underline --', '*** -- Blink --', '*** -- Negative --', '*** -- Crossed --')
    for i in dir(color.fg):
        if i[0:1] != '_':
            print('{:>10} {}'.format(i, getattr(color.fg, i) + color.style.NORMAL + i + color.END), 
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.BRIGHT + i + color.END), 
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.DIM + i + color.END), 
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.ITALIC + i + color.END),    
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.UNDERLINE + i + color.END), 
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.BLINK + i + color.END), 
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.NEGATIVE + i + color.END), 
                  '{:>10} {}'.format(i, getattr(color.fg, i) + color.style.CROSSED + i + color.END))    
    print('\n', 'Background Colors')
    for i in dir(color.bg):
        if i[0:1] != '_':
            print('{:>16} {}'.format(i, getattr(color.bg, i) + i + color.END))