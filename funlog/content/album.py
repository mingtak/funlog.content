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


from funlog.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IAlbum(form.Schema, IImageScaleTraversable):
    """
    Album folder
    """

    title = schema.TextLine(
        title=_("Title for album"),
        required=True,
    )

    description = schema.Text(
        title=_("Description for album"),
        required=False,
    )


class Album(Container):
    grok.implements(IAlbum)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IAlbum)
    grok.require('zope2.View')
    grok.name('view')
    # Add view methods here
