#!/usr/bin/env python

import spark
from helper import getValue

device = 'htb0'

root_setup = """#
#
# "%s":
tc qdisc add dev %s root handle %s: htb
tc class add dev %s parent %s classid %s htb rate %skbit ceil %skbit"""

class_setup = """
#
# Client "%s":
tc class add dev %s parent %s classid %s htb rate %skbit ceil %skbit"""


class Interpret(spark.GenericASTTraversal):
    def __init__(self, ast):
        spark.GenericASTTraversal.__init__(self, ast)
        self.postorder()

    def n_root(self, node):
        # generate code:
        handle = node.classid.attr.split(':')[0]
        node.code = root_setup % (
            getValue(node, 'descr'),
            device,
            handle,
            device,
            '%s:%s' % (handle, 0),
            node.classid,
            getValue(node, 'rate'),
            getValue(node, 'ceil') or getValue(node, 'rate')

        )

    def n_classdef(self, node):
        # generate code:
        node.code = class_setup % (
            getValue(node, 'descr'),
            device,
            node.parent,
            node.classid,
            getValue(node, 'rate'),
            getValue(node, 'ceil') or getValue(node, 'rate')
        )

    def default(self, node):
        # "default" will be called for all
        # unmentioned nodes.
        # In our case -- for "classdefs",
        # which contain other classes.

        # generate code:
        node.code = '\n'.join([ x.code for x in node.kids ])

