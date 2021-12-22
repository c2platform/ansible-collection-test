#!/usr/bin/python

from ansible.module_utils.basic import *
from atlassian import Confluence


def connection(data):
    return Confluence(
        url=data['url'],
        username=data['username'],
        password=data['password'])


def get_body(data):
    f = open(data['body'], "r")
    return f.read()


def page_year(confluence, data):
    page = confluence.get_page_by_title(space=data['space'],
                                        title=data['sprint']['year'])
    return page


def page_update(confluence, data):
    page = confluence.get_page_by_title(space=data['space'],
                                        title=data['title'])
    status = confluence.update_page(page_id=page['id'],
                                    title=data['title'],
                                    body=get_body(data))
    return status


def page_create(confluence, data, year):
    status = confluence.create_page(
        space=data['space'],
        title=data['title'],
        parent_id=year['id'],
        type='page',
        representation='storage',
        editor='v2',
        body=get_body(data))
    return status


def page(data):
    confluence = connection(data)
    year = page_year(confluence, data)
    if confluence.page_exists(data['space'], data['title']):
        status = page_update(confluence, data)
    else:
        status = page_create(confluence, data, year)
    page = confluence.get_page_by_title(space=data['space'],
                                        title=data['title'])
    confluence.set_page_label(page['id'], 'sprint-log')
    return year, status


def main():
    fields = {"url": {"required": True, "type": "str"},
              "username": {"required": True, "type": "str"},
              "password": {"required": True, "type": "str", "no_log": True},
              "space": {"required": True, "type": "str"},
              "title": {"required": True, "type": "str"},
              "sprint": {"required": True, "type": "dict"},
              "body": {"required": True, "type": "str"}}
    module = AnsibleModule(argument_spec=fields)
    pg = page(module.params)
    module.exit_json(changed=False, results=pg)


if __name__ == '__main__':
    main()
