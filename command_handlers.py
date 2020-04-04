import random
import itertools

# Any command starting with $ will execute its corresponding function here

def test(message):
    return 'Test'

def lotto(message):
    options = message.content.split()[1:]
    return random.choice(options)

def teams(message):
    num_teams = int(message.content.split()[1])
    options = message.content.split()[2:]
    random.shuffle(options)

    teams = [[] for _ in range(num_teams)]
    it = itertools.cycle(range(num_teams))

    for name in options:
        teams[next(it)].append(name)

    random.shuffle(teams)

    response = ''

    for idx in range(num_teams):
        response += 'Team {}: '.format(idx+1) + ', '.join(teams[idx]) + '\n'

    return response
