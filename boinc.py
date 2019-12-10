import locale
import subprocess
from datetime import datetime
import re

projects = None

def normalize(data: str) -> [str]:
    data = data.strip().split('\n')
    return '\n'.join(re.sub(r'^[ ]+', '', line[3:]) for line in data).split('\n-----------\n')[1:]


def parse(data: str) -> [dict]:
    data = normalize(data)
    r = []
    for d in data:
        dic = {}
        for e in d.split('\n'):
            if e == '':
                break
            f = e.split(': ')
            dic[f[0]] = f[1]

        r.append(dic)

    return r


def get_project(proj_url: str) -> dict:
    global projects
    if projects is None:
        projects = parse(subprocess.run(['boinccmd', '--get_project_status'], capture_output=True, check=True, text=True).stdout)

    for project in projects:
        if proj_url == project['master URL']:
            return project

    return None


def parse_remaining_time(seconds: float) -> str:
    hours = seconds / 3600
    minutes = (hours - int(hours)) * 60
    hours = int(hours)
    seconds = int((minutes - int(minutes)) * 60)
    minutes = int(minutes)

    s = ''

    if hours > 0:
        s = '%dh' % hours
    if minutes > 0:
        s = ''.join([s, '%s%dmin' % ('0' if hours > 0 and minutes < 10 else '', minutes)])
    if seconds > 0 and hours == 0:
        s = ''.join([s, '%s%ds' % ('0' if minutes > 0 and seconds < 10 else '', seconds)])

    return s


def get_output(data: [dict]) -> str:
    text = ''

    for task in data:
        line = ''

        if task['scheduler state'] not in ['preempted', 'scheduled']:
            continue

        locale.setlocale(locale.LC_ALL, 'C')
        date = datetime.strptime(task['report deadline'], '%c')

        locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

        line = ' '.join([line,
                         '|>' if task['active_task_state'] == 'EXECUTING' else '||',
                         get_project(task['project URL'])['name'],
                         'pour le %s' % date.strftime('%d %b'),
                         '(reste %s)' % parse_remaining_time(float(task['estimated CPU time remaining']))
                        ])
        text = '\n'.join([text, line])

    return text


print(get_output(parse(subprocess.run(['boinccmd', '--get_tasks'],
                                      capture_output=True,
                                      check=True,
                                      text=True).stdout)))
