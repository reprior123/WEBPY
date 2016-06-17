# coding: utf8

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

error_page=URL('error')

if not session.recent_companies: session.recent_companies=[]
if not session.recent_persons: session.recent_persons=[]
if not session.recent_tasks: session.recent_tasks=[]
if not session.recent_accounts: session.recent_accounts=[]


def layoutaddfinthemehome():
    return dict()
response.menu=[
  ['organizations',False,url('list_organizations')],
  ['crm_contacts',False,url('list_crm_contacts')],
  ['currencies',False,url('list_currencies')],
]

def add(mylist,item):
    if not item.id in [x[0] for x in mylist]:
        return mylist[:9]+[(item.id,item.name)]
    else:
        return mylist

def index():
    return dict()
def list_organizations():
	form=crud.create(db.organizations )
	organizations=db(db.organizations.id>0).select(orderby=db.organizations.id)
	return dict(organizations=organizations,form=form)

def list_currencies():
	form=crud.create(db.currencies )
	currencies=db(db.currencies.id>0).select(orderby=db.currencies.id)
	return dict(currencies=currencies,form=form)
def list_crm_contacts():
	form=crud.create(db.list_crm_contacts )
	custom_fields=db(db.list_crm_contacts.id>0).select(orderby=db.list_crm_contacts.id)
	return dict(list_crm_contacts=list_crm_contacts,form=form)
############################

@auth.requires_login()
def edit_task():
    task_id=request.args(0)
    task=db.task[task_id] or redirect(error_page)
    person=db.person[task.person]
    db.task.person.writable=db.task.person.readable=False
##    session.recent_tasks = add(session.recent_tasks,task)
    form=crud.update(db.task,task,next='view_task/[id]')
    return dict(form=form, person=person)

@auth.requires_login()
def view_task():
    task_id=request.args(0)
    task=db.task[task_id] or redirect(error_page)
    person=db.person[task.person]
##    session.recent_tasks = add(session.recent_tasks,person)

    db.task.person.writable=db.task.person.readable=False
    form=crud.read(db.task,task)

    return dict(form=form, person=person, task=task)

@auth.requires(auth.user and auth.user.email=='reprior123@gmail.com')
def reset():
    for table in db.tables:
        if table=='auth_user':
            db(db[table].email!='reprior123@gmail.com').delete()
        else:
            db(db[table].id>0).delete()
    session.flash='done!'
    redirect('index')
def error():
    return dict(message="something is wrong")
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
###########################
  
