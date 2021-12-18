#!/usr/bin/python

from ansible.module_utils.basic import *
from datetime import datetime


def log(data):
    return comments(data)


def comment_created_day(comment):
    cmt_created = comment['created'].strftime("%Y-%m-%d")
    return datetime.strptime(cmt_created, "%Y-%m-%d")


# Comment made in sprint?
def sprint_comment(data, comment):
    cmt_created = comment_created_day(comment)
    start = datetime.strptime(data['sprint']['start'], "%Y-%m-%d")
    end = datetime.strptime(data['sprint']['end'], "%Y-%m-%d")
    return start <= cmt_created <= end


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
                   "summary": issue['fields']['summary']}
            if sprint_comment(data, cmt):
                cmts.append(cmt)
    return sorted(cmts, key=lambda issue: issue['created'])


def main():
    fields = {"issues": {"required": True, "type": "list"},
              "sprint": {"required": True, "type": "dict"}}
    module = AnsibleModule(argument_spec=fields)
    cmts = log(module.params)
    module.exit_json(changed=False, comments=cmts)


if __name__ == '__main__':
    main()
