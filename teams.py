import discord
import random


team_list_dict = {}


class Team:

    def __init__(self, name):
        self.name = name
        self.users = []

    def __eq__(self, other):
        if isinstance(other, Team):
            return self.name == other.name
        return False

    def to_string(self):
        return self.name + ": " + ", ".join([u.name for u in self.users])


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# TODO: get team names from a user-defined list, requires persistence which idk how to do with discord
# Adds a number of teams, with increasing numbers
def add_random_teams(amount, guild):
    team_list = team_list_dict[guild]
    new_team_list = []
    team_nr = 0
    while amount > 0:
        team_nr = team_nr + 1
        team = Team("Team {}".format(team_nr))
        if team in team_list:
            continue
        team_list.append(team)
        new_team_list.append(team)
        amount = amount - 1
    return new_team_list


#  Adds a user from a guild into a team, removes the user from ay other teams they are in
def add_to_team(user, team, guild):
    team_list = team_list_dict[guild]
    for t in team_list:
        if user in t.users:
            t.users.remove(user)
    team.users.append(user)


#  Takes a list of users, and a list of teams (which are not necessarily in the guild!), and distributes those users
#  over every specified team that is actually in the guild
def distribute_over_teams(users, team_list, guild):
    guild_team_list = team_list_dict[guild]
    random.shuffle(users)
    while len(users) > 0:
        for team in random.shuffle(guild_team_list[:]):
            if team in team_list:
                add_to_team(users.pop(), team, guild)


#  returns a string that contains all teams of a guild, and the members of those teams
def print_teams(guild):
    return "\n\n".join([t.to_string() for t in team_list_dict[guild]])


#  sub-commands


#  removes all teams from the guild this message was sent in
def reset(message):
    team_list_dict[message.guild] = []
    return 'All teams have been removed!'


#  empties all teams from their members, in the guild this message was sent in
def empty(message):
    team_list = team_list_dict[message.guild]
    for team in team_list:
        team.users = []
    return 'All teams have been emptied!'


#  used to create a set of teams, in the guild this message was sent in
def create(message):
    content_list = message.content.split()
    new_team_list = []

    if is_int(content_list[2]):  # create {num_teams}
        new_team_list = add_random_teams(int(content_list[2]), message.guild)
    else:  # create {team name list}
        team_list = team_list_dict[message.guild]
        team_names = [n.strip() for n in " ".join(message.content.split()[2:]).split(",")]
        for team_name in team_names:
            team = Team(team_name)
            if team not in team_list:
                team_list.append(team)
                new_team_list.append(team)
        if not new_team_list:
            return "All of those teams already exist!" if len(team_names) > 1 else "That team already exists!"

    return "The following team" + ("s have" if len(new_team_list) > 1 else " has") + " been created:\n" + ", ".join([t.name for t in new_team_list])


#  used to divide the members of a voice channel into a set of teams
def divide(message):
    global errors
    team_list = team_list_dict[message.guild]
    content = message.content.split()

    if len(content) > 4:
        return errors['wrong_args']

    if len(content) == 2:  # divide
        users = message.author.voice.voice_channel.members
        if users is None:
            return errors['user_not_in_channel']

    elif is_int(content[2]):  # divide {num_teams}
        users = message.author.voice.voice_channel.members
        if users is None:
            return errors['user_not_in_channel']
        team_list = add_random_teams(int(content[3]), message.guild)

    else:  # divide {channel_name} || divide {channel_name} {num_teams}
        voice_channels = [channel for channel in message.guild.voice_channels if channel.name == content[2]]
        if not voice_channels:
            return errors['unknown_channel_name']
        users = voice_channels[0].members

        if len(content) > 3:  # divide {channel_name} {num_teams}
            num_teams = content[3]
            if not is_int(num_teams):
                return errors['wrong_args']
            num_teams = int(num_teams)
            team_list = add_random_teams(num_teams, message.guild)

    distribute_over_teams(users, team_list, message.guild)
    return "Done! This is the current team distribution:\n" + print_teams(message.guild)


#  adds the user that sent this message to a random existing team in the guild this message was sent in
def join_random(message):
    global errors
    team_list = team_list_dict[message.guild]
    if not team_list:
        return errors['no_teams']
    team = random.choice(team_list)
    add_to_team(message.author, team, message.guild)
    return message.author.name + ", you are now in: " + team.name


# adds the user to the team that is specified with the first argument, if that team exists in the guild this message
# was sent in
def join(message):
    global errors
    team_list = team_list_dict[message.guild]
    content = message.content.split()
    if len(content) < 3:
        return errors['wrong_args']
    team_name = content[2]
    team = [t for t in team_list if t.name == team_name]
    if not team:
        return errors['unknown_team']
    add_to_team(message.author, team[0], message.guild)
    return message.author.name + ", you are now in: " + team_name


#  removes the user from the team they are in, in the guild this message was sent in
def leave(message):
    global errors
    team_list = team_list_dict[message.guild]
    removed_list = []

    for t in team_list:
        if message.author in t.users:
            removed_list.append(t)
            t.users.remove(message.author)

    if not removed_list:
        return errors['not_in_team']

    return message.author + " has been removed from team" + ("s" if len(removed_list) > 1 else "") + ": " + ", ".join(
        [t.name for t in removed_list])


#  deletes a team with a specific name, in the guild this message was sent in
def delete(message):
    global errors

    content = message.content.split()
    if len(content < 3):
        return errors['wrong_args']
    team_list = team_list_dict[message.guild]

    for t in team_list[:]:
        if t.name == content[2]:
            team_list.remove(t)
            return "Deleted team: " + t.name

    return errors['unknown_team']


#  displays all teams that are in the guild this message was sent in
def all_teams(message):
    return "Existing teams:\n" + print_teams(message.guild)


#  displays a help message elaborating on the possible team commands
def print_commands(message):
    unique_commands = commands.keys()

    result = "Hey " + message.author.name + "! Here is an overview of the possible team commands, and their " \
                                            "explanation. [Arguments] in square brackets are mutually exclusive, " \
                                            "{arguments} in curly brackets are optional:\n\n "
    explanations = []

    for c in unique_commands:
        explanation = "$teams " + c + " " + command_help_messages.get(commands[c], "some idiot added this command "
                                                                                   "without making a help message for "
                                                                                   "it...")
        explanations.append(explanation)

    return result + "\n\n".join(explanations)


#  displays an error, called when the message has an invalid team command
def error(message):
    global type_help
    return "'" + message.content.split()[1] + "' is not a known teams command. "+type_help


#  the strings that need to be typed in order to execute a command, linked to the function that executes the command
#  values should be unique, keys should be lowercase
commands = {
    'all': all_teams,
    'reset': reset,
    'empty': empty,
    'delete': delete,
    'create': create,
    'divide': divide,
    'join_random': join_random,
    'join': join,
    'leave': leave,
    'help': print_commands
}


#  can be used to specify any aliases for commands. here, values need not be unique, keys should still be lowercase
command_aliases = {
    'vincent_likes_to_eat_feathers': reset
}


#  each function that executes a command, linked to a help message

#  note: full message is printed as:
#  '$teams {command name} {help message}'

#  {help message} should be:
#  {command arguments} :\n {command help message}\n
#  repeated(    {argument name}     :   {argument explanation})
command_help_messages = {
    all_teams: ":\n display all teams and their members",

    reset: ":\n deletes all existing teams",

    empty: ":\n empties all existing teams of their members",

    delete: "team_name :\n deletes a team with a specific name\n"
            "   team_name       :           name of the team to be deleted",

    create: "[N, team_name_list] :\n creates a set of teams\n"
            "   team_name_list  :   a comma separated list of team names. e.g.: team 1, team 2, team 3\n"
            "   N               :   the amount of teams the should be randomly created",

    divide: "{channel_name} {N} : \ndistributes the users in a voice channel over a set of teams\n"
            "   {channel_name} :    if provided, the set of users will be taken from the voice channel with this name\n"
            "                       if not provided, the set of users will be taken from the voice channel you are in\n"
            "   {N}            :    if provided, the set of teams will be N newly created teams\n"
            "                       if not provided, the set of teams will be all existing teams",

    join_random: ":\nputs you into a random existing team",

    join: "team_name :\nputs you into an existing team with a specific name\n"
          "   team_name     :       the name of the team you want to be put in",

    leave: ":\nremoves you from the team you are currently in",

    print_commands: ":\ndisplays this message",

}


#  error messages for easy access
type_help = "Type '$teams help' for more information."
errors = {
    'not_in_team': "You need to be in a team to use this command." + type_help,
    'no_teams': "This command requires the existence of at least one team." + type_help,
    'unknown_team': "The team you specified does not exist." + type_help,
    'user_not_in_channel': "Join a channel before using this command, or specify the channel name. " + type_help,
    'unknown_channel_name': "The channel with the name you provided does not exist. " + type_help,
    'wrong_args': "Those arguments don't match the given command. " + type_help
}


#  main command that is called by the Discord API
def teams(message):
    if message.guild not in team_list_dict:
        team_list_dict[message.guild] = []

    content = message.content.split()
    if len(content) < 2:
        return "$teams requires at least one additional command. "+type_help

    return commands.get(content[1].lower(), command_aliases.get(content[1].lower(), error))(message)
