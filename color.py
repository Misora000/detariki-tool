c_red = '\x1b[31;20m'
c_yellow = '\x1b[33;20m'
c_blue = '\x1b[34;20m'
c_green = '\x1b[32;20m'
c_grey = '\x1b[38;20m'
c_bold_red = '\x1b[31;1m'
c_reset = '\x1b[0m'

def red(msg) -> str:
    return f'{c_red}{msg}{c_reset}'

def yellow(msg) -> str:
    return f'{c_yellow}{msg}{c_reset}'

def green(msg) -> str:
    return f'{c_green}{msg}{c_reset}'

def blue(msg) -> str:
    return f'{c_blue}{msg}{c_reset}'