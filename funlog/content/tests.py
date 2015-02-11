import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import funlog.content

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['funlog.content'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              funlog.content)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='funlog.content',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='funlog.content.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for Theme
        ztc.ZopeDocFileSuite(
            'Theme.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Profile
        ztc.ZopeDocFileSuite(
            'Profile.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for SiteFolder
        ztc.ZopeDocFileSuite(
            'SiteFolder.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Travel
        ztc.ZopeDocFileSuite(
            'Travel.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Article
        ztc.ZopeDocFileSuite(
            'Article.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Album
        ztc.ZopeDocFileSuite(
            'Album.txt',
            package='funlog.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
