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
from collective import dexteritytextindexer

from funlog.content import MessageFactory as _


# Interface class; used to define content-type schema.

class ITravel(form.Schema, IImageScaleTraversable):
    """
    Travel Note
    """

    title = schema.TextLine(
        title=_(u"Title for travel"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description for travel"),
        description=_(u"Short description, if no filling, will show text head 20 words instead."),
        required=False,
    )

    dexterity.write_permission(leadImage='funlog.editTravel')
    leadImage = NamedBlobImage(
        title=_(u"Lead Image"),
        description=_(u"Will show in blog's article list page"),
        required=False,
    )

    dexterity.write_permission(location='funlog.editTravel')
    location = schema.TextLine(
        title=_(u"Location"),
        description=_(u"help_location", default="""
            Please fill in a specific location or address,
            such as "Yangmingshan" or "Chongqing South Road, Taipei's Zhongzheng District No. 122 paragraph 1,",
            Do not fill in the gray zone, such as "near by Yangmingshan", it will not locate on google map.""" ),
        required=True,
    )

    dexterity.write_permission(text='funlog.editTravel')
    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u"Text"),
        required=False,
    )


class Travel(Container):
    grok.implements(ITravel)


class SampleView(grok.View):
    """ sample view class """

    grok.context(ITravel)
    grok.require('zope2.View')
    grok.name('view')
    #Add view methods here
