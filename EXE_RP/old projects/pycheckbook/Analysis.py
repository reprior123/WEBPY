#!/usr/bin/python

import Checkbook
import Date

def analysis(checks, month):
    spendings = earnings = 0
    for check in checks:
        if check.date.month == month:
            if check.amount > 0:
                earnings = earnings + check.amount
            else:
                spendings = spendings + check.amount
    return (earnings, spendings)

def print_analysis(data):
    print "In:           $%.2f" % data[0]
    print "Out:          $%.2f" % abs(data[1])
    net = data[0] + data[1]
    sign = ' '
    if net < 0:
        sign = '-'
    net = abs(net)
    print "Net:         %s$%.2f" % (sign, net)

cb = Checkbook.Checkbook('/home/shaleh/.bofa.qif')
today = Date.Date()
three_months = [0,0]

print "Analysis:"

output = analysis(cb.checks, today.month)
print "            Current month"
print_analysis(output)
three_months[0] = output[0]
three_months[1] = output[1]

print ''

output = analysis(cb.checks, today.month - 1)
three_months[0] = three_months[0] + output[0]
three_months[1] = three_months[1] + output[1]

print "            Last 3 months"
output = analysis(cb.checks, today.month - 2)
three_months[0] = three_months[0] + output[0]
three_months[1] = three_months[1] + output[1]
print_analysis(three_months)
