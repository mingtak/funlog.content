from five import grok
from zope.interface import Interface
from plone import api
#from funlog.content import MessageFactory as _


class FollowMe(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("followMe")

    def update(self):
        if api.user.is_anonymous():
            return
        catalog = self.context.portal_catalog
        ownerId = self.context.owner_info()["id"]
        currentUserId = api.user.get_current().getId()
        currentProfileBrain = catalog({"Creator":currentUserId, "Type":"Profile"})[0]
        profile = currentProfileBrain.getObject()
        try:
            if currentProfileBrain.followList is None:
                profile.followList = [ownerId]
                profile.reindexObject(idxs=["followList"])
                return
            elif ownerId not in currentProfileBrain.followList:
                profile.followList.append(ownerId)
                profile.reindexObject(idxs=["followList"])
                return
            if ownerId in currentProfileBrain.followList:
                profile.followList.remove(ownerId)
                profile.reindexObject(idxs=["followList"])
        except:
            profile.reindexObject(idxs=["followList"])
        return

    def render(self):
        response = self.request.response
        response.redirect("./", lock=True)
        return


class GetFollowMe(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("getFollowMe")

    def update(self):
        catalog = self.context.portal_catalog
        ownerId = self.context.owner_info()["id"]
        self.brain = catalog(followList=ownerId)
        if len(self.brain) == 0:
            return None
        return

    def render(self):
        return self.brain
