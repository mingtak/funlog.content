from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
from Products.CMFPlone.utils import safe_unicode

from funlog.content import MessageFactory as _


class PersionalInfo(BrowserView):

    def getUserPeoperty(self, property=None):
        user = api.user.get_current()
        return user.getProperty(property)

    def getBlogName(self):
        return self.getUserPeoperty('blogName')

    def getBlogDescription(self):
        return self.getUserPeoperty('blogDescription')

    def getBlogOnOff(self):
        return self.getUserPeoperty('blogOnOff')

    def getBlogId(self):
        return self.getUserPeoperty('blogId')

    def getUserId(self):
        return self.getUserPeoperty('id')

    def getFullName(self):
        return self.getUserPeoperty('fullname')

    def getDescription(self):
        return self.getUserPeoperty('description')

    def getEmail(self):
        return self.getUserPeoperty('email')

    def getHomePage(self):
        return self.getUserPeoperty('home_page')


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
            api.portal.show_message(message=_(u"Error url format, must be include 'http://' or 'https://'"), request=request, type='error')
            self.callBackUrl(portal, response)
            return

        beforeValue = safe_unicode(user.getProperty('fullname'))
        afterValue = safe_unicode(getattr(request, 'user-name', ''))
        self.setMemberProperty(user, 'fullname', beforeValue, afterValue)

        beforeValue = safe_unicode(user.getProperty('description'))
        afterValue = safe_unicode(getattr(request, 'persional-description', ''))
        self.setMemberProperty(user, 'description', beforeValue, afterValue)

        beforeValue = safe_unicode(user.getProperty('home_page'))
        afterValue = safe_unicode(getattr(request, 'persional-homepage', ''))
        self.setMemberProperty(user, 'home_page', beforeValue, afterValue)


        self.callBackUrl(portal, response)
        return


class SetBlogInfo(BrowserView):

    def setMemberProperty(self, user, property, beforeValue, afterValue):
        if beforeValue != afterValue:
            user.setMemberProperties(mapping={property:safe_unicode(afterValue)})

    def callBackUrl(self, portal, response):
        redirectUrl = portal['site']['blog-setup'].absolute_url()
        response.redirect(redirectUrl, lock=True)

    def __call__(self):
        request = self.request
        response = request.response
        portal = api.portal.get()
        user = api.user.get_current()

        beforeValue = safe_unicode(user.getProperty('blogId'))
        afterValue = safe_unicode(getattr(request, 'blog-id', ''))
        if not afterValue.encode('utf-8').isalnum():
            api.portal.show_message(message=_('Error blog id format, only use A-Z, a-z, 0-9.'), request=request, type='error')
            self.callBackUrl(portal, response)
            return
        if beforeValue != afterValue:
            with api.env.adopt_roles(['Manager']):
                folder = api.content.rename(obj=portal[beforeValue], new_id=afterValue.encode('utf-8'))
                folder.reindexObject(idxs=["id"])
            self.setMemberProperty(user, 'blogId', beforeValue, afterValue)

        beforeValue = safe_unicode(user.getProperty('blogName'))
        afterValue = safe_unicode(getattr(request, 'blog-name', ''))
        self.setMemberProperty(user, 'blogName', beforeValue, afterValue)

        beforeValue = safe_unicode(user.getProperty('blogOnOff'))
        afterValue = safe_unicode(getattr(request, 'blog-on-off', True))
        self.setMemberProperty(user, 'blogOnOff', beforeValue, afterValue)

        beforeValue = safe_unicode(user.getProperty('blogDescription'))
        afterValue = safe_unicode(getattr(request, 'blog-description', ''))
        self.setMemberProperty(user, 'blogDescription', beforeValue, afterValue)

        self.callBackUrl(portal, response)
        return

