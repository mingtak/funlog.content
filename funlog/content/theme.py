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

# for add/edit form
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm, DefaultEditView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from funlog.content import MessageFactory as _


# Interface class; used to define content-type schema.

class ITheme(form.Schema, IImageScaleTraversable):
    """
    Theme content type
    """
    title = schema.TextLine(
        title=_(u"Theme id"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Theme description"),
        required=False,
    )

    leadImage = NamedBlobImage(
        title=_("Theme image"),
        required=True,
    )


class AddForm(DefaultAddForm):
    template = ViewPageTemplateFile('template/addForm.pt')


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    template = ViewPageTemplateFile('template/editForm.pt')


class EditView(DefaultEditView):
    form = EditForm


class Theme(Container):
    grok.implements(ITheme)


class SampleView(grok.View):
    """ sample view class """

    grok.context(ITheme)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
