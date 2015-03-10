from five import grok
from funlog.content.profile import IProfile


grok.templatedir('templates')

class SelectTheme(grok.View):

    grok.context(IProfile)
    grok.require('cmf.ModifyPortalContent')

    def update(self):
        import pdb; pdb.set_trace()
        catalog = self.context.portal_catalog
        self.themeBrain = catalog(Type='Theme', sort_on='created', sort_order='reverse')
        return
