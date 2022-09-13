from flask_restx import Namespace, Resource

ns = Namespace('example', description='Respond with Hello World')


@ns.route('/')
class Tenants(Resource):
    @staticmethod
    def get():
        """Respond to request with 'Hello World'"""
        return 'Hello World', 200
