import sqlite3
import sys
from sqlite3 import Cursor
import os
import click as click

from database import database
from database.database import Database
from rooms import rooms_service
from users import users_service
from users.user_model import User
from rooms.rooms_service import Room

db = Database


@click.pass_context
def user(obj, login, password):
    print(obj)
    with obj:
        cursor = obj['db'].cursor()
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
        'db': db
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


@user_command.command("list")
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
    rooms_service.insertIntoRooms(obj['db'].cursor(), obj['user'].id, room_password)


if __name__ == '__main__':
    run_command()
