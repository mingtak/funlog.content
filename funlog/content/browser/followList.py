from Products.Five.browser import BrowserView
from plone import api


class IsAnonymous(BrowserView):

    def __call__(self):
        return api.user.is_anonymous()

class JoinFollowList(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            return
        catalog = self.context.portal_catalog
        ownerId = self.context.getOwner().getId()
        current = api.user.get_current().getId()
        profile = catalog({"Creator":current, "Type":"Profile"})[0].getObject()
        if ownerId in profile.followList:
            return
        profile.followList.append(ownerId)
        profile.reindexObject(idxs=["followList"])


class CancelFollowList(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            return
        catalog = self.context.portal_catalog
        ownerId = self.context.getOwner().getId()
        current = api.user.get_current().getId()
        profile = catalog({"Creator":current, "Type":"Profile"})[0].getObject()
        if ownerId in profile.followList:
            profile.followList.remove(ownerId)
            profile.reindexObject(idxs=["followList"])


class GetFollowMe(BrowserView):

    def __call__(self):
        catalog = self.context.portal_catalog
        ownerId = self.context.getOwner().getId()
        brain = catalog(followList=ownerId)
        if len(brain) == 0:
            return None
        followList = []
        for item in brain:
            followList.append(item.Creator)
        return list(set(followList))
