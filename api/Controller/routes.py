from .routesfunc import *

def setuproute(app, call):
    @app.route('/test/',            ['OPTIONS', 'POST', 'GET'], lambda x = None: call([])                                    )
    @app.route('/login/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([getauth])                             )
    @app.route('/signup/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signup, signin, gettoken])    )
    @app.route('/signin/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signin, gettoken])            )
    @app.route('/renew/',    	    ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, gettoken])          )
    @app.route('/infos/',    	    ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, infos])             )
    @app.route('/updateinfos/',    	['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, upinfos])           )
    @app.route('/addcard/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, addcard])                   )
    @app.route('/delcard/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser ])                   )
    @app.route('/listcard/',    	['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, listcard])                   )
    @app.route('/order/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser ])                   )
    @app.route('/orderdetail/',    	['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser ])                   )
    @app.route('/history/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser ])                   )
    @app.route('/emulate/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([])                                    )
    def base():
        return
