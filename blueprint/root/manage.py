from blueprint.root import root


@root.route('/')
def index():
    return "<h1 align='center'>super　notes　server</h1>"
