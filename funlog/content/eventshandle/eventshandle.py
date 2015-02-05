from plone import api
from Products.CMFPlone.utils import safe_unicode


def transitionState(item, event):
    """ TODO """


def excludeFromNav_True(item, event):
    item.exclude_from_nav = True
    item.reindexObject(idxs=["exclude_from_nav"])


def checkRoles(event):
    portal = api.portal.get()
    container = portal
    user = event.object
    if user is None:
        return
    userId = user.getId()
    user = api.user.get(userid=userId)
    userRoles = user.getRoles()
    username = safe_unicode(user.getProperty('fullname'))
    folderPath = "/%s" % userId
    folder = api.content.get(path=folderPath)

    if folder is not None:
        return

    with api.env.adopt_roles(['Manager']):
        folder = api.content.create(container=container, type="Folder", id=userId, title=username)
#        api.content.transition(obj=folder, transition='publish')
#        folder.reindexObject(idxs=["review_state"])
