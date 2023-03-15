
routes = {}


def route(path):
    def wrapper(handler):
        routes[path] = handler
        return handler
    return wrapper


@route('/')
def index_handler():
    return '<h1>Welcome to my website!</h1>', 200


@route('/about')
def about_handler():
    return '<h1>About us</h1><p>We are a small company that loves to make websites.</p>', 200


@route('/contact')
def contact_handler():
    return '<h1>Contact us</h1><p>Email: info@example.com</p><p>Phone: 555-1234</p>', 200


@route('/api/smartmeter')
def data_handler():
    return '{"data": "[1, 2, 3, 4, 5]"}', 200


def not_found():
    return 'Page not found', 404

################################################################################################################
    """
    handler = routes.get(path, not_found)
    print(handler.__name__)
    response, status = handler()
    
    """
