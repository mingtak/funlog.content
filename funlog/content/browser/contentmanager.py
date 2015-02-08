from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api

from funlog.content import MessageFactory as _


class ContentManager(BrowserView):

    template = ViewPageTemplateFile('templates/contentmanager.pt')
    jqueryCodeTemplate = ViewPageTemplateFile('templates/jqueryCodeTemplate.pt')

    def __call__(self):
        self.portal = api.portal.get()
        self.catalog = self.portal.portal_catalog
        self.user = api.user.get_current()
        return self.template()

    def getBrain(self, type=None):
        brain = self.catalog({"Creator":self.user.id, "Type":type,
                              "review_state":["published", "private", "tempState"]},
                             sort_on="created", sort_order="reverse")
        return brain

    def albumBrain(self):
        return self.getBrain("Album")

    def articleBrain(self):
        return self.getBrain("Article")

    def travelBrain(self):
        return self.getBrain("Travel")

    def getTransitions(self, review_state=None):
        if review_state == "published":
            return [_(u"retract"), _(u"throwAway")]
        if review_state == "private":
            return [_(u"publish"), _(u"throwAway")]
        if review_state == "tempState":
            return [_(u"publish"), _(u"retract"), _(u"throwAway")]
        if review_state == "traceCan":
            return [_(u"retract")]

    def jqueryCode(self, item, transition):
        self.scriptString = """
            <script type="text/javascript" async="true" defer="true">
              $(document).ready(function(){
                $('#%s%sinput').click(function(){
                  setTimeout(function(){
                    $('#%s').load('%s?uid=%s');
                  }, 500);
                });
              });
           </script>
        """ % (item.UID, transition, item.UID, 'http://localhost:7777/funlog/update_jquery', item.UID)
        return self.jqueryCodeTemplate()



class ContentTransition(BrowserView):

    def __call__(self):
        self.portal = self.context
        self.catalog = self.portal.portal_catalog
        return self.transition()

    def transition(self):
        request = self.request
        transition, type, uid = request['transition'], request['type'], request['uid']
        item = self.catalog({"UID":uid, "Type":type})[0]
        state = api.content.transition(obj=item.getObject(), transition=transition)
        return state 


class UpdateJquery(BrowserView):

    updateJqueryTemplate = ViewPageTemplateFile('templates/updateJqueryTemplate.pt')
    jqueryCodeTemplate = ViewPageTemplateFile('templates/jqueryCodeTemplate.pt')

    def __call__(self):
        self.uid = self.request['uid']
        self.portal = self.context
        self.catalog = self.portal.portal_catalog
        self.item = self.catalog({'UID':self.uid})[0]
        self.id = self.item.id
        self.state = self.item.review_state
        if self.state == "published":
            self.transitions = [_(u"retract"), _(u"throwAway")]
        if self.state == "private":
            self.transitions = [_(u"publish"), _(u"throwAway")]
        if self.state == "tempState":
            self.transitions = [_(u"publish"), _(u"retract"), _(u"throwAway")]
        if self.state == "traceCan":
            self.transitions = [_(u"retract")]
        return self.updateJqueryTemplate()


    def jqueryCode(self, item, transition):
        self.scriptString = """
            <script type="text/javascript" async="true" defer="true">
              $(document).ready(function(){
                $('#%s%sinput').click(function(){
                  setTimeout(function(){
                    $('#%s').load('%s?uid=%s');
                  }, 500);
                });
              });
           </script>
        """ % (item.UID, transition, item.UID, 'http://localhost:7777/funlog/update_jquery', item.UID)
        return self.jqueryCodeTemplate()

