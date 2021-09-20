from flask import Flask, request
from flask_restful import Resource, Api


application = Flask(__name__)
api = Api(application)


queries = {"test1": "buy something"}


class QuerySimple(Resource):
    def get(self, query_id):
        # search dictionary for key=query_id
        return {query_id: queries[query_id]}

    def put(self, query_id):
        # HTTP request, return data from 'data'
        queries[query_id] = request.form["data"]
        return {query_id: queries[query_id]}


api.add_resource(QuerySimple, "/<string:query_id>")


if __name__ == "__main__":
    application.run(debug=True)
