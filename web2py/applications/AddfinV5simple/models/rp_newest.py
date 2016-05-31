TASK_TYPES = ('Phone', 'Fax', 'Mail', 'Meet')

if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

db.define_table('organizations',
         Field('id', 'string', length=150,default=None, required=False),
         Field('name', 'string', length=150,default=None, required=False),
         Field('org_type', 'string', length=100,default=None, required=False),
         Field('industry', 'string', length=50,default=None, required=False),
         Field('annual_revenue', 'string', length=100,default=None, required=False),
         Field('website', 'string', length=255,default=None, required=False),
         Field('ownership', 'string', length=100,default=None, required=False),
         Field('employees', 'string', length=10,default=None, required=False),
         Field('ticker_symbol', 'string', length=10,default=None, required=False),                
         Field('sic_code', 'string', length=10,default=None, required=False))
                
db.define_table('crm_phones',  # these are attached to cons&Orgs
         Field('phone_type', 'string', length=100,default=None, required=False), ## pulldown list office,home,mobile,mobile2,other,other2
         Field('conorg_type', 'string', length=100,default=None, required=False), ## pulldown list contacts,organizations
         Field('phone_number', 'string', length=100,default=None, required=False), ## prefix info?
         Field('contacts_id', 'string', length=36,default=None, required=False), # can user conorg_id instead?
         Field('organization_id', 'string', length=36,default=None, required=False))
                
db.define_table('crm_addresses',         # these are attached to cons&Orgs
         Field('address_type', 'string', length=100,default=None, required=False), ## pulldown list primary,alt,billing,shipping,mailing,home,office,other,other2
         Field('conorg_type', 'string', length=100,default=None, required=False), ## pulldown list contacts,organizations,korr_thirdparty[CRs?]
         Field('contacts_id', 'string', length=36,default=None, required=False), # can user conorg_id instead?
         Field('organization_id', 'string', length=36,default=None, required=False),
         Field('address_street', 'string', length=150,default=None, required=False),
         Field('address_city', 'string', length=100,default=None, required=False),
         Field('address_state', 'string', length=100,default=None, required=False),
         Field('address_postalcode', 'string', length=20,default=None, required=False),
         Field('address_country', 'string', length=255,default=None, required=False),
         Field('accounts_accounts_1accounts_ida', 'string', length=36,default=None, required=False),
         Field('contact_id', 'string', length=36,default=None, required=False),
         Field('account_id', 'string', length=36,default=None, required=False),

         Field('id_c', 'string', length=36,default=None, required=False),
         Field('language_c', 'string', length=100,default= 'english', required=False),
         Field('skype_c', 'string', length=255,default=None, required=False),
         Field('facebook_c', 'string', length=255,default=None, required=False),
         Field('linkein_c', 'string', length=255,default=None, required=False),
         Field('company_type_c', 'string', length=100,default= 'limited_corporation', required=False),
         Field('relationship_c', 'string', length=100,default= 'partner', required=False),

         Field('bean', 'string', length=50,default=None, required=False),
         Field('bean_id', 'string', length=36,default=None, required=False))
                #####################
      
         # standard system
####         Field('date_entered', 'datetime',default=None, required=False),
####         Field('date_modified', 'datetime',default=None, required=False),
####         Field('modified_user_id', 'string', length=36,default=None, required=False),
####         Field('created_by', 'string', length=36,default=None, required=False),
####         Field('assigned_user_id', 'string', length=36,default=None, required=False),
####         Field('parent_id', 'string', length=36,default=None, required=False),
####         Field('campaign_id', 'string', length=36,default=None, required=False),
####         Field('filename', 'string', length=255,default=None, required=False),
####         Field('deleted', 'integer',default= '0', required=False),
####         Field('data_type', 'string', length=100,default=None, required=False),
####         Field('before_value_string', 'string', length=255,default=None, required=False),
####         Field('after_value_string', 'string', length=255,default=None, required=False), ### only for audit tables....                
####         Field('before_value_text', 'date',default=None, required=False),
####         Field('after_value_text', 'date',default=None, required=False))
               
db.define_table('crm_compliance', ## these are attached to CRs
         Field('nxcfile_pepdoc', 'string', length=255,default=None, required=False),
         Field('pepcheckstatus', 'string', length=255,default= '2', required=False),
         Field('taxt_status', 'string', length=255,default=None, required=False),        
         Field('name2_c', 'string', length=255,default=None, required=False),
         Field('memberships_c', 'date',default=None, required=False))
### crm still needs calls,tasks,

db.define_table('client_roles',
	Field('clientrole', 'string', length=100,default= 'ContractingParty', required=False),
	Field('client_role_signatory_r', 'string', length=100,default= 'IndividualSignature', required=False))

db.define_table('crm_contacts',
         Field('clientroles_accountsclientroles_ida', 'string', length=36,default=None, required=False),
         Field('clientroles_accountsaccounts_idb', 'string', length=36,default=None, required=False),

         Field('clientroles_contactsclientroles_ida', 'string', length=36,default=None, required=False),
         Field('clientroles_contactscontacts_idb', 'string', length=36,default=None, required=False),
         Field('category', 'string', length=32,default=None, required=False),
         Field('name', 'string', length=32,default=None, required=False),
         Field('salutation', 'string', length=255,default=None, required=False),
                
         Field('first_name', 'string', length=100,default=None, required=False),
         Field('last_name', 'string', length=100,default=None, required=False),
         Field('title', 'string', length=100,default=None, required=False),
                
         Field('department', 'string', length=255,default=None, required=False),
         Field('do_not_call', 'integer',default= '0', required=False),
                
         Field('assistant', 'string', length=75,default=None, required=False),
         Field('assistant_phone', 'string', length=100,default=None, required=False),
         Field('lead_source', 'string', length=255,default=None, required=False),
         Field('reports_to_id', 'string', length=36,default=None, required=False),
                
         Field('birthdate', 'datetime',default=None, required=False),
         Field('campaign_id', 'string', length=36,default=None, required=False),
         Field('occupation_c', 'string', length=255,default=None, required=False),
         Field('nickname', 'string', length=255,default=None, required=False),
         Field('skype', 'string', length=255,default=None, required=False),
         Field('facebook', 'string', length=255,default=None, required=False),
         Field('linkedin', 'string', length=255,default=None, required=False),
         Field('source', 'string', length=255,default=None, required=False),

         Field('wealth_size', 'string', length=255,default=None, required=False),
         Field('investment_size', 'string', length=255,default=None, required=False),
                
         Field('protect', 'string', length=255,default=None, required=False),
         Field('mantain', 'string', length=255,default=None, required=False),
         Field('improve', 'string', length=255,default=None, required=False),
         Field('partner', 'string', length=255,default=None, required=False),
                
         Field('middle_name', 'string', length=255,default=None, required=False),
                
         Field('memberships', 'date',default=None, required=False),                
         Field('type', 'string', length=255,default=None, required=False),
                
         Field('contact_language', 'string', length=255,default=None, required=False),
                
         Field('home_currency', 'string', length=255,default=None, required=False), ##might need for fee billing?
                
         Field('investment_currency', 'string', length=255,default=None, required=False),
                
         Field('married_status', 'string', length=255,default=None, required=False),
         Field('children', 'string', length=255,default=None, required=False),
         Field('nationality1', 'string', length=255,default=None, required=False),
         Field('nationality2', 'string', length=255,default=None, required=False),
         Field('nationality3', 'string', length=255,default=None, required=False),
         Field('domicile', 'string', length=255,default=None, required=False),
         Field('resident', 'string', length=255,default=None, required=False),

         Field('photo_field_c', 'string', length=255,default=None, required=False),
         Field('occupation', 'string', length=255,default=None, required=False),
         Field('interests', 'date',default=None, required=False),
                
         Field('assistant_id', 'string', length=36,default=None, required=False), ## could this lead to a contact id?
         Field('social_links', 'date',default=None, required=False))

db.define_table('portfolios',
	Field('contacts__1contacts_ida', 'string', length=36,default=None, required=False),
	Field('contacts_nx_idb', 'string', length=36,default=None, required=False))
                
db.define_table('currencies',
	Field('name', 'string', length=36,default=None, required=False),
	Field('symbol', 'string', length=36,default=None, required=False),
	Field('iso4217', 'string', length=3,default=None, required=False),
	Field('conversion_rate', 'double',default= '0', required=False),
	Field('status', 'string', length=100,default=None, required=False),
	Field('currencies',default=None, required=False),
	Field('currency_code', 'string', length=255,default=None, required=False),
	Field('isin', 'string', length=255,default=None, required=False),
	Field('rolotec_id', 'string', length=255,default=None, required=False))
                
db.define_table('custom_fields',
	Field('bean_id', 'string', length=36,default=None, required=False),
	Field('set_num', 'integer',default= '0', required=False))

db.define_table('database_fundinfo',
	Field('rolotec_id', 'string', length=255,default=None, required=False),
	Field('history_date', 'date',default=None, required=False),
	Field('close_price', 'decimal(16,2)',default=None, required=False),
	Field('name', 'string', length=255,default=None, required=False),
	Field('isin', 'string', length=32,default=None, required=False),
	Field('document_type', 'string', length=4,default=None, required=False),
	Field('document_country', 'string', length=2,default=None, required=False),
	Field('document_language', 'string', length=2,default=None, required=False),
	Field('document_url', 'string', length=255,default=None, required=False),
	Field('document_idd', 'integer',default=None, required=False),
	Field('document_record_date', 'date',default=None, required=False),
	Field('document_modified_date', 'date',default=None, required=False),
	Field('document_constraint', 'string', length=3,default=None, required=False),
	Field('document_file', 'string', length=255,default=None, required=False),
	Field('document_node', 'string', length=255,default=None, required=False))
                
db.define_table('fdata_products',
	Field('name', 'string', length=255,default=None, required=False),
	Field('rolotec_id', 'string', length=255,default=None, required=False),
	Field('isin', 'string', length=32,default=None, required=False),
	Field('full_name', 'string', length=255,default=None, required=False),
	Field('short_name', 'string', length=255,default=None, required=False),
	Field('aum_size', 'string', length=64,default=None, required=False),
	Field('issuer_given_index', 'string', length=64,default=None, required=False),
	Field('issuing_size', 'string', length=64,default=None, required=False),
	Field('performance_chart_last_12_months', 'string', length=64,default=None, required=False),
	Field('average_daily_volume_chart_last_12_months', 'string', length=64,default=None, required=False))
### check these vs rolotec and vwd mapping tables                
db.define_table('documents',
	Field('description', 'date',default=None, required=False),
	Field('assigned_user_id', 'string', length=36,default=None, required=False),
	Field('rolotec_id', 'string', length=255,default=None, required=False),

	Field('parent_id', 'string', length=36,default=None, required=False),

	Field('data_type', 'string', length=100,default=None, required=False),
	
	Field('change_log', 'string', length=255,default=None, required=False),
	Field('document_id', 'string', length=36,default=None, required=False),
	Field('doc_id', 'string', length=100,default=None, required=False),
	Field('doc_type', 'string', length=100,default= 'Sugar', required=False),
	Field('doc_url', 'string', length=255,default=None, required=False),
   
	Field('filename', 'string', length=255,default=None, required=False),
	Field('file_ext', 'string', length=100,default=None, required=False),
	Field('file_mime_type', 'string', length=100,default=None, required=False),
	Field('revision', 'string', length=100,default=None, required=False),
	Field('deleted', 'integer',default= '0', required=False),

	Field('id', 'string', length=36,default=None, required=False),


	Field('active_date', 'date',default=None, required=False),
	Field('exp_date', 'date',default=None, required=False),
	Field('category_id', 'string', length=100,default=None, required=False),
	Field('subcategory_id', 'string', length=100,default=None, required=False),
	Field('status_id', 'string', length=100,default=None, required=False),
	Field('document_revision_id', 'string', length=36,default=None, required=False),
                
	Field('related_doc_id', 'string', length=36,default=None, required=False),
	Field('related_doc_rev_id', 'string', length=36,default=None, required=False),
	Field('is_template', 'integer',default= '0', required=False),
	Field('template_type', 'string', length=100,default=None, required=False))
               
db.define_table('crm_CustRelation',
	Field('source', 'string', length=36,default=None, required=False),
	Field('enclosure', 'string', length=1,default= ' ', required=False),
	Field('delimiter', 'string', length=1,default= '', required=False),
	Field('module', 'string', length=36,default=None, required=False),
	Field('content', 'date',default=None, required=False),
	Field('default_values', 'date',default=None, required=False),
	Field('has_header', 'integer',default= '1', required=False),

	Field('is_published', 'string', length=3,default= 'no', required=False),

	Field('status', 'string', length=20,default=None, required=False),

	Field('ie_timestamp', 'integer',default=None, required=False),

	Field('alias', 'string', length=255,default=None, required=False),
	Field('vqf', 'integer',default= '1', required=False),
	Field('bvv', 'integer',default= '0', required=False),
	Field('vsv', 'integer',default= '0', required=False),
	Field('bovv', 'integer',default= '0', required=False),
	Field('mifid2', 'integer',default= '0', required=False),
	Field('kubetype', 'string', length=100,default= 'privateindividual', required=False),
	Field('kubenp', 'string', length=100,default= 'other', required=False),
	Field('kubele', 'string', length=100,default= 'contractingparty', required=False),
	Field('amla_file_no', 'integer',default=None, required=False),
	Field('kbe_vqf_id_c', 'string', length=36,default=None, required=False),
	Field('kube_lang_other', 'string', length=255,default=None, required=False),
	Field('kube_sprache', 'date',default=None, required=False),
	Field('contract_date', 'date',default=None, required=False),
	Field('geschaeftsbez_aufnahme', 'date',default=None, required=False),
	Field('finma', 'integer',default= '0', required=False),
	Field('fma', 'integer',default= '0', required=False),
	Field('bafin', 'integer',default= '0', required=False),

	Field('employee_id_c', 'string', length=36,default=None, required=False),
	Field('client_currency', 'string', length=10,default=None, required=False),

	Field('contract_document', 'string', length=255,default=None, required=False))	

db.define_table('kreports',
	Field('report_module', 'string', length=25,default=None, required=False),
	Field('report_status', 'string', length=1,default=None, required=False),
	Field('union_modules', 'date',default=None, required=False),
	Field('reportoptions', 'date',default=None, required=False),
	Field('listtype', 'string', length=10,default=None, required=False),
	Field('listtypeproperties', 'date',default=None, required=False),
	Field('selectionlimit', 'string', length=25,default=None, required=False),
	Field('presentation_params', 'date',default=None, required=False),
	Field('visualization_params', 'date',default=None, required=False),
	Field('integration_params', 'date',default=None, required=False),
	Field('wheregroups', 'date',default=None, required=False),
	Field('whereconditions', 'date',default=None, required=False),
	Field('listfields', 'date',default=None, required=False),
	Field('unionlistfields', 'date',default=None, required=False),
	Field('advancedoptions', 'date',default=None, required=False))

db.define_table('leads', ## use same as contacts except less fields

	Field('converted', 'integer',default= '0', required=False),
	Field('refered_by', 'string', length=100,default=None, required=False),
	Field('lead_source', 'string', length=100,default=None, required=False),
	Field('lead_source_description', 'date',default=None, required=False),
	Field('status', 'string', length=100,default=None, required=False),
	Field('status_description', 'date',default=None, required=False),

	Field('opportunity_id', 'string', length=36,default=None, required=False),
	Field('campaign_id', 'string', length=36,default=None, required=False),

	Field('birthdate', 'date',default=None, required=False),
	Field('portal_name', 'string', length=255,default=None, required=False),
	Field('portal_app', 'string', length=255,default=None, required=False),
	Field('website', 'string', length=255,default=None, required=False),

	Field('middle_name', 'string', length=255,default=None, required=False))

db.define_table('fundinfo_docs',
	Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('fdata_vdf',
	Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('fdata_rolotec',
	Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('portf_mandate_bands',
	Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('portf_rulesets',
         Field('rule_type', 'string', length=255,default=None, required=False), ## ExcludedName,ExcludedSector,Percentage
         Field('rule_target', 'string', length=255,default=None, required=False), ## Names,Sectors,Perc_concentration,Perc_Absolute
         Field('monitor_freq', 'string', length=255,default=None, required=False), ## real,simulated,other
         Field('name', 'string', length=36,default=None, required=False))
                                
db.define_table('crm_tasks',
	Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('crm_meetings',
	Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('fdata_transactions',
         Field('name', 'string', length=36,default=None, required=False))
                
db.define_table('portf_portfolio',
         Field('portfolio_type', 'string', length=255,default=None, required=False), ## real,simulated,other
         Field('name', 'string', length=36,default=None, required=False))

db.define_table('portf_allocationModel',
         Field('website', 'string', length=255,default=None, required=False),
         Field('name', 'string', length=36,default=None, required=False))

db.define_table('comp_pii',
	Field('name', 'string', length=36,default=None, required=False))
db.define_table('rules_n_bands',
	Field('name', 'string', length=36,default=None, required=False))
db.define_table('portf_stamm_acct',
	Field('name', 'string', length=36,default=None, required=False))
db.define_table('portf_sub_acct',
	Field('name', 'string', length=36,default=None, required=False))
db.define_table('portf_depot_banks',
	Field('name', 'string', length=36,default=None, required=False))
db.define_table('portf_benchmarks',
	Field('name', 'string', length=36,default=None, required=False))
