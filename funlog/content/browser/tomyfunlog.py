from Products.Five.browser import BrowserView
from plone import api


class ToMyFunlog(BrowserView):

    def __call__(self):
        response = self.request.response
        portal = api.portal.get()
        blogRoot = portal['blog']
        user = api.user.get_current()
        blogId = user.getProperty('blogId')
        redirectUrl = blogRoot[blogId].absolute_url()
        return response.redirect(redirectUrl, lock=True)

