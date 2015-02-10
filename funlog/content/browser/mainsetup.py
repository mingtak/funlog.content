from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api

from funlog.content import MessageFactory as _


class MainSetup(BrowserView):

    template = ViewPageTemplateFile('templates/mainsetup.pt')

    def __call__(self):
        request = self.request
        response = request.response
        portal = api.portal.get()
        user = api.user.get_current()

        return self.template()
