#
# Test our OrderSupport implementation
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase


class TestOrderSupport(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        # Get rid of the .personal subfolder
        membership = self.portal.portal_membership
        self.folder._delObject(membership.personal_id)
        # Add a bunch of subobjects we can order later on
        self.folder.invokeFactory('Document', id='foo')
        self.folder.invokeFactory('Document', id='bar')
        self.folder.invokeFactory('Document', id='baz')

    def testGetObjectPosition(self):
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObject(self):
        self.folder.moveObjectToPosition('foo', 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectToSamePos(self):
        self.folder.moveObjectToPosition('bar', 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectToFirstPos(self):
        self.folder.moveObjectToPosition('bar', 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectToLastPos(self):
        self.folder.moveObjectToPosition('bar', 2)
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveObjectOutLowerBounds(self):
        # Pos will be normalized to 0
        self.folder.moveObjectToPosition('bar', -1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectOutUpperBounds(self):
        # Pos will be normalized to 2
        self.folder.moveObjectToPosition('bar', 3)
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveObjectsUp(self):
        self.folder.moveObjectsUp(['bar'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectsDown(self):
        self.folder.moveObjectsDown(['bar'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveObjectsToTop(self):
        self.folder.moveObjectsToTop(['bar'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectsToBottom(self):
        self.folder.moveObjectsToBottom(['bar'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveTwoObjectsUp(self):
        self.folder.moveObjectsUp(['bar', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testMoveTwoObjectsDown(self):
        self.folder.moveObjectsDown(['foo', 'bar'])
        self.assertEqual(self.folder.getObjectPosition('baz'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveTwoObjectsToTop(self):
        self.folder.moveObjectsToTop(['bar', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testMoveTwoObjectsToBottom(self):
        self.folder.moveObjectsToBottom(['foo', 'bar'])
        self.assertEqual(self.folder.getObjectPosition('baz'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testRenameObject(self):
        # Renaming should not change position
        get_transaction().commit(1) # make rename work
        self.folder.manage_renameObjects(['bar'], ['barney'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('barney'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testRenameFirstObject(self):
        # Renaming should not change position
        get_transaction().commit(1) # make rename work
        self.folder.manage_renameObjects(['foo'], ['flintstone'])
        self.assertEqual(self.folder.getObjectPosition('flintstone'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testRenameLastObject(self):
        # Renaming should not change position
        get_transaction().commit(1) # make rename work
        self.folder.manage_renameObjects(['baz'], ['bedrock'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.assertEqual(self.folder.getObjectPosition('bedrock'), 2)

    def testOrderObjects(self):
        self.folder.orderObjects('id')
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def DISABLED_test_manage_move_objects_up(self):
        # Make sure ZMI method works
        self.folder.manage_move_objects_up(self.app.REQUEST, ids=['bar'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def DISABLED_test_manage_move_objects_down(self):
        # Make sure ZMI method works
        self.folder.manage_move_objects_down(self.app.REQUEST, ids=['bar'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def DISABLED_test_manage_move_objects_to_top(self):
        # Make sure ZMI method works
        self.folder.manage_move_objects_to_top(self.app.REQUEST, ids=['bar'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def DISABLED_test_manage_move_objects_to_bottom(self):
        # Make sure ZMI method works
        self.folder.manage_move_objects_to_bottom(self.app.REQUEST, ids=['bar'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testSubsetIds(self):
        self.folder.moveObjectsByDelta(['baz'], -1, ['foo', 'bar', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testSkipObjectsNotInSubsetIds(self):
        self.folder.moveObjectsByDelta(['baz'], -1, ['foo', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('baz'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1) # Did not move
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testIgnoreNonObjects(self):
        #Fix for (http://plone.org/collector/3959) non contentish objects
        #cause errors, we should just ignore them
        self.folder.moveObjectsByDelta(['bar','blah'], -1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveCMFObjectsOnly(self):
        # Plone speciality
        self.folder.manage_addProduct['OFSP'].manage_addDTMLMethod('wilma', file='')
        self.folder.moveObject('wilma', 2)
        # Non-CMF object should keep position
        self.folder.moveObjectToPosition('foo', 2)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('wilma'), 2) # Did not move
        self.assertEqual(self.folder.getObjectPosition('foo'), 3)

    def testMoveUpCMFObjectsOnly(self):
        # Plone speciality
        self.folder.manage_addProduct['OFSP'].manage_addDTMLMethod('wilma', file='')
        self.folder.moveObject('wilma', 2)
        # Non-CMF object should keep position
        self.folder.moveObjectsUp(['baz'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('wilma'), 2) # Did not move
        self.assertEqual(self.folder.getObjectPosition('bar'), 3)


class TestOrderSupportInPortal(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.setRoles(['Manager'])
        # Add a bunch of subobjects we can order later on
        self.portal.invokeFactory('Document', id='foo')
        self.portal.invokeFactory('Document', id='bar')
        self.portal.invokeFactory('Document', id='baz')
        # Move them to the top
        self.portal.moveObjectsByDelta(ids=['foo', 'bar', 'baz'],
                                       delta=-len(self.portal._objects),
                                       subset_ids=self.portal.objectIds())

    def testRenameObject(self):
        # Renaming should not change position
        get_transaction().commit(1) # make rename work
        self.portal.manage_renameObjects(['bar'], ['barney'])
        self.assertEqual(self.portal.getObjectPosition('foo'), 0)
        self.assertEqual(self.portal.getObjectPosition('barney'), 1)
        self.assertEqual(self.portal.getObjectPosition('baz'), 2)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderSupport))
    suite.addTest(makeSuite(TestOrderSupportInPortal))
    return suite

if __name__ == '__main__':
    framework()
