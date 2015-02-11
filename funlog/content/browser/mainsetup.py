from Products.Five.browser import BrowserView
from plone import api


class MainSetup(BrowserView):

    def __call__(self):
        catalog = self.context.portal_catalog
        userId = api.user.get_current().getId()
        url = catalog({"Creator":userId, "Type":"Profile"})[0].getURL()
        redirectUrl ="%s/edit" % url
        response = self.request.response
        return response.redirect(redirectUrl, lock=True)
