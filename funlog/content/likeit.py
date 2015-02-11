from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from plone.directives import form
from zope.component import adapts
from zope.interface import alsoProvides, implements

from funlog.content import MessageFactory as _


class ILikeIt(model.Schema):
    """
       Marker/Form interface for LikeIt
    """
    form.omitted('likeItList')
    likeItList = schema.List(
        title=_(u"Like it list"),
        value_type=schema.Choice(
            title=_(u"users"),
            vocabulary="plone.principalsource.Users",
            required=False,
        ),
        required=False,
    )



alsoProvides(ILikeIt, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class LikeIt(object):
    """
       Adapter for LikeIt
    """
    implements(ILikeIt)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-

    likeItList = context_property("likeItList")
