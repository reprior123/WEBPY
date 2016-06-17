
import sys, re, os, string
from pprint import pprint

# Required for Rally
import requests
from pyral import Rally, rallySettings

# Required for Perforce
from P4 import P4,P4Exception

# Initialise Perforce
p4 = P4()
p4.user = 'Tristan.Gaffney'
p4.client = 'Tristan.Gaffney.vc7.Main.LDNRS010'
p4.exception_level = 2

#Initialise Rally
from pyral import Rally, rallySettings
options = []
server, user, password, workspace, project = rallySettings(options)
user = "robot@actant.com"
password = "SingSing"
rally = Rally(server, user, password, workspace=workspace, project=project)
rally.enableLogging('mypyral.log')

def extractChangeLists( startChangelist, endChangelist ):
    try:
            start = "3.71.3.130"
            end = "3.71.3.140"

            p4.connect()
            completed = {}
            contributions = {}


            allInMain = p4.run("changes", "-ssubmitted","//AQTOR3/Working/Main/...")

#['AcceptedDate', 'AffectedCustomer', 'AffectedCustomers', 'AffectsDoc', 'AnalysisStatement', 'Attachments', 'Blocked', 'Blocker', 'Build', 'ChangeDescription', 'Changesets',
#'ClosedDate', 'CreationDate', 'Description', 'Discussion', 'Duplicates', 'EngineeringSupport', 'Environment', 'Exchange', 'ExecutionVendor', 'FixedInBuild', 'FormattedID', 'FoundInBuild',
#'FoundinBuildNumber', 'FoundinRelease', 'InProgressDate', 'IncidentReport', 'Iteration', 'KanbanState', 'LastUpdateDate', 'Linktodefectfolder', 'LocalAttachments', 'MKSLink',
#'MKSid', 'Name', 'Notes', 'NumberofCases', 'ObjectID', 'OpenedDate', 'Origin', 'OriginEpicRallyId', 'OriginatingExchange', 'Owner', 'Package', 'PlanEstimate', 'PriceFeedVendor',
#'Priority', 'Project', 'Rank', 'Reason', 'Recycled', 'Release', 'ReleaseNote', 'RequestedRelease', 'Requirement', 'Resolution', 'RevisionHistory', 'SalesforceCase', 'SalesforceCaseID',
#'SalesforceCaseNumber', 'SalesforceCreationDate', 'ScheduleState', 'ServiceDesk', 'Severity', 'State', 'SubmittedBy', 'Subscription', 'Tags', 'TargetBuild', 'TargetDate', 'TaskActualTotal',
#'TaskEstimateTotal', 'TaskRemainingTotal', 'TaskStatus', 'Tasks', 'TestCase', 'TestCaseResult', 'TestCaseStatus', 'TestCases', 'TouchedIn', 'Value', 'ValueCcy', 'ValueRisk', 'VerifiedInBuild',
#'Workspace', '_CreatedAt', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattr__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__',
#'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_context', '_hydrated', '_ref', '_type', 'attributes', 'oid']

            for changelist in allInMain:

                    change = int(changelist['change'])
                    if change >= startChangelist and change <= endChangelist:
#                        print changelist['change'], changelist['user']

                        info = p4.run("fixes",'-c' + changelist['change'])
                        for value in info:

                            if value['Job'][0:2] == "DE":
                                query_criteria = 'FormattedID = "%s"' % value['Job']

                                response = rally.get('Defect', fetch=True, query=query_criteria)
                                if response.errors:
                                    sys.stdout.write("\n".join(response.errors))
                                    sys.exit(1)

                                for defect in response:
                                    Customers = "Internal" if defect.AffectedCustomers == "" else defect.AffectedCustomers
                                    if defect.State != "Submitted" and defect.State != "Open":
                                        defect.Name = string.replace(defect.Name,"&apos;", "'")
                                        completed[ defect.FormattedID ] = '%s;%s;%s' % (defect.FormattedID, Customers, defect.Name)
                                    else:
                                        contributions[ defect.FormattedID ] = '%s;%s;%s' % (defect.FormattedID, Customers, defect.Name)

                            if value['Job'][0:2] == "US":
                                query_criteria = 'FormattedID = "%s"' % value['Job']

                                response = rally.get('UserStory', fetch=True, query=query_criteria)
                                if response.errors:
                                    sys.stdout.write("\n".join(response.errors))
                                    sys.exit(1)

                                for story in response:
                                    if story.ScheduleState == "Accepted":
                                        completed[ story.FormattedID ] = '%s;%s' % (story.FormattedID, story.Name)
                                    else:
                                        contributions[ story.FormattedID ] = '%s;%s' % (story.FormattedID, story.Name)

            p4.disconnect()

            print '------------------------------------------------'
            print 'COMPLETED'
            for value in completed.values():
                print value
            print '------------------------------------------------'
            print 'CONTRIBUTIONS'
            for value in contributions.values():
                print value
            print '------------------------------------------------'

    except P4Exception:
            print 'EXCEPTION'
            for e in p4.errors:                                     # Display errors
                    print e

def printUsage():
    print 'Interrogate Rally.py start-change-list end-change-list'
    print '   start-change-list'
    print '   end-change-list'

if __name__ == "__main__":
    print 'ARGS:', sys.argv
    if len(sys.argv) == 3:
        startChangelist = int(sys.argv[1])
        endChangelist = int(sys.argv[2])
        extractChangeLists( startChangelist, endChangelist )
    else:
        printUsage()
