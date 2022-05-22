import os
from flask import Flask, render_template

from flask_app.blueprints.user.models.user_auth_model import UserOauth
from flask_app.applogger import logger
from flask_app.blueprints_register import register_all_blueprints
from flask_app.sqldb.appdb import register_app_with_db
from flask_app.blueprints.user.user_authentication import login_is_required

INSTANCE_CONFIG_FILE = "config.py"
ENV_CONFIGS_MODULE = f"configs.config.{os.environ['FLASK_ENV']}Config"


def create_app(test_config=None):
    template_dir = os.path.abspath('flask_app/frontend/templates')
    static_dir = os.path.abspath('flask_app/frontend/static')
    logger.debug(template_dir)

    app = Flask(__name__,
                instance_relative_config=True, 
                template_folder=template_dir, 
                static_folder=static_dir)

    app.config.from_object(ENV_CONFIGS_MODULE)

    app.config.from_mapping(
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
    )

    if test_config is None:
        logger.debug("Loading configs from pyfile config.py")
        app.config.from_pyfile(INSTANCE_CONFIG_FILE, silent=True)
    else:
        logger.debug("Loading configs from test_config")
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print(app.config)
    logger.info(f"Loaded configs\n {app.config}")

    register_app_with_db(app)
    register_all_blueprints(app)

    @app.route("/")
    def hello_world():
        return render_template("index.html")

    @app.route("/protected")
    @login_is_required
    def user_is_logged_in(user: UserOauth):
        return f"User is logged in {user.given_name}"

    return app
