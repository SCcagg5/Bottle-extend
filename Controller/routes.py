from .routesfunc import *

def setuproute(app, call):
    @app.route('/test/',        ['OPTIONS', 'POST', 'GET'], lambda x = None: call([])                       )
    @app.route('/exemple/',    	['OPTIONS', 'POST'],        lambda x = None: call([exemple])                )
    def base():
        return
