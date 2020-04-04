import random

# Any command starting with $ will execute its corresponding function here

def test(message):
    return 'Test'

def lotto(message):
    options = message.content.split()[1:]
    return random.choice(options)
