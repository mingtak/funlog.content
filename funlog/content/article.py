from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from funlog.content import profile
from collective import dexteritytextindexer
from plone.indexer import indexer

# for add/edit form
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm, DefaultEditView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from funlog.content import MessageFactory as _


# Interface class; used to define content-type schema.

from plone.formwidget.autocomplete import AutocompleteFieldWidget

"""
@grok.provider(IContextSourceBinder)
def availableAttachments(context):
#    catalog = context.portal_catalog
    query = {"Creator":context.owner_info()["id"], "portal_type":"funlog.content.profile"}
#    import pdb; pdb.set_trace()
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)
"""


class IArticle(form.Schema, IImageScaleTraversable):
    """
    Normal article
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title for album"),
        required=True,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Description for album"),
        description=_(u"Short description, if no filling, will show text head 20 words instead."),
        required=False,
    )

    leadImage = NamedBlobImage(
        title=_(u"Lead Image"),
        description=_(u"Will show in blog's article list page"),
        required=False,
    )

    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u"Text"),
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


class Article(Container):
    grok.implements(IArticle)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IArticle)
    grok.require('zope2.View')
    grok.name('view')
    # Add view methods here


@indexer(IArticle)
def aspectRatio_indexer(obj):
    width, height = obj.leadImage.getImageSize()
    return float(width)/float(height)
grok.global_adapter(aspectRatio_indexer, name='aspectRatio')

@indexer(IArticle)
def imageSize_indexer(obj):
    return obj.leadImage.getSize()
grok.global_adapter(imageSize_indexer, name='imageSize')

@indexer(IArticle)
def likeItList_indexer(obj):
    return obj.likeItList
grok.global_adapter(likeItList_indexer, name='likeItList')

@indexer(IArticle)
def likeItCount_indexer(obj):
    return len(obj.likeItList)
grok.global_adapter(likeItCount_indexer, name='likeItCount')

@indexer(IArticle)
def keywords_indexer(obj):
    keywords = obj.keywords
    return keywords.replace(' ', '').split(',')
grok.global_adapter(keywords_indexer, name='Subject')
