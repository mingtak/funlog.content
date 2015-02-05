from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api

from funlog.content import MessageFactory as _


class PersionalInfo(BrowserView):

    def getDescription(self):
        user = api.user.get_current()
        return user.getProperty('description')

    def getUserId(self):
        user = api.user.get_current()
        return user.id

    def getFullName(self):
        user = api.user.get_current()
        return user.getProperty('fullname')

    def getEmail(self):
        user = api.user.get_current()
        return user.getProperty('email')

    def getHomePage(self):
        user = api.user.get_current()
        return user.getProperty('home_page')


class SetPersionalInfo(BrowserView):

    def __call__(self):
        request = self.request
        response = request.response
        portal = api.portal.get()
        user = api.user.get_current()

        beforeValue = user.getProperty('description')
        afterValue = request['comments']
        if beforeValue != afterValue:
            user.setMemberProperties(mapping={"description":afterValue})

        redirectUrl = portal['site']['persional-information'].absolute_url()
        response.redirect(redirectUrl, lock=True)
        return

