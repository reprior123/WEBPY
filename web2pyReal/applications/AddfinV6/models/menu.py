# coding: utf8

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('this is the subtitle response in models menu')

##########################################
## this is the authentication menu
## remove if not necessary
##########################################

if 'auth' in globals():
    if not auth.is_logged_in():
       response.menu_auth = [
           [T('Login'), False, auth.settings.login_url,
            [
                   [T('Register'), False,
                    URL(request.application,'default','user/register')],
                   [T('Lost Password'), False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
           ]
    else:
        response.menu_auth = [
            ['User: '+auth.user.first_name,False,None,
             [
                    [T('Logout'), False,
                     URL(request.application,'default','user/logout')],
                    [T('Edit Profile'), False,
                     URL(request.application,'default','user/profile')],
                    [T('Change Password'), False,
                     URL(request.application,'default','user/change_password')]]
             ],
            ]

##########################################
## this is the main application menu
## add/remove items as required
##########################################
##response.menu.old = [
##    [T('Index'), False,
##     URL(request.application,'default','index'), []],
##    ]

response.menu = [
     [T('anychange').capitalize(), False,'', 
         [
         [T('level1-1').capitalize(),False,URL(request.application,'defaultlevel1','index'),
             [
                 [T('level2-1').capitalize(),
                 False,
                 URL(request.application,
                 'defaultlevel1',
                 'index'),
                 []],
             ]],
         [T('level1-2').capitalize(),
             False,
             URL(request.application,
             'controller',
             'function'),
             []],
         [T('level1-3').capitalize(),
             False,
             URL(request.application,
             'controller',
             'function'),
             []],
         
     ]],


     [T('root2').capitalize(),
         False,
         '',
         [
             [T('level1-1').capitalize(),
                 False,
                 URL(request.application,
                 'controller',
                 'function'),
                 []],
             [T('level1-2').capitalize(),
                 False,
                 URL(request.application,
                 'controller',
                 'function'),
                 []],
     ]],
    ]
