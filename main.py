import sqlite3
import sys
from sqlite3 import Cursor
import os
import click as click

from database import database
from database.database import Database
from users import users_service
from users.user_model import User

db = Database


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
    print(user)
    return user



if __name__ == '__main__':
    run_command()
