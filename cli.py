from threading import Thread

def docli(cli):
    if cli == '':
        return []

    args = cli.split()

    updates = []
    if args[0] == 'add':
        idx = 0
        if len(args) != 3:
            print('usage: add idx atom')
            return
        idx = int(args[1])
        a = args[2]
        if a not in ['+']:
            a = int(a)-1
        updates.append({'addAtom': [a, idx]})
    elif args[0] == 'convert':
        if len(args) != 3:
            print('usage: convert idx atom')
            return
        idx = int(args[1])
        a = args[2]
        if a not in ['+']:
            a = int(a)-1
        updates.append({'convertTo': [idx, a]})
    elif args[0] == 'delete':
        if len(args) != 2:
            print('usage: delete idx')
        idx = int(args[1])
        updates.append({'delete': [idx]})
    elif args[0] == 'merge':
        if len(args) != 1:
            print('usage: merge')
        updates.append({'checkMerge': []})
    elif args[0] == 'exit':
        raise Exception()

    return updates

def startcli(game):
    game.cli = ''
    def get_user_cli_input():
        print('waiting debug input...')
        while True:
            game.cli = input()
    t = Thread(target=get_user_cli_input)
    t.daemon = True
    t.start()
