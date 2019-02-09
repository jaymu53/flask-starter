import os
from flask_restplus import Api
import app.resources as resources
from app import create_app

config_name = os.getenv('APP_SETTINGS') or 'development' # config_name = "development"
app = create_app(config_name)
api = Api(app)


#resourse route mappings
api.add_resource(resources.UserResource, '/user')
api.add_resource(resources.ProtectedResource, '/protected')
api.add_resource(resources.Logout, '/logout')

if __name__ == '__main__':
    app.run()

