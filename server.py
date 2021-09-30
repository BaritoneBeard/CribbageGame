from flask import Flask, request
from flask_restful import Resource, Api
import logging

logger = logging.getLogger("server.py")
logging.basicConfig(filename="serverlog.txt", filemode ='w')  # every time server is restarting the log is overwritten
logger.setLevel(logging.INFO)
# logger.error("this is an ERROR test")
# logger.warning("this is a warning test")
# logger.info("this is an info test")
# logger.debug("this is a debug test")
application = Flask(__name__)
api = Api(application)

status_code = {200:"OK -- Successful", 201:"Created", 205: "Content Rest",
               404: "Not Found", 409: "Conflict", 500: "Internal Server Error"}
queries = {"test1": "buy something", "index_page": "This is the home page."}


class QuerySimple(Resource):
    def post(self, query_id):  # Create
        # HTTP request, return data from 'data'
        logger.info("Attempting to Create {} \n".format(query_id))
        queries[query_id] = request.form["data"]
        try:
            return {query_id: queries[query_id]}, 201
        except:
            return {"error": "unable to create item"}, 404

    def get(self, query_id="index_page"):  # Return
        # search dictionary for key=query_id, return it
        logger.info("Attempting to Return {} \n".format(query_id))
        try:
            return {query_id: queries.get(query_id, "does not exit")}
        except TypeError:
            return 404

    def put(self, query_id):  # Update
        logger.info("Attempting to Update {} \n".format(query_id))
        queries[query_id] = request.form["data"]
        try:
            return {query_id: queries[query_id]}, 200
        except:
            print("Temporarily catch all ERROR")

    def delete(self, query_id):  # Delete
        logger.info("Attempting to Delete {} from dictionary \n".format(query_id))
        try:
            queries.pop(queries[query_id])
        except:
            print("Temporary catch all ERROR")


# add a path to '/query_id' i.e. 'localhost:5000/test1'
# add a path that doesn't require any resources, all but GET should cause errors
api.add_resource(QuerySimple, '/', "/<string:query_id>")


if __name__ == "__main__":
    application.run(debug=True)
