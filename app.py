from robyn import Robyn

app = Robyn(__file__)

@app.get("/")
async def h(request): # request is an optional parameter
    return "Hello, world!"

app.start(port=8000, url="0.0.0.0") # url is optional, defaults to 127.0.0.1

class Select:

    def __init__(self, table_name, *columns):
        self.query = f"SELECT {', '.join(columns)} from {table_name}"

    def where(self, *conditions):

        return

def select(table_name, *columns):

    return f"SELECT {', '.join(columns)} from {table_name}"

def where(*conditions):
    pass




# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
