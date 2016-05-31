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


response.menu=[
  ['organizations',False,url('list_organizations')],
  ['crm_compliance',False,url('list_crm_compliance')],
  ['address_book',False,url('list_address_book')],
  ['calls',False,url('list_calls')],
  ['cases',False,url('list_cases')],
  ['client_roles',False,url('list_client_roles')],
  ['crm_contacts',False,url('list_crm_contacts')],
  ['portfolios',False,url('list_portfolios')],
  ['currencies',False,url('list_currencies')],
  ['custom_fields',False,url('list_custom_fields')],
  ['database_fundinfo',False,url('list_database_fundinfo')],
  ['fdata__products',False,url('list_fdata__products')],
  ['documents',False,url('list_documents')],
  ['emails',False,url('list_emails')],
  ['fields_meta_data',False,url('list_fields_meta_data')],
  ['gii',False,url('list_gii')],
  ['crm_custRelation',False,url('list_crm_custRelation')],
  ['kreports',False,url('list_kreports')],
  ['leads',False,url('list_leads')],
  ['fundinfo_docs',False,url('list_fundinfo_docs')],
  ['fdata_vdf',False,url('list_fdata_vdf')],
  ['fdata_rolotec',False,url('list_fdata_rolotec')],
  ['mandate_bands',False,url('list_mandate_bands')],
  ['tasks',False,url('list_tasks')],
  ['meetings',False,url('list_meetings')],
  ['fdata_transactions',False,url('list_fdata_transactions')],
  ['portfolio',False,url('list_portfolio')],
  ['allocationModel',False,url('list_allocationModel')],
  ['pii',False,url('list_pii')],
  ['rules_n_bands',False,url('list_rules_n_bands')],
  ['stamm_acct',False,url('list_stamm_acct')],
  ['sub_acct',False,url('list_sub_acct')],
  ['depot_banks',False,url('list_depot_banks')],
  ['benchmarks',False,url('list_benchmarks')],
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
def list_crm_compliance():
	form=crud.create(db.crm_compliance )
	crm_compliance=db(db.crm_compliance.id>0).select(orderby=db.crm_compliance.id)
	return dict(crm_compliance=crm_compliance,form=form)
def list_address_book():
	form=crud.create(db.address_book )
	address_book=db(db.address_book.id>0).select(orderby=db.address_book.id)
	return dict(address_book=address_book,form=form)
def list_calls():
	form=crud.create(db.calls )
	calls=db(db.calls.id>0).select(orderby=db.calls.id)
	return dict(calls=calls,form=form)
def list_cases():
	form=crud.create(db.cases )
	cases=db(db.cases.id>0).select(orderby=db.cases.id)
	return dict(cases=cases,form=form)
def list_client_roles():
	form=crud.create(db.client_roles )
	client_roles=db(db.client_roles.id>0).select(orderby=db.client_roles.id)
	return dict(client_roles=client_roles,form=form)
def list_crm_contacts():
	form=crud.create(db.crm_contacts )
	crm_contacts=db(db.crm_contacts.id>0).select(orderby=db.crm_contacts.id)
	return dict(crm_contacts=crm_contacts,form=form)
def list_portfolios():
	form=crud.create(db.portfolios )
	portfolios=db(db.portfolios.id>0).select(orderby=db.portfolios.id)
	return dict(portfolios=portfolios,form=form)
def list_currencies():
	form=crud.create(db.currencies )
	currencies=db(db.currencies.id>0).select(orderby=db.currencies.id)
	return dict(currencies=currencies,form=form)
def list_custom_fields():
	form=crud.create(db.custom_fields )
	custom_fields=db(db.custom_fields.id>0).select(orderby=db.custom_fields.id)
	return dict(custom_fields=custom_fields,form=form)
def list_database_fundinfo():
	form=crud.create(db.database_fundinfo )
	database_fundinfo=db(db.database_fundinfo.id>0).select(orderby=db.database_fundinfo.id)
	return dict(database_fundinfo=database_fundinfo,form=form)
def list_fdata__products():
	form=crud.create(db.fdata__products )
	fdata__products=db(db.fdata__products.id>0).select(orderby=db.fdata__products.id)
	return dict(fdata__products=fdata__products,form=form)
def list_documents():
	form=crud.create(db.documents )
	documents=db(db.documents.id>0).select(orderby=db.documents.id)
	return dict(documents=documents,form=form)
def list_emails():
	form=crud.create(db.emails )
	emails=db(db.emails.id>0).select(orderby=db.emails.id)
	return dict(emails=emails,form=form)
def list_fields_meta_data():
	form=crud.create(db.fields_meta_data )
	fields_meta_data=db(db.fields_meta_data.id>0).select(orderby=db.fields_meta_data.id)
	return dict(fields_meta_data=fields_meta_data,form=form)
def list_gii():
	form=crud.create(db.gii )
	gii=db(db.gii.id>0).select(orderby=db.gii.id)
	return dict(gii=gii,form=form)
def list_crm_custRelation():
	form=crud.create(db.crm_custRelation )
	crm_custRelation=db(db.crm_custRelation.id>0).select(orderby=db.crm_custRelation.id)
	return dict(crm_custRelation=crm_custRelation,form=form)
def list_kreports():
	form=crud.create(db.kreports )
	kreports=db(db.kreports.id>0).select(orderby=db.kreports.id)
	return dict(kreports=kreports,form=form)
def list_leads():
	form=crud.create(db.leads )
	leads=db(db.leads.id>0).select(orderby=db.leads.id)
	return dict(leads=leads,form=form)
def list_fundinfo_docs():
	form=crud.create(db.fundinfo_docs )
	fundinfo_docs=db(db.fundinfo_docs.id>0).select(orderby=db.fundinfo_docs.id)
	return dict(fundinfo_docs=fundinfo_docs,form=form)
def list_fdata_vdf():
	form=crud.create(db.fdata_vdf )
	fdata_vdf=db(db.fdata_vdf.id>0).select(orderby=db.fdata_vdf.id)
	return dict(fdata_vdf=fdata_vdf,form=form)
def list_fdata_rolotec():
	form=crud.create(db.fdata_rolotec )
	fdata_rolotec=db(db.fdata_rolotec.id>0).select(orderby=db.fdata_rolotec.id)
	return dict(fdata_rolotec=fdata_rolotec,form=form)
def list_mandate_bands():
	form=crud.create(db.mandate_bands )
	mandate_bands=db(db.mandate_bands.id>0).select(orderby=db.mandate_bands.id)
	return dict(mandate_bands=mandate_bands,form=form)
def list_tasks():
	form=crud.create(db.tasks )
	tasks=db(db.tasks.id>0).select(orderby=db.tasks.id)
	return dict(tasks=tasks,form=form)
def list_meetings():
	form=crud.create(db.meetings )
	meetings=db(db.meetings.id>0).select(orderby=db.meetings.id)
	return dict(meetings=meetings,form=form)
def list_fdata_transactions():
	form=crud.create(db.fdata_transactions )
	fdata_transactions=db(db.fdata_transactions.id>0).select(orderby=db.fdata_transactions.id)
	return dict(fdata_transactions=fdata_transactions,form=form)
def list_portfolio():
	form=crud.create(db.portfolio )
	portfolio=db(db.portfolio.id>0).select(orderby=db.portfolio.id)
	return dict(portfolio=portfolio,form=form)
def list_allocationModel():
	form=crud.create(db.allocationModel )
	allocationModel=db(db.allocationModel.id>0).select(orderby=db.allocationModel.id)
	return dict(allocationModel=allocationModel,form=form)
def list_pii():
	form=crud.create(db.pii )
	pii=db(db.pii.id>0).select(orderby=db.pii.id)
	return dict(pii=pii,form=form)
def list_rules_n_bands():
	form=crud.create(db.rules_n_bands )
	rules_n_bands=db(db.rules_n_bands.id>0).select(orderby=db.rules_n_bands.id)
	return dict(rules_n_bands=rules_n_bands,form=form)
def list_stamm_acct():
	form=crud.create(db.stamm_acct )
	stamm_acct=db(db.stamm_acct.id>0).select(orderby=db.stamm_acct.id)
	return dict(stamm_acct=stamm_acct,form=form)
def list_sub_acct():
	form=crud.create(db.sub_acct )
	sub_acct=db(db.sub_acct.id>0).select(orderby=db.sub_acct.id)
	return dict(sub_acct=sub_acct,form=form)
def list_depot_banks():
	form=crud.create(db.depot_banks )
	depot_banks=db(db.depot_banks.id>0).select(orderby=db.depot_banks.id)
	return dict(depot_banks=depot_banks,form=form)
def list_benchmarks():
	form=crud.create(db.benchmarks )
	benchmarks=db(db.benchmarks.id>0).select(orderby=db.benchmarks.id)
	return dict(benchmarks=benchmarks,form=form)

############################
def list_logs():
    person_id=request.args(0)
    person=db.person[person_id] or redirect(error_page)
    session.recent_persons = add(session.recent_persons,person)
    db.log.person.default=person.id
    db.log.person.writable=False
    db.log.person.readable=False
    form=crud.create(db.log)
    logs=db(db.log.person==person.id).select(orderby=~db.log.created_on)
    return dict(person=person,logs=logs,form=form)

@auth.requires_login()
def edit_person():
    person_id=request.args(0)
    person=db.person[person_id] or redirect(error_page)
    session.recent_persons = add(session.recent_persons,person)
    db.person.company.writable=False
    db.person.company.readable=False
    form=crud.update(db.person,person,next=url('view_person',person_id))
    return dict(form=form)


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

@auth.requires_login()
def list_tasks():
    person_id=request.args(0)
    person=db.person[person_id]
    if person_id:
       session.recent_tasks = add(session.recent_tasks,task)
       tasks=db(db.task.person==person_id)\
               (db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select()
    else:
       tasks=db(db.task.created_by==auth.user.id)\
               (db.task.start_time<=request.now).select()
    db.task.person.default=person_id
    db.task.person.writable=db.task.person.readable=False
    form=crud.create(db.task,next='view_task/[id]')
    return dict(tasks=tasks,person=person,form=form)

@auth.requires_login()
def calendar():
    person_id=request.args(0)
    person=db.person[person_id]
    if person_id:
       tasks=db(db.task.person==person_id)\
               (db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select()
    else:
       tasks=db(db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select()
    return dict(tasks=tasks,person=person)

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
def hello5():
    return HTML(BODY(H1(T('Hello World'),_style="color: red;"))).xml() # .xml to serialize
def hello6():
    response.flash=T("Hello World in a flash!")
    return dict(message=T("Hello World"))
def hello4():
    response.view='simple_examples/hello3.html'
    return dict(message=T("Hello World"))
def hello3():
    return dict()
##    return dict(message=T("Hello World"))
def statusex():
    return dict(toobar=response.toolbar())

def redirectme():
    redirect(URL('hello3'))
                   
def raisehttp():
    raise HTTP(400,"internal error")
             
def ajaxwiki():
    form=FORM(TEXTAREA(_id='text',_name='text'),
              INPUT(_type='button',_value='markmin click to save',
              _onclick="ajax('ajaxwiki_onclick',['text'],'html')"))
    return dict(form=form,html=DIV(_id='html'))

def ajaxwiki_onclick():
    return MARKMIN(request.vars.text).xml()           
