#!/usr/bin/python
# -*- coding: utf-8 -*-

# Skip List is sorted multiple layer linked list.

# Ref:
# http://videolectures.net/mit6046jf05_demaine_lec12/
# http://blog.nosqlfan.com/html/3041.html

# Search is from left -> right, top level -> bottom

# k = 元素参与的层数，由随机函数决定

from random import randint, seed

class SkipNode:
    """A node from a skip list"""
    def __init__(self, height = 0, elem = None):
        self.elem = elem
        self.level = [None] * height   #TODO: what is this data type ?

class SkipList:

    def __init__(self):
        self.head = SkipNode()
        self.len = 0
        self.maxHeight = 0

    def __len__(self):
        return self.len

    # Return element
    def find(self, elem, update = None):
        if update == None:
            update = self.updateList(elem)
        if len(update) > 0:
            candidate = update[0].level[0]
            if candidate != None and candidate.elem == elem:
                return candidate
        return None

    # Boolean
    def contains(self, elem, update = None):
        return self.find(elem, update) != None

    # Get k value
    def randomHeight(self):
        height = 1
        while randint(1, 2) != 1:
            height += 1
        return height

    # It returns a list of nodes in each level that contains
    # the greatest value that is smaller than elem.
    def updateList(self, elem):
        update = [None] * self.maxHeight
        x = self.head
        for i in reversed(range(self.maxHeight)):
            while x.level[i] != None and x.level[i].elem < elem:
                x = x.level[i]
            update[i] = x
        return update


    def insert(self, elem):
        node = SkipNode(self.randomHeight(), elem)
        # Max height for Skip list
        self.maxHeight = max(self.maxHeight, len(node.level))

        while len(self.head.level) < len(node.level):
            self.head.level.append(None)

        update = self.updateList(elem)
        if self.find(elem, update) == None:
            for i in range(len(node.level)):
                node.level[i] = update[i].level[i]
                update[i].level[i] = node
            self.len += 1

    def remove(self, elem):
        update = self.updateList(elem)
        x = self.find(elem, update)
        if x != None:
            for i in reversed(range(len(x.level))):
                update[i].level[i] = x.level[i]
                if self.head.level[i] == None:
                    self.maxHeight -= 1
            self.len -= 1

    def printList(self):
        for i in range(len(self.head.level)-1, -1, -1):
            x = self.head
            while x.level[i] != None:
                print x.level[i].elem,
                x = x.level[i]
            print ''