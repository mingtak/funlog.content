from five import grok
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
#from random import shuffle
from DateTime import DateTime


class IsAnonymous(BrowserView):

    def __call__(self):
        return api.user.is_anonymous()


class GetCurrentUser(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            return "guest"
        return api.user.get_current()


class GetLikeList(BrowserView):
    """ for search hotest page at lastest 30 days """
    def __call__(self):
        catalog = self.context.portal_catalog
        today = DateTime()
        brain = catalog({"Type":["Article", "Travel"],
                         "created":{'query':(today-30),
                                    'range': 'min'}
                        },
                        sort_on="likeItCount", sort_order="reverse")
        return brain


class SetLikeList(BrowserView):
    """ for search hotest page """
    def __call__(self):
        context = self.context
        currentId = api.user.get_current().getId()
        context.likeItList.append(currentId)
        context.reindexObject(idxs=["likeItCount", "likeItList"])
        return
