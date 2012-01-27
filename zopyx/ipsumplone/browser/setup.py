################################################################
# zopyx.ipsumplone
# (C) 2012, ZOPYX Limited. Published under GPL 2
################################################################


import os
import urllib2
import random
import loremipsum

from DateTime.DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.CMFPlone.factory import addPloneSite
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.de import Normalizer

def gen_paragraphs(num=3):
    return u'/'.join([p[2] for p in loremipsum.Generator().generate_paragraphs(num)])

def gen_sentence():
    return loremipsum.Generator().generate_sentence()[-1]

def gen_word():
    return gen_sentence().split()[0]

def gen_sentences(length=80):
    return u'/'.join([s[2] for s in loremipsum.Generator().generate_sentences(length)])

def random_image(width, height):
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()

class Setup(BrowserView):

    def setupSite(self, prefix='sample', extra_profiles=[]):
        portal_id = '%s-%s' % (prefix, DateTime().strftime('%d.%m.%y-%H%M%S'))
        profiles = ['plonetheme.sunburst:default'] + extra_profiles
        addPloneSite(self.context, portal_id, create_userfolder=True, extension_ids=profiles)
        self.site = self.context[portal_id]
        self.request.response.redirect(self.context.getId() + '/' + portal_id)

    def setupDemoContent(self):
        for i in range(1, 10):
            self.createDocument('press/release-%d' % i, title='Press release %d' % i)
        for i in range(1, 10):
            self.createImage('images/image-%d' % i, width=800, height=600)
        for i in range(1, 10):
            self.createNewsitem('news/newsitem-%d' % i)
        for i in range(1, 10):
            self.createEvent('events/event-%d' % i)
        self.request.response.redirect(self.context.absolute_url())

    def _createObject(self, portal_type, path, title=None, description=None):

        dirpath, id = path.rsplit('/')
        current = self.context
        for p in dirpath.split('/'):
            if not p in current.objectIds():
                current.invokeFactory('Folder', id=p, title=p)
                current[p].setTitle(p.capitalize())
                current[p].reindexObject()
            current = current[p]

        if id in current.objectIds():
            current.manage_delObjects(id)    
        current.invokeFactory(portal_type, id=id)
        obj = current[id]
        fieldNames = [field.getName() for field in obj.Schema().fields()]

        if not title:
            title = gen_sentence()
        if not description:
            description = gen_paragraphs(1)

        obj.setTitle(title)
        obj.setDescription(description)
        if 'text' in fieldNames:
            obj.setText(gen_sentences())
            obj.setContentType('text/html')
            obj.Schema().getField('text').getContentType(obj, 'text/html')
        obj.reindexObject()
        return obj    

    def createDocument(self, path, title=None):
        obj = self._createObject('Document', path, title=title)
        obj.reindexObject()

    def createNewsitem(self, path, title=None):
        obj = self._createObject('News Item', path, title=title)
        obj.setImage(random_image(400, 200))
        obj.reindexObject()

    def createImage(self, path, width=800, height=600, title=None):
        obj = self._createObject('Image', path, title=title)
        obj.setImage(random_image(width, height))
        obj.reindexObject()

    def createEvent(self, path):
        obj = self._createObject('Event', path)
        start = DateTime() + random.randint(-1000, 1000)
        end = start + random.randint(0,5)
        obj.setStartDate(start)
        obj.setEndDate(end)
        obj.setLocation(gen_word())
        obj.setEventUrl('http://www.plone.org')
        obj.setContactName('Andreas Jung')
        obj.setContactEmail('dummy@plone.org')
        obj.reindexObject()

