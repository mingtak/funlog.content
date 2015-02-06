from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api

from funlog.content import MessageFactory as _


class PersionalInfo(BrowserView):

    def getUserPeoperty(self, property=None):
        user = api.user.get_current()
        return user.getProperty(property)

    def getUserId(self):
        user = api.user.get_current()
        return user.id

    def getFullName(self):
        user = api.user.get_current()
        return user.getProperty('fullname')

    def getDescription(self):
        user = api.user.get_current()
        return user.getProperty('description')

    def getEmail(self):
        user = api.user.get_current()
        return user.getProperty('email')

    def getHomePage(self):
        user = api.user.get_current()
        return user.getProperty('home_page')


class SetPersionalInfo(BrowserView):

    def setMemberProperty(self, user, property, beforeValue, afterValue):
        if beforeValue != afterValue:
            user.setMemberProperties(mapping={property:afterValue})

    def callBackUrl(self, portal, response):
        redirectUrl = portal['site']['persional-information'].absolute_url()
        response.redirect(redirectUrl, lock=True)

    def __call__(self):
        request = self.request
        response = request.response
        portal = api.portal.get()
        user = api.user.get_current()
        httpValue = getattr(request, 'persional-homepage', '')[0:7]
        httpsValue = getattr(request, 'persional-homepage', '')[0:8]
        if httpValue != "http://" and httpsValue != "https://":
            api.portal.show_message(message=_(u"Worn url format, must be include 'http://' or 'https://'"), request=request, type='warn')
            self.callBackUrl(portal, response)
            return

        beforeValue = user.getProperty('fullname')
        afterValue = getattr(request, 'user-name', '')
        self.setMemberProperty(user, 'fullname', beforeValue, afterValue)

        beforeValue = user.getProperty('description')
        afterValue = getattr(request, 'persional-description', '')
        self.setMemberProperty(user, 'description', beforeValue, afterValue)

        beforeValue = user.getProperty('home_page')
        afterValue = getattr(request, 'persional-homepage', '')
        self.setMemberProperty(user, 'home_page', beforeValue, afterValue)


        self.callBackUrl(portal, response)
        return
