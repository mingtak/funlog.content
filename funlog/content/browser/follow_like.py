from Products.Five.browser import BrowserView
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


class JoinFollowList(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            return
        catalog = self.context.portal_catalog
        ownerId = self.context.owner_info()["id"]
        current = api.user.get_current().getId()
        profileBrain = catalog({"Creator":current, "Type":"Profile"})[0]
        profile = profileBrain.getObject()
        if profileBrain.followList is None:
            profile.followList = [ownerId]
        elif ownerId not in profileBrain.followList:
            profile.followList.append(ownerId)
        profile.reindexObject(idxs=["followList"])
        response = self.request.response
        return response.redirect("./", lock=True)


class CancelFollowList(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            return
        catalog = self.context.portal_catalog
#        ownerId = self.context.getOwner().getId()
        ownerId = self.context.owner_info()["id"]
        current = api.user.get_current().getId()
        profile = catalog({"Creator":current, "Type":"Profile"})[0].getObject()
        if ownerId in profile.followList:
            profile.followList.remove(ownerId)
            profile.reindexObject(idxs=["followList"])
        response = self.request.response
        return response.redirect("./", lock=True)


class GetFollowMe(BrowserView):

    def __call__(self):
        catalog = self.context.portal_catalog
        ownerId = self.context.owner_info()["id"]
#        currentId = api.user.get_current().id
        brain = catalog(followList=ownerId)
#        self.checkInList = bool(len(catalog(followList=currentId)))
        if len(brain) == 0:
            return None
#        shuffle(brain)
        return brain
