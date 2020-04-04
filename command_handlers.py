import random
import itertools

# Any command starting with $ will execute its corresponding function here.

# Simply return a test message.
def test(message):
    return 'Test'

# Take any number of arguments and return one of them randomly.
def lotto(message):
    if len(message.content.split()) < 2:
        return "I can't choose anything if you don't give me any options!"
    options = message.content.split()[1:]
    return random.choice(options)

# First argument specifies number of teams. Other arguments are player names.
# Players are then randomly divided over equally large teams.
def teams(message):
    try:
        num_teams = int(message.content.split()[1])
        if num_teams < 1:
            return 'You need at least one team.'

        options = message.content.split()[2:]

        if len(options) == 0:
            return "I can't make any teams if there are no people."
    except (ValueError, IndexError):
        return "Give me the number of teams you need and the names of the people you are with. I'll make you some teams."
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
