""":mod:`getpost` --- Getpost project module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from os.path import join, dirname, abspath

from flask import Flask, render_template, send_from_directory
from flask.ext.login import LoginManager, AnonymousUserMixin
from flask.ext.mail import Mail
from flask.ext.bootstrap import Bootstrap


ANONYMOUS_ROLE = 'anonymous_role'

mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    configure_login_manager()
    register_blueprints(app)
    install_error_handlers(app)
    install_static_routers(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    return app


def configure_login_manager():

    class MyAnonymousUser(AnonymousUserMixin):
        def get_current_role(self):
            return ANONYMOUS_ROLE

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'fatlady.login'
    login_manager.login_message_category = 'error'
    login_manager.anonymous_user = MyAnonymousUser


def register_blueprints(app):
    from .hogwarts import hogwarts_blueprint
    from .hogwarts.fatlady import fatlady_blueprint
    from .hogwarts.owls import owls_blueprint
    from .hogwarts.parcels import parcels_blueprint
    from .hogwarts.wizards import wizards_blueprint
    from .hogwarts.househead import househead_blueprint

    blueprints = [
        hogwarts_blueprint, fatlady_blueprint, househead_blueprint,
        owls_blueprint, parcels_blueprint, wizards_blueprint,
    ]

    # TODO : choose one of three choices
    # choice 1
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    '''
    # choice 2
    [app.register_blueprint(blueprint) for blueprint in blueprints]

    # choice 3
    map(app.register_blueprint, blueprints)
    '''


def install_error_handlers(app):
    @app.errorhandler(500)
    def internal(error):
        desc = 'Uh oh! Something went wrong.'
        return render_template(
            'voldemort.html', status=500, description=desc
        ), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        desc = 'This method is not allowed.'
        return render_template(
            'voldemort.html', status=405, description=desc
        ), 405

    @app.errorhandler(404)
    def not_found(error):
        desc = 'This page does not exist.'
        return render_template(
            'voldemort.html', status=404, description=desc
        ), 404

    @app.errorhandler(403)
    def forbidden(error):
        desc = 'You do not have permission to access this page.'
        return render_template(
            'voldemort.html', status=403, description=desc
        ), 403

    @app.errorhandler(401)
    def unauthorized(error):
        desc = 'You do not have necessary authentication to access this page.'
        return render_template(
            'voldemort.html', status=403, description=desc
        ), 403


def install_static_routers(app):
    static_directory = join(abspath(dirname(__file__)), 'static/')

    css_codenames = {'footer.css': 'padfoot.css',
                     'error.css': 'voldemort.css'}

    @app.route('/css/<path:path>')
    def send_css(path):
        if path in css_codenames:
            path = css_codenames[path]
        return send_from_directory(join(static_directory, 'css/'), path)

    js_codenames = {'signup.js': 'boats.js',
                    'edit.js': 'transfigure.js',
                    'addaccount.js': 'letter.js'}

    @app.route('/js/<path:path>')
    def send_js(path):
        if path in js_codenames:
            path = js_codenames[path]
        return send_from_directory(join(static_directory, 'js/'), path)
