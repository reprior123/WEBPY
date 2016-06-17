

if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

db.define_table('campaigns_audit',
   Field('name'),
   Field('role'))
db.define_table('cases',
   Field('name'),
   Field('role'))
