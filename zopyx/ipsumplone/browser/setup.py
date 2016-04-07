################################################################
# zopyx.ipsumplone
# (C) 2012, ZOPYX Limited. Published under GPL 2
################################################################


import os
import urllib2
import loremipsum

import plone.api
import zope.component
from DateTime.DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.CMFPlone.factory import addPloneSite
from Products.CMFCore.WorkflowCore import WorkflowException
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityFTI
from plone.behavior.interfaces import IBehaviorAssignable
from plone.namedfile import NamedImage
from plone.namedfile import NamedFile


pdf_data = file(os.path.join(os.path.dirname(__file__), 'demo.pdf'), 'rb').read()


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


def get_all_fields(context):
    """ Return all fields (including behavior fields) of a context object
        as dict fieldname -> field.
    """

    schema = zope.component.getUtility(
        IDexterityFTI, name=context.portal_type).lookupSchema()
    fields = dict((fieldname, schema[fieldname]) for fieldname in schema)

    assignable = IBehaviorAssignable(context)
    for behavior in assignable.enumerateBehaviors():
        behavior_schema = behavior.interface
        fields.update((name, behavior_schema[name])
                      for name in behavior_schema)

    return fields


class Setup(BrowserView):

    def setupSite(self, prefix='sample', extra_profiles=[]):
        portal_id = '%s-%s' % (prefix, DateTime().strftime('%y-%m-%d-%H%M%S'))
        profiles = ['plonetheme.barceloneta:default'] + extra_profiles
        addPloneSite(self.context, portal_id, extension_ids=profiles)
        self.site = self.context[portal_id]
        if 'content' in self.request.form:
            self.site.restrictedTraverse('@@demo-content')()
        self.request.response.redirect(self.context.getId() + '/' + portal_id)

    def setupDemoContent(self):
        for i in range(1, 10):
            self.createDocument('documents/document-%d' % i, title='Document %d' % i)
        for i in range(1, 10):
            self.createNewsitem('documents-all-content/document-%d' % i, title='Document %d' % i)
        self.context['documents-all-content'].setLayout('summary_view')
        for i in range(1, 20):
            self.createImage('images/image-%d' % i, width=800, height=600)
        self.context['images'].setLayout('album_view')
        for i in range(1, 10):
            self.createNewsitem('news/newsitem-%d' % i)
        for i in range(1, 10):
            self.createFile('files/file-%d' % i)
        for i in range(1, 10):
            self.createEvent('events/events-%d' % i)
        self.request.response.redirect(self.context.absolute_url())

    def _createObject(self, portal_type, path, title=None, description=None, publish=True):

        dirpath, id = path.rsplit('/', 1)
        current = self.context
        for p in dirpath.split('/'):
            if p not in current.objectIds():
                obj = plone.api.content.create(type='Folder', container=current, id=p, title=p)
                obj.setTitle(p.capitalize())
                plone.api.content.transition(obj, 'publish')
                obj.reindexObject()
                current = obj
            else:
                current = current[p]

        if id in current.objectIds():
            current.manage_delObjects(id)
        obj = plone.api.content.create(type=portal_type, container=current, id=id)
        obj = current[id]

        all_fields = get_all_fields(obj)

        if not title:
            title = gen_sentence()
        if not description:
            description = gen_paragraphs(1)

        obj.setTitle(title)
        obj.setDescription(description)
        if 'text' in all_fields:
            text = gen_sentences()
            obj.text = RichTextValue(text, 'text/html', 'text/html')

        if publish:
            try:
                plone.api.content.transition(obj=obj, transition='publish')
            except:
                pass
        obj.reindexObject()
        return obj

    def createDocument(self, path, title=None):
        obj = self._createObject('Document', path, title=title)
        obj.reindexObject()

    def createNewsitem(self, path, title=None):
        obj = self._createObject('News Item', path, title=title)
        named_image = NamedImage()
        named_image.data = random_image(400, 200)
        named_image.filename = u'test.jpg'
        named_image.contentType = 'image/jpg'
        obj.image = named_image
        obj.reindexObject()

    def createImage(self, path, width=800, height=600, title=None):
        obj = self._createObject('Image', path, title=title)
        named_image = NamedImage()
        named_image.data = random_image(width, height)
        named_image.filename = u'test.jpg'
        named_image.contentType = 'image/jpg'
        obj.image = named_image
        obj.reindexObject()

    def createFile(self, path, title=None):
        obj = self._createObject('File', path, title=title)
        named_file = NamedFile()
        named_file.data = pdf_data
        named_file.filename = u'test.pdf'
        named_file.contentType = 'application/pdf'
        obj.file = named_file
        obj.reindexObject()
    
    def createEvent(self, path, title=None):
        obj = self._createObject('Event', path, title=title)
        obj.contact_name = u'Heinz Becker'
        obj.contact_email = u'no-such-email@demo.com'
        obj.contact_phone = '+49 1234 1212121'
        obj.event_url = u'https://www.plone.org'
        obj.reindexObject()
