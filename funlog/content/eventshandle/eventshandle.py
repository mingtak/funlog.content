from plone import api
from Products.CMFPlone.utils import safe_unicode


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
        api.content.transition(obj=folder, transition='publish')
        folder.exclude_from_nav = True
#        import pdb; pdb.set_trace()
#        folder.setConstrainTypesMode(1)
#        folder.setLocallyAllowedTypes(['Album'])
        folder.reindexObject()

#        folder.manage_setLocalRoles(userId, rolesList)
#        folder.reindexObjectSecurity()

