import click as click
from database.database import Database
from rooms import rooms_service
from users import users_service
from users.user_model import User

db = Database()


def user(obj, login, password):
    cursor = obj['db'].cursor
    user = users_service.login(cursor, login, password)
    if user is None:
        print("Wrong credentials!")
        exit(1)
    obj['user'] = user
    obj['db'] = db


@click.group()
@click.pass_context
def run_command(ctx):
    ctx.obj = {
        'db': db,
        'user': user
    }


@run_command.group('user')
def user_command():
    pass


@user_command.command('register')
@click.option("--login", required=True, prompt=True)
@click.password_option()
@click.pass_obj
def registerNewUser(obj, login, password):
    if users_service.ifUserExists(obj['db'], login):
        print("This name is taken")
        exit()
    users_service.insertIntoUsers(obj['db'], login, password)


@user_command.command("login")
@click.option("--login", required=True, prompt=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def login(obj, login, password):
    user = users_service.login(obj['db'], login, password)
    print("Logged as")
    print(user.login)
    obj['user'] = user
    obj['db'] = db


@user_command.group("login")
@click.option("--login", required=True, prompt=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def login_command(obj, login, password):
    user(obj, login, password)


@login_command.command("list")
@click.pass_obj
@click.option("--filter", required=False)
def listAllUsers(obj, filter):
    for user in users_service.getAllUsers(obj['db']):
        if filter is None:
            print(user.login)
        elif user.login.find(filter) > -1:
            print(user.login)


@user_command.command("delete")
@click.pass_obj
@click.option("--login", required=True, prompt=True)
def remove_command(obj, login):
    users_service.deleteUser(obj['db'], login)


@run_command.group('room')
@click.option("--login", required=True, prompt=True)
@click.password_option(confirmation_prompt=False)
@click.pass_obj
def rooms_command(obj, login, password):
    user(obj, login, password)


@rooms_command.command('create')
@click.password_option("--room-password", confirmation_prompt=True)
@click.pass_obj
def create_command(obj, room_password):
    rooms_service.insertIntoRooms(obj['db'].cursor, obj['user'].id, room_password)


@rooms_command.command("delete")
@click.option("--room-id", required=True, prompt=True, type=click.types.INT)
@click.pass_obj
def deleteRoom(obj, room_id):
    cursor = obj['db'].cursor
    # room = rooms_service.findRoomById(cursor, id)
    # if room is None:
    #     print("Wrong room id!")
    #     exit(1)
    # if room.owner_id != obj['user'].id:
    #     print("Wrong room id!")
    #     exit(1)
    rooms_service.deleteRoomById(cursor, id)


@rooms_command.command("join")
@click.option("--room-id", required=True, prompt=True, type=click.types.INT)
@click.password_option("--room-password", confirmation_prompt=False)
@click.pass_obj
def joinRoomCommand(obj, room_id, room_password):
    if not rooms_service.joinRoom(obj['db'].cursor, obj['user'].id, room_id, room_password):
        print("Wrong room id or passowrd!")
        exit(1)


@rooms_command.command("set-topic")
@click.option("--room-id", required=True, prompt=True, type=click.types.INT)
@click.option("--new-topic", required=True, prompt=True)
@click.pass_obj
def setTopicCommand(obj, room_id, new_topic):
    cursor = obj['db'].cursor
    room = rooms_service.findRoomById(cursor, room_id)
    if room is None:
        print("Unknown room!")
        exit(1)
    if room.owner_id != obj['user'].id:
        print("Unknown room!")
        exit(1)
    # topic = rooms_service.get_topic(cursor, room_id)
    # if topic is not None:
    rooms_service.createTopic(cursor, room_id, new_topic)


@rooms_command.command("vote")
@click.option("--topic-id", required=True, prompt=True, type=click.types.INT)
@click.option("--value", required=True, prompt=True, type=click.types.FLOAT)
@click.pass_obj
def vote_command(obj, topic_id, value):
    cursor = obj['db'].cursor
    # topic = rooms_service.get_topic_by_id(cursor, topic_id)
    # if topic is None:
    #     print("Wrong topic!")
    #     exit(1)
    #
    # if not rooms_service.joined_room(cursor, obj['user'].id, topic.room_id):
    #     print("Wrong topic!")
    #     exit(1)

    rooms_service.addVote(cursor, topic_id, value, obj['user'].id)


if __name__ == '__main__':
    run_command()
