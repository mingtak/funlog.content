from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime

from plone import api

from funlog.content import MessageFactory as _

class SiteSearch(BrowserView):

    template = ViewPageTemplateFile('templates/sitesearch.pt')

    def __call__(self):
        portal = api.portal.get()
        catalog = portal.portal_catalog
        request = self.request
        keyword = getattr(request, 'keyword', '').strip()
        if keyword == '':
            return self.template()
        now = DateTime()
        startDate = now - 90
        self.brainByLatest = catalog({'SearchableText':keyword,
                                      'Type':['Article', 'Album', 'Travel'],
                                      'created':{'query':startDate, 'range':'min'},},
                                     sort_on='created', sort_order='reverse')
        self.brainByHotest = catalog({'SearchableText':keyword,
                                      'Type':['Article', 'Album', 'Travel'],
                                      'created':{'query':startDate, 'range':'min'},},
                                     sort_on='likeItCount', sort_order='reverse')
        return self.template()
