import configargparse

CONFIG = None

arg_parser = configargparse.ArgParser(default_config_files=["config.txt"])

arg_parser.add("-c", "--config", is_config_file=True, help="Config file")

arg_parser.add(
    "-d",
    "--database_connection",
    default="sqlite:///data.db",
    help="An SQLAlchemy connection string",
)

arg_parser.add("--host", default="127.0.0.1", help="Bind socket to this host")

arg_parser.add("--port", default="8000", help="Bind socket to this port")

arg_parser.add("-m", "--mail_port", default="587", help="email TSL port")

arg_parser.add("-f", "--mail_from", default="App Listing", help="preffered from name")

arg_parser.add("-s", "--mail_server", default="smtp.gmail.com", help="your mail server")


def parse_args():
    global CONFIG
    CONFIG = arg_parser.parse_args()
