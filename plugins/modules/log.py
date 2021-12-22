#!/usr/bin/python

from ansible.module_utils.basic import *
from datetime import datetime
from datetime import timedelta


def log(data):
    return days(data)


# Comment created without time
def comment_created_day(comment):
    crtd = datetime.strptime(comment['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    return datetime.strptime(crtd.strftime("%Y-%m-%d"), "%Y-%m-%d")


# Comment made in sprint?
def sprint_comment(data, comment, comment_created):
    start = datetime.strptime(data['sprint']['start'], "%Y-%m-%d")
    end = datetime.strptime(data['sprint']['end'], "%Y-%m-%d")
    return start <= comment_created <= end


def comments(data):
    cmts = []
    for issue in data['issues']:
        for comment in issue['fields']['comment']['comments']:
            crtd = datetime.strptime(comment['created'],
                                     '%Y-%m-%dT%H:%M:%S.%f%z')
            cmt = {"author": comment['author']['key'],
                   "created": crtd,
                   "body": comment['body'],
                   "issue": issue['key'],
                   "id": comment['id'],
                   "summary": issue['fields']['summary']}
            cmt_created = comment_created_day(comment)
            cmt['created-day'] = cmt_created.strftime("%Y-%m-%d")
            if sprint_comment(data, cmt, cmt_created):
                cmts.append(cmt)
    return sorted(cmts, key=lambda issue: issue['created'])


def days(data):
    sdays = {}
    cmts = comments(data)
    start = datetime.strptime(data['sprint']['start'], "%Y-%m-%d")
    end = datetime.strptime(data['sprint']['end'], "%Y-%m-%d")
    delta = end - start   # returns timedelta
    for i in range(delta.days + 1):
        day = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        cmts2 = [item for item in cmts if item['created-day'] == day]
        # cmts2 = [item for item in cmts]
        sdays[day] = cmts2
    return sdays


def main():
    fields = {"issues": {"required": True, "type": "list"},
              "sprint": {"required": True, "type": "dict"}}
    module = AnsibleModule(argument_spec=fields)
    cmts = log(module.params)
    module.exit_json(changed=False, days=cmts)


if __name__ == '__main__':
    main()
