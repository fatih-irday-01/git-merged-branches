#!/usr/bin/python
import os
import sys
from datetime import datetime

try:
    from prettytable import PrettyTable, ALL
except:
    os.system('python3 -m pip install -U prettytable')
    from prettytable import PrettyTable, ALL

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bgcolor(text, status):
    return status + text + bcolors.ENDC

# os.system("git fetch -qp")
data = os.popen('git ls-remote | grep -v "tags\|HEAD\|From\|/master\|/test\|dev\|release"')
data = data.read()
data = data.splitlines()

args = sys.argv[1::]
remoteBranchToCheck = 'origin/master'
if '-b' in args:
    branchSelect = args.index('-b') + 1
    remoteBranchToCheck = 'origin/' + str(args[branchSelect])

userSelect = None
if '-u' in args:
    userSelect = args.index('-u') + 1
    userSelect = str(args[userSelect])

branchAuthorsData = os.popen('git for-each-ref --format="%(refname:strip=3)---%(authorname)---%(committer)" --sort=authordate refs/remotes')
branchAuthorsData = branchAuthorsData.read().strip().splitlines()

branchAuthors = {}
branchDateTimes = {}
users = {}
for item in branchAuthorsData:
    breach, user, time = item.split('---')
    users[user] = None
    branchAuthors[breach] = user
    branchDateTimes[breach] = datetime.fromtimestamp(int(time.split(' ')[-2])).strftime("%Y-%m-%d")

colors = []
for i in list(range(91,99)) + list(range(31,37)):
    colors.append('\033['+str(i)+'m')

colorCount = len(colors)

for key, item in enumerate(users):
    if key >= colorCount:
        key = key % colorCount
    users[item] = colors[key] + item + '\033[0m'


table = PrettyTable([bgcolor("User", bcolors.OKGREEN), bgcolor('Commant', bcolors.OKGREEN), bgcolor('Last Update', bcolors.OKGREEN)])
# table.hrules=ALL
table.align='l'
table.valign='t'
lines = False

for item in data:
    commitHash, branchName = item.split('refs/heads/')
    result = os.popen("git branch -r --contains "+commitHash+" | grep '"+remoteBranchToCheck+"$' | grep -vi 'head'").read()
    isMergedIntoBranch = result.strip() == remoteBranchToCheck
    if isMergedIntoBranch:
        author = '??'
        if(branchName in branchAuthors):
            author = branchAuthors[branchName]

        branchDateTime = '??'
        if(branchName in branchDateTimes):
            branchDateTime = branchDateTimes[branchName]

        if(userSelect is not None and userSelect != author):
            continue

        if author in users:
            author = users[author]

        table.add_row([
            author,
            'git push origin --delete '+branchName,
            branchDateTime
        ])

        lines = True

if lines:
    print(table)
else:
    print(bgcolor('No Records Found', bcolors.WARNING))
