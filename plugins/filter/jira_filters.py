"""java filters."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError
import re


def jira_markup2html(jira_markup):
    jira_markup = re.sub("{{", "<code>", jira_markup)
    jira_markup = re.sub("}}", "</code>", jira_markup)
    jira_markup = re.sub("\(/\)",
                         "<ac:emoticon ac:name=\"tick\" />",
                         jira_markup)
    jira_markup = re.sub(
        pattern="\*(\S.*?\S)\*",
        repl='<strong>\\1</strong>',
        string=jira_markup
    )
    jira_markup = re.sub(
        pattern="\(!\)",
        repl='<ac:emoticon ac:name="warning" />',
        string=jira_markup
    )
    jira_markup = re.sub(
        pattern="\(on\)",
        repl='<ac:emoticon ac:name="light-on" />',
        string=jira_markup
    )
    jira_markup = re.sub(
        pattern="\(\?\)",
        repl='<ac:emoticon ac:name="question" />',
        string=jira_markup
    )
    jira_markup = re.sub(
        pattern="{color:(\#\S{6})}(.*?){color}",
        repl='<span style="color: \\1">\\2</span>',
        string=jira_markup
    )
    jira_markup = re.sub(
        pattern="\[(.*?)\|(.*?)\]",
        repl='<a href="\\2">\\1</a>',
        string=jira_markup
    )
    return jira_markup


class FilterModule(object):
    """java filters."""

    def filters(self):
        return {
            'jira_markup2html': jira_markup2html
        }
