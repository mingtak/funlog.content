from five import grok
from zope.interface import Interface
from plone import api


class IsManager(grok.View):

    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("isManager")

    def update(self):
        if api.user.is_anonymous():
            self.isManager = False
        elif 'Manager' in api.user.get_roles():
            self.isManager = True
        else:
            self.isManager = False

    def render(self):
        return self.isManager
