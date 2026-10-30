from flask import Flask
from flask_restful import Resource, Api
import datetime
import socket

app = Flask(__name__)
api = Api(app)


class ReturnIndex(Resource):
    def get(self):
        return {
            "app_name": "${{ values.app_name }}",
            "env": "${{ values.app_env }}",
            "endpoints": ["/api/v1/info", "/livez", "/readyz"],
        }


class ReturnInfo(Resource):
    def get(self):
        return {
            "time": datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y"),
            "hostname": socket.gethostname(),
            "message": "You are welcome to the ${{ values.app_name }}!",
            "deployed_on": "kubernetes",
            "env": "${{ values.app_env }}",
            "app_name": "${{ values.app_name }}",
        }


class ReturnLive(Resource):
    # Liveness: is the process able to respond? Never check dependencies here.
    def get(self):
        return {"status": "alive"}, 200


class ReturnReady(Resource):
    # Readiness: can this pod serve traffic right now? Add dependency checks (DB, downstream APIs) here.
    def get(self):
        return {"status": "ready"}, 200


api.add_resource(ReturnIndex, "/")
api.add_resource(ReturnInfo, "/api/v1/info")
api.add_resource(ReturnLive, "/livez")
api.add_resource(ReturnReady, "/readyz")

if __name__ == "__main__":
    # Local development only; the container runs gunicorn
    app.run(host="0.0.0.0", port=5000)
