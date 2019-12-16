# Extended bottle

This framework is based on functions table, each route specified in `api/Controller/routes.py`

These functions should be referenced in `/api/Controller/routesfunc.py` and use object specified in the folder `api/Object/`


**routes.py**
```python
@app.route('/test/',   ['OPTIONS', 'POST', 'GET'], lambda x = None: call([])                                 )
@app.route('/login/',  ['OPTIONS', 'POST'],        lambda x = None: call([getauth])                          )
@app.route('/signup/', ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signup, signin, gettoken]) )
```
*The first parameter is the route's URL, the second is an array containning the method(s) allowed, the third is a `lambda` using a funtion of the `cn` object under the name `call`, you'll have to pass it an array of func*
```python
call = lambda x : callnext(request, response).call(x)
```


**routesfunc.py**
```python
def getauth(cn, nextc):
    err = check.contain(cn.pr, ["pass"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    err = auth.gettoken(cn.pr["pass"])
    return cn.call_next(nextc, err)

def myauth(cn, nextc):
    err = check.contain(cn.hd, ["token"], "HEAD")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.hd = err[1]
    err = auth.verify(cn.hd["token"])
    return cn.call_next(nextc, err)

def signup(cn, nextc):
    err = check.contain(cn.pr, ["email", "password1", "password2"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = user()
    err = use.register(cn.pr["email"], cn.pr["password1"], cn.pr["password2"])
    cn.private["user"] = use

    return cn.call_next(nextc, err)
```

**Warning**:

You'll have to follow this partern to create functions in `routesfunc.py`
```python
def signup(cn, nextc):
    err = [TRUE, {}, 200]
    #YOUR CODE
    return cn.call_next(nextc, err)
```

**The `cn` object:**

The `cn` object is created at launch it contain's **POST parameters** under `pr`, **cookies** under `ck`, **headers** under `hd`

``` python
class callnext:
    def __init__(self, req, resp = None, err = None, anonlvl = None):
        self.pr = check.json(req)
        self.ck = check.cookies_json(req)
        self.hd = check.head_json(req, self.ck)
        self.private = {}
        self.cookie = {}
        self.toret = ret(req.path, self.pr, self.hd, self.ck, anonlvl)
        self.req = req
        self.resp = resp
        self.err = err
```

**The `nextc` object:**
It's an array containing the functions left to call

**The `err` object:**
It's an array containing the returns of your function, it'll have the patern:
```python
err = [TRUE,                #FALSE -> it will stop the execution and throw an error
       {"mydata": "test"},  # if TRUE -> json else a string containning an error
       200,                 # response code
       {"mycookie": "data"} # (optionnal) -> cookies to set
      ]
```

### Routes's Basics:

Routes | Methods |
-|-|
`/test/` | POST, GET |
`/login/` | POST |
`/signup/` | POST |
`/signin/` | POST |
`/renew/` | GET |
`/infos/` | GET |
`/updateinfos` | POST |
`/addcard/` | POST |
`/delcard/` | POST |
`/listcard/` | GET |
`/order/` | POST |
`/history/` | POST |
`/orderdetail/` | POST |


### Return template

```javascript
// In DEV mod
  {
  "queryInfos": { //query infos only available on mod: ['DEV', 'TEST']
      "route": "/test/", //the route called
      "params": {}, //params sent in the body
      "header": { //header and cookies are in a common array but header have the priority over cookie
          "host": "api.localhost",
      },
      "cookie": {} //cookies [token && usr_token]
  },
  "status": 200, //http code
  "error": null, //string
  "data": null, //array
  "succes": true, //true or false
  "mod": "DEV" //DEFINED in the .env [DEFAULT = PROD]
}

//cookie sent are relocated in the header, overrided if a header with the same key is provided
```
