from flask import Flask, jsonify, Response, request, json
from flask import Blueprint
from datetime import datetime
import time
import MySQLdb
from os import getenv

server = None
config = None

# Clasa care modeleaza server-ul de login

class LOGIN_SERVER:
    def __init__(
        self,
        app: Flask,
        blueprints_lst,
        configuration,
        connection=None,
        cursor=None,
        host="0.0.0.0",
    ):
        self.app = app
        self.host = host
        self.blueprints_lst = blueprints_lst
        self.configuration = configuration
        self.connection = connection
        self.cursor = cursor

    def config_server(self):
        self.connection = MySQLdb.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            passwd=config["password"],
            db=config["database"],
        )
        self.cursor = self.connection.cursor()

    def register_blueprints(self):
        for blueprint in self.blueprints_lst:
            self.app.register_blueprint(blueprint)


class API_AUTH:
    def __init__(self, blueprint, database, fields_list, request=None):
        self.database = database
        self.request = request
        self.fields_list = fields_list
        self.blueprint = blueprint


# Mici configuratii pentru buna functionare a server-ului

app = Flask(__name__)

config = {
    "user": getenv("MYSQL_USER"),
    "password": getenv("MYSQL_PASSWORD"),
    "host": "mysql-db",
    "port": int(getenv("MYSQL_PORT")),
    "database": getenv("MYSQL_DATABASE"),
}

auth_logic = Blueprint("auth_logic", __name__)
auth = API_AUTH(
    auth_logic,
    "Accounts",
    [],
)

server = LOGIN_SERVER(
    app,
    [auth_logic],
    config,
)

# Functiile care modeleaza ruta

@auth_logic.route("/", methods=[" "])
def process_login_logic():
    auth.request = request
    server.config_server()

    return None


server.register_blueprints()

if __name__ == "__main__":
    server.app.run(server.host)
