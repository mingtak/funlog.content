from five import grok
from plone import api
from Products.CMFPlone.utils import safe_unicode

from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent, IObjectAddedEvent, IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent, IAfterTransitionEvent
from zope.app.container.interfaces import IObjectAddedEvent
from zope import component
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
from zope.event import notify

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

@grok.subscribe(IFolder, IAfterTransitionEvent)
def transitionState(item, event):
    catalog = item.portal_catalog
    userId = item.owner_info()["id"]
    otherObj = catalog({"Creator":userId, "Type":"Profile"})
    if len(otherObj) == 0:
        return
    otherObj = otherObj[0].getObject()
    if api.content.get_state(obj=item) == "private" and otherObj.blogOnOff == True:
        otherObj.blogOnOff = False
    if api.content.get_state(obj=item) == "published" and otherObj.blogOnOff == False:
        otherObj.blogOnOff = True


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
#    import pdb; pdb.set_trace()
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
    with api.env.adopt_user(user=user):
        with api.env.adopt_roles(['Manager']):
            funlog = api.content.create(container=blogRoot, type="Folder", id=userId, title=username)
            profile = api.content.create(container=profileRoot, type="funlog.content.profile", id=userId, title=username)
            profile.blogId = userId
            profile.blogName = username
            profile.reindexObject(idxs=["blogId", "blogName"])


from mingtak.oauthlogin.browser.oauthLogin import OauthWorkFlow
import urllib2

@grok.subscribe(UserLoggedInEvent)
@grok.subscribe(UserInitialLoginInEvent)
def updateLongTermToken(event):
    portal = api.portal.get()
    user = event.object
    longTermToken = user.getProperty("description")
    userId = user.id
    if hasattr(portal["profile"], userId):
        profile = portal["profile"][userId]
        if profile.fbLongTermToken is None:
            shortTermToken = user.getProperty("description")
        else:
            shortTermToken = profile.fbLongTermToken
#        import pdb; pdb.set_trace()


        oauthWorkFlow = OauthWorkFlow(oauthServerName="facebook")
        client_id, client_secret, scope, redirect_uri = oauthWorkFlow.getRegistryValue()
        token_url = "https://graph.facebook.com/oauth/access_token"
        exchangeTokenUrl = "%s?client_id=%s&client_secret=%s&grant_type=fb_exchange_token&fb_exchange_token=%s" % \
                           (token_url, client_id, client_secret, shortTermToken)
        longTermToken = urllib2.urlopen(exchangeTokenUrl)
        longTermToken = longTermToken.read().split("=")[1].split("&")[0]
        user.setMemberProperties({"description":""})
        profile.fbLongTermToken = longTermToken

@grok.subscribe(IImage, IObjectAddedEvent)
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

@grok.subscribe(IImage, IObjectAddedEvent)
@grok.subscribe(IAlbum, IObjectAddedEvent)
@grok.subscribe(IArticle, IObjectAddedEvent)
@grok.subscribe(ITravel, IObjectAddedEvent)
def setRelatedProfile(obj, event):
    """ Set related profile """
    userId = obj.owner_info()['id']
    if 'Manager' in api.user.get_roles(username=userId):
        return
    catalog = obj.portal_catalog
    profile = catalog({"Type":"Profile", "Creator":userId})[0].getObject()
    intIds = component.getUtility(IIntIds)
    obj.relatedProfile = RelationValue(intIds.getId(profile))
    notify(ObjectModifiedEvent(obj))



@grok.subscribe(IProfile, IObjectModifiedEvent)
@grok.subscribe(IFolder, IObjectModifiedEvent)
def syncBolgTitle_Description(obj, event):
    userId = obj.owner_info()["id"]
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
        if obj.blogOnOff == True and api.content.get_state(obj=otherObj) == "private":
            api.content.transition(obj=otherObj, transition="publish")
        if obj.blogOnOff == False and api.content.get_state(obj=otherObj) == "published":
            api.content.transition(obj=otherObj, transition="retract")
        otherObj.reindexObject(idxs=["id", "title", "description", "review_state"])

    if obj.Type() == "Folder":
        otherObj = catalog({"Creator":userId, "Type":"Profile"})[0].getObject()
        objTitle, objDescription = obj.title, obj.description
        otherObjTitle, otherObjDescription = otherObj.blogName, otherObj.blogDescription
        if objTitle != otherObjTitle:
            otherObj.blogName = objTitle
        if objDescription != otherObjDescription:
            otherObj.blogDescription = objDescription
        otherObj.reindexObject(idxs=["blogName", "blogDescription",])
