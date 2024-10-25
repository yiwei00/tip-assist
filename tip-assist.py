# constants
SCRIPT_NAME = 'tip-assist'
EXIT_COMMANDS = set(['quit', 'exit'])



# main
if __name__ == '__main__':
    quit = False
    while not quit:
        # read stdin
        raw_input = input(f'{SCRIPT_NAME}> ')
        # process raw stdin
        tokenized_input = raw_input.strip().split()
        if len(tokenized_input) <= 0:
            continue
        # extract and process commands
        command = tokenized_input[0]
        if command in EXIT_COMMANDS:
            quit = True
            continue