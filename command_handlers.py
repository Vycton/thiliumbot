import random
import itertools

# Any command starting with $ will execute its corresponding function here.

# Simply return a test message.
def test(message):
    return 'Test'

# Take any number of arguments and return one of them randomly.
def lotto(message):
    options = message.content.split()[1:]
    return random.choice(options)

# First argument specifies number of teams. Other arguments are player names.
# Players are then randomly divided over equally large teams.
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
