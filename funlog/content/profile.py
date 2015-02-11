from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
#from plone.autoform import directives
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from plone import api
from collective import dexteritytextindexer
from plone.indexer import indexer

from funlog.content import MessageFactory as _


# Validators

def checkBlogId(value):
    if not str(value).isalnum():
        raise Invalid(_(u"Wrong funlog id Format, please fill in only engilish letter or number."))
    portal = api.portal.get()
    if hasattr(portal['blog'], value) :
        if portal['blog'][value].getOwner().getId() != api.user.get_current().getId():
            raise Invalid(_(u"Sorry! this blog id already in use."))
    return True

def checkEmail(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise Invalid(_(u"Invalid email address."))
    return True


# Interface
class IProfile(form.Schema, IImageScaleTraversable):
    """
    Profile content type for funloger
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Name"),
        required=True,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Introduction"),
        required=False,
    )

    leadImage = NamedBlobImage(
        title=_(u"Persional image."),
        required=False,
    )

    form.omitted('followList')
    followList = schema.List(
        title=_(u"Follow list"),
        value_type=schema.Choice(
            title=_(u"users"),
            vocabulary="plone.principalsource.Users",
            required=False,
        ),
        required=False,
    )

    # Fieldset for funlog setup
    form.fieldset(
        'funlogSetup',
        label=_(u"Funlog setup"),
        fields=['blogId', 'blogName', 'blogDescription', 'blogTheme']
    )

    blogId = schema.TextLine(
        title=_(u'label_blogId', default=u'Blog Id'),
        description=_(u"this value will became a port of blog url, be careful to change, and only engilish letter or number."),
        required=True,
        constraint=checkBlogId
    )

    dexteritytextindexer.searchable('blogName')
    blogName = schema.TextLine(
        title=_(u'label_blogName', default=u'Blog name'),
        default=_(u"My funlog space"),
        required=True,
    )

    dexteritytextindexer.searchable('blogDescription')
    blogDescription = schema.Text(
        title=_(u'label_blogDescription', default=u'Blog description'),
        default=_(u"Introuction for my funlog"),
        required=True,
    )

    blogTheme = schema.TextLine(
        title=_(u'label_Theme', default=u'Blog theme.'),
        description=_(u'Funlog switch theme'),
        required=False,
    )

    # Fieldset for funlog switch on/off
    form.fieldset(
        'blogSwitch',
        label=_(u"Blog switch"),
        fields=['blogOnOff']
    )

    blogOnOff = schema.Bool(
        title=_(u'label_description', default=u'Blog siwtch.'),
        description=_(u'Funlog switch turn on/off'),
        default=True,
        required=False,
    )

    # Social network fieldset
    form.fieldset(
        'social',
        label=_(u"Social network"),
        fields=['email', 'webPage', 'fbUrl', 'gPlusUrl', 'twitterUrl', 'linkedInUrl']
    )

    email = schema.TextLine(
        title=_(u"email"),
        description=_(u"Contact email address"),
        required=False,
        constraint=checkEmail
    )

    webPage = schema.URI(
        title=_(u"External website"),
        description=_(u"Must be include 'http://' or 'https://'"),
        required=False,
    )

    fbUrl = schema.URI(
        title=_(u"Your facebook address"),
        description=_(u"Must be include 'http://' or 'https://'"),
        required=False,
    )

    gPlusUrl = schema.URI(
        title=_(u"Your google plus address"),
        description=_(u"Must be include 'http://' or 'https://'"),
        required=False,
    )

    twitterUrl = schema.URI(
        title=_(u"Your twitter address"),
        description=_(u"Must be include 'http://' or 'https://'"),
        required=False,
    )

    linkedInUrl = schema.URI(
        title=_(u"Your linkedIn address"),
        description=_(u"Must be include 'http://' or 'https://'"),
        required=False,
    )


class Profile(Container):
    grok.implements(IProfile)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IProfile)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here


@indexer(IProfile)
def aspectRatio_indexer(obj):
    width, height = obj.leadImage.getImageSize()
    return float(width)/float(height)
grok.global_adapter(aspectRatio_indexer, name='aspectRatio')

@indexer(IProfile)
def imageSize_indexer(obj):
    return obj.leadImage.getSize()
grok.global_adapter(imageSize_indexer, name='imageSize')

@indexer(IProfile)
def followList_indexer(obj):
    return obj.followList
grok.global_adapter(followList_indexer, name='followList')
