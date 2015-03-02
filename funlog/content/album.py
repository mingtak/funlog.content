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

from plone.app.contenttypes.interfaces import IImage
from collective import dexteritytextindexer
from plone.indexer import indexer

# for add/edit form
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm, DefaultEditView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from funlog.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IAlbum(form.Schema, IImageScaleTraversable):
    """
    Album folder
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_("Title for album"),
        required=True,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_("Description for album"),
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


class Album(Container):
    grok.implements(IAlbum)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IAlbum)
    grok.require('zope2.View')
    grok.name('view')
    # Add view methods here


# creat index and catalog for image

@indexer(IImage)
def aspectRatio_indexer(obj):
    width, height = obj.image.getImageSize()
    return float(width)/float(height)
grok.global_adapter(aspectRatio_indexer, name='aspectRatio')

@indexer(IImage)
def imageSize_indexer(obj):
    return obj.image.getSize()
grok.global_adapter(imageSize_indexer, name='imageSize')

@indexer(IAlbum)
def keywords_indexer(obj):
    keywords = obj.keywords
    return keywords.replace(' ', '').split(',')
grok.global_adapter(keywords_indexer, name='Subject')
