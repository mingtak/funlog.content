from five import grok
from plone import api
from Products.CMFPlone.utils import safe_unicode

from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent, IObjectAddedEvent, IObjectModifiedEvent
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from zope.app.container.interfaces import IObjectAddedEvent

from plone.app.contenttypes.interfaces import IFolder, IImage, IDocument
from funlog.content.album import IAlbum
from funlog.content.article import IArticle
from funlog.content.travel import ITravel
from funlog.content.profile import IProfile
from funlog.content.theme import ITheme


@grok.subscribe(ITravel, IObjectAddedEvent)
def addedTravel(item, event):
    parentNode = item.getParentNode()
    current = api.user.get_current()
    api.user.grant_roles(user=current,
        roles=['Contributor'],
        obj=item
    )
    redirectUrl = "%s/%s" % (parentNode[item.id].absolute_url(), "edit")
    response = item.REQUEST.response
    response.redirect(redirectUrl, lock=True)


@grok.subscribe(IFolder, IBeforeTransitionEvent)
def transitionState(item, event):
    """ TODO """


@grok.subscribe(IFolder, IObjectCreatedEvent)
@grok.subscribe(IImage, IObjectCreatedEvent)
@grok.subscribe(IDocument, IObjectCreatedEvent)
@grok.subscribe(IAlbum, IObjectCreatedEvent)
@grok.subscribe(IArticle, IObjectCreatedEvent)
@grok.subscribe(ITravel, IObjectCreatedEvent)
@grok.subscribe(IProfile, IObjectCreatedEvent)
@grok.subscribe(ITheme, IObjectCreatedEvent)
def excludeFromNav_True(item, event):
    item.exclude_from_nav = True


@grok.subscribe(UserInitialLoginInEvent)
def checkRoles(event):
    portal = api.portal.get()
    blogRoot = portal['blog']
    profileRoot = portal['profile']
    user = event.object
    if user is None:
        return
    userId = user.getId()
    user = api.user.get(userid=userId)
    userRoles = user.getRoles()
    username = safe_unicode(user.getProperty('fullname'))

    if hasattr(blogRoot, userId):
        return

    with api.env.adopt_roles(['Manager']):
        funlog = api.content.create(container=blogRoot, type="Folder", id=userId, title=username)
        profile = api.content.create(container=profileRoot, type="funlog.content.profile", id=userId, title=username)
        profile.blogId = userId
        profile.blogName = username
        profile.reindexObject(idxs=["blogId", "blogName"])


@grok.subscribe(IAlbum, IObjectAddedEvent)
@grok.subscribe(IArticle, IObjectAddedEvent)
@grok.subscribe(ITravel, IObjectAddedEvent)
def moveContentToTop(obj, event):
   """
   Moves Items to the top of its folder
   """
   folder = obj.getParentNode()
   if folder != None:
       folder.moveObjectsToTop(obj.id)

@grok.subscribe(IProfile, IObjectModifiedEvent)
@grok.subscribe(IFolder, IObjectModifiedEvent)
def syncBolgTitle_Description(obj, event):
    userId = obj.getOwner().getId()
    catalog = obj.portal_catalog
    if obj.Type() == "Profile":
       otherObj = catalog({"Creator":userId, "Type":"Folder"})[0].getObject()
       objId, objTitle, objDescription = obj.blogId, obj.blogName, obj.blogDescription
       otherObjId, otherObjTitle, otherObjDescription = otherObj.id, otherObj.title, otherObj.description
       if objId != otherObjId:
           with api.env.adopt_roles(['Manager']):
                api.content.rename(obj=otherObj, new_id=str(objId))
       if objTitle != otherObjTitle:
           otherObj.title = objTitle
       if objDescription != otherObjDescription:
           otherObj.description = objDescription
       otherObj.reindexObject(idxs=["id", "title", "description"])

    if obj.Type() == "Folder":
       otherObj = catalog({"Creator":userId, "Type":"Profile"})[0].getObject()
       objTitle, objDescription = obj.title, obj.description
       otherObjTitle, otherObjDescription = otherObj.blogName, otherObj.blogDescription
       if objTitle != otherObjTitle:
           otherObj.blogName = objTitle
       if objDescription != otherObjDescription:
           otherObj.blogDescription = objDescription
       otherObj.reindexObject(idxs=["blogName", "blogDescription"])
