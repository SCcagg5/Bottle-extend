from Model.basic import check
#from Object.your_obj import yourclass

def exemple(cn, nextc):
    err = check.contain(cn.pr, ["mail", ["password", "token"]])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    #use = #init your obj here
    #err = use.your_func()
    #cn.private["user_id"] = use.id
    return cn.call_next(nextc, err)
