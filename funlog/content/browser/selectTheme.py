from five import grok
from funlog.content.profile import IProfile
from Products.CMFPlone.utils import safe_unicode


grok.templatedir('templates')

class SelectTheme(grok.View):

    grok.context(IProfile)
    grok.require('cmf.ModifyPortalContent')

    def changeTheme(self, themeId):
        catalog = self.context.portal_catalog
        if themeId == self.context.blogTheme:
            return
        brain = catalog({'Type':'Theme','id':themeId})
        if len(brain) == 0:
            self.context.blogTheme = 'default'
        else:
            self.context.blogTheme = themeId
        self.context.reindexObject(idxs=['blogTheme'])

    def update(self):

        catalog = self.context.portal_catalog
        themeId = safe_unicode(getattr(self.request, 'theme', None))
        if themeId is not None:
            self.changeTheme(themeId)

        self.themeBrain = catalog(Type='Theme', sort_on='created', sort_order='reverse')
