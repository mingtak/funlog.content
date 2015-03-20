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

# for add/edit form
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm, DefaultEditView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from funlog.content import MessageFactory as _


# Validators

def checkBlogId(value):
    if not str(value).isalnum():
        raise Invalid(_(u"Wrong funlog id Format, please fill in only engilish letter or number."))
    portal = api.portal.get()
    if hasattr(portal['blog'], value) :
#        if portal['blog'][value].getOwner().getId() != api.user.get_current().getId():
        if portal['blog'][value].owner_info()["id"] != api.user.get_current().getId():
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
        title=_(u"Personal image."),
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

    form.omitted('imageQuota')
    imageQuota = schema.Int(
        title=_(u"Image quota"),
        description=_(u"500MB limited"),
        default=0,
        required=False,
    )

    # Fieldset for funlog setup
    form.fieldset(
        'funlogSetup',
        label=_(u"Funlog setup"),
        fields=['blogId', 'blogName', 'blogDescription', 'blogTheme', 'metaCode',]
    )

    blogId = schema.TextLine(
        title=_(u'label_blogId', default=u'Blog Id'),
        description=_(u"this value will became a part of blog url, be careful to change, and only engilish letter or number."),
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

    metaCode = schema.Text(
        title=_(u'label_metaCode', default=u'Meta code'),
        description=_(u"Meta code, only start at 'meta' tag, per line one record "),
        required=False,
    )

    form.omitted('blogTheme')
    blogTheme = schema.TextLine(
        title=_(u'label_Theme', default=u'Blog theme.'),
        description=_(u'Funlog switch theme'),
        default=u'creatika',
        required=False,
    )

    # Fieldset for funlog cover image
    form.fieldset(
        'funlogCoverImage',
        label=_(u"Funlog cover image"),
        fields=['coverImage_1', 'coverImage_2', 'coverImage_3', 'coverImage_4', 'coverImage_5'],
        description=_(u"You can upload up to five photos, Width: Height suggestions about 3: 2"),
    )

    coverImage_1 = NamedBlobImage(
        title=_(u"Cover image 1"),
        required=False,
    )

    coverImage_2 = NamedBlobImage(
        title=_(u"Cover image 2"),
        required=False,
    )

    coverImage_3 = NamedBlobImage(
        title=_(u"Cover image 3"),
        required=False,
    )

    coverImage_4 = NamedBlobImage(
        title=_(u"Cover image 4"),
        required=False,
    )

    coverImage_5 = NamedBlobImage(
        title=_(u"Cover image 5"),
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

    # Fieldset for funlog cover image
    form.fieldset(
        'Agree banner',
        label=_(u"Agree banner function"),
        fields=['agreeBanner', 'adScript'],
        description=_(u"check agreeBanner to enable you banner ad"),
    )

    agreeBanner = schema.Bool(
        title=_(u"Agree banner"),
        description=_(u"To agree banner function, check it."),
        default=False,
        required=False,
    )

    adScript = schema.Text(
        title=_(u"Ad Script"),
        description=_(u"To fill Ad script code"),
        required=False,
    )

    form.omitted('fbLongTermToken')
    fbLongTermToken = schema.TextLine(
        title=_(u"Facebook long term token"),
        required=False,
    )


class AddForm(DefaultAddForm):
    template = ViewPageTemplateFile('template/addForm.pt')


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    template = ViewPageTemplateFile('template/editForm.pt')


class EditView(DefaultEditView):
    form = EditForm


class Profile(Container):
    grok.implements(IProfile)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IProfile)
    grok.require('zope2.View')
    grok.name('view')

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

@indexer(IProfile)
def agreeBanner_indexer(obj):
    return obj.agreeBanner
grok.global_adapter(agreeBanner_indexer, name='agreeBanner')

@indexer(IProfile)
def adScript_indexer(obj):
    return obj.adScript
grok.global_adapter(adScript_indexer, name='adScript')

@indexer(IProfile)
def blogId_indexer(obj):
    return obj.blogId
grok.global_adapter(blogId_indexer, name='blogId')

@indexer(IProfile)
def blogName_indexer(obj):
    return obj.blogName
grok.global_adapter(blogName_indexer, name='blogName')

@indexer(IProfile)
def blogDescription_indexer(obj):
    return obj.blogDescription
grok.global_adapter(blogDescription_indexer, name='blogDescription')

@indexer(IProfile)
def blogTheme_indexer(obj):
    return obj.blogTheme
grok.global_adapter(blogTheme_indexer, name='blogTheme')

@indexer(IProfile)
def imageQutoa_indexer(obj):
    return obj.imageQutoa
grok.global_adapter(imageQutoa_indexer, name='imageQutoa')

@indexer(IProfile)
def email_indexer(obj):
    return obj.email
grok.global_adapter(email_indexer, name='email')

@indexer(IProfile)
def webPage_indexer(obj):
    return obj.webPage
grok.global_adapter(webPage_indexer, name='webPage')

@indexer(IProfile)
def fbUrl_indexer(obj):
    return obj.fbUrl
grok.global_adapter(fbUrl_indexer, name='fbUrl')

@indexer(IProfile)
def gPlusUrl_indexer(obj):
    return obj.gPlusUrl
grok.global_adapter(gPlusUrl_indexer, name='gPlusUrl')

@indexer(IProfile)
def linkedInUrl_indexer(obj):
    return obj.linkedInUrl
grok.global_adapter(linkedInUrl_indexer, name='linkedInUrl')

@indexer(IProfile)
def twitterUrl_indexer(obj):
    return obj.twitterUrl
grok.global_adapter(twitterUrl_indexer, name='twitterUrl')
