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
#    folderPath = "/%s" % userId
#    folder = api.content.get(path=folderPath)

    if hasattr(blogRoot, userId):
        return

    with api.env.adopt_roles(['Manager']):
        api.content.create(container=blogRoot, type="Folder", id=userId, title=username)
        api.content.create(container=profileRoot, type="funlog.content.profile", id=userId, title=username)
        user.setMemberProperties(mapping={'blogId':userId})
#        api.content.transition(obj=folder, transition='publish')
#        folder.reindexObject(idxs=["review_state"])


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


@grok.subscribe(IFolder, IObjectModifiedEvent)
def syncBolgTitle_Description(obj, event):
    user = api.user.get(userid=obj.getOwner().getId())
    blogName = safe_unicode(user.getProperty('blogName', ''))
    blogDescription = safe_unicode(user.getProperty('blogDescription', ''))

    if obj.title != blogName:
        user.setMemberProperties(mapping={'blogName': obj.title})

    if obj.description != blogDescription:
        user.setMemberProperties(mapping={'blogDescription': obj.description})
