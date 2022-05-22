from flask_app.blueprints.user import user_authentication
from flask_app.blueprints.albums import photo_albums
from flask_app.blueprints.similar_images import similar_images_api
from flask_app.blueprints.dashboard import dashboard

def register_all_blueprints(app):
    app.register_blueprint(user_authentication.bp)
    app.register_blueprint(photo_albums.bp)
    app.register_blueprint(similar_images_api.bp)
    app.register_blueprint(dashboard.bp)