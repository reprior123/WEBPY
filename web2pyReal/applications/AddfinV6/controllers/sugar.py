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



def index():
    return dict()
