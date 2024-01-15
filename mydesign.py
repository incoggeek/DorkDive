
# ANSI escape codes for text colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLACK = '\033[30m'
WHITE = '\033[97m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Reset to default color

# ANSI escape codes for text styles
BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
STRIKETHROUGH = '\033[9m'


def color_style_text(color, text, style=''):
    print((color + style + text + RESET))

def red_text(text):
    print((RED + text  + RESET))

def green_text(text):
    print((GREEN + text  + RESET))

def yellow_text(text):
    print(YELLOW + text  + RESET)

def cyan_text(text):
    print(CYAN + text  + RESET)