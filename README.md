# transport-api


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
`/emulate/` | POST |


### Return template

```javascript
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
```
