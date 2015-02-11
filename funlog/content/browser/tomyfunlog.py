from Products.Five.browser import BrowserView
from plone import api


class ToMyFunlog(BrowserView):

    def __call__(self):
        catalog = self.context.portal_catalog
        userId = api.user.get_current().getId()
        redirectUrl = catalog({"Creator":userId, "Type":"Folder"})[0].getURL()
        response = self.request.response
        return response.redirect(redirectUrl, lock=True)
