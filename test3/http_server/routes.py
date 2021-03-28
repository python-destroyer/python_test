from views import method_A, method_B

def setup_routes(app):
    app.router.add_route('GET', "/A", method_A)
    app.router.add_route('GET', "/B", method_B)