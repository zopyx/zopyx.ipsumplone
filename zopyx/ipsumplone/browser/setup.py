import os
import urllib2
import random
import loremipsum

from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFPlone.factory import addPloneSite
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.de import Normalizer


def gen_paragraphs(num=3):
    return u'/'.join([p[2] for p in loremipsum.Generator().generate_paragraphs(num)])

def gen_sentence():
    return loremipsum.Generator().generate_sentence()[-1]

def gen_sentences(length=80):
    return u'/'.join([s[2] for s in loremipsum.Generator().generate_sentences(length)])

def random_image(width, height):
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()

def invokeFactory(folder, portal_type, title=None):
    pt = getToolByName(folder, 'plone_utils')
    obj_title = title
    if not obj_title:
        obj_title = gen_sentence()
    obj_id = pt.normalizeString(obj_title)
    if obj_id in folder.objectIds():
        obj_id += str(random.randint(0,100))
    folder.invokeFactory(portal_type, id=obj_id, title=obj_title)
    folder[obj_id].reindexObject()
    folder[obj_id].setDescription(gen_paragraphs(1))
    return folder[obj_id]

class Setup(BrowserView):

    def setupSite(self, prefix='sample', extra_profiles=[]):
        portal_id = '%s-%s' % (prefix, DateTime().strftime('%d.%m.%y-%H%M%S'))
        profiles = ['plonetheme.sunburst:default'] + extra_profiles
        addPloneSite(self.context, portal_id, create_userfolder=True, extension_ids=profiles)
        site = self.context[portal_id]
        self.request.response.redirect(self.context.getId() + '/' + portal_id)


    def setupContent(self, site):
        self.installStructure(site)
        self.installPressRoom(site)
        self.installReferences(site)
        self.installProductInfo(site)
        self.installGlossary(site)
        self.installMessekalendar(site)
        self.installDownloads(site)
        self.installAssets(site)

    def installStructure(self, site):

        site.restrictedTraverse('setup-subsidary')('deutschland', ('de', 'en'))

        fname = os.path.join(os.path.dirname(__file__), '..', 'data', 'structure.txt')        
        for line in file(fname):
            line = line.strip()
            if not line:
                continue

            if ':' in line:
                path, portal_type = line.split(':')
            else:
                path = line
                portal_type = 'Document'

            language = 'de'
            if line.startswith('en/'):
                language = 'en'

            current = site
            level = 0
            for c in path.split('/')[:-1]:
                if not c in current.objectIds():
                    current.invokeFactory(level2pt.get(level, 'Folder'), id=c, title=c.capitalize())
                current = current[c]
                level += 1
                current.setLanguage(language)
                current.reindexObject()

            id = path.split('/')[-1]
            if id in current.objectIds():
                current.manage_delObjects(id)
            current.invokeFactory(portal_type, id=id, title=id.capitalize())
            content = current[id]
            content.reindexObject()
            content.setLanguage(language)

    def installProductInfo(self, site):
        produkte = site.restrictedTraverse('deutschland/de/produkte/neubau')
        produkt = invokeFactory(produkte, 'ProductFolder', 'Brennwertkessel')
        for i in range(3):
            pi = invokeFactory(produkt, 'ProductInfoPage')
            pi.setText(gen_sentences())
            pi.setImage(random_image(500, 300))
            pi.reindexObject()

    def installReferences(self, site):
        ueber = site.restrictedTraverse('deutschland/de/unternehmen')
        reff = invokeFactory(ueber, 'ReferencesFolder', 'Unsere Referenzen')
        for i in range(9):
            ref = invokeFactory(reff, 'Reference')
            ref.setText(gen_sentences())
            ref.setImage(random_image(400, 400))
            ref.reindexObject()

    def installGlossary(self, site):
        service = site.restrictedTraverse('deutschland/de/service')
        glossary = invokeFactory(service, 'PloneGlossary', 'Glossar')
        for i in range(100):
            term = invokeFactory(glossary, 'PloneGlossaryDefinition')
            term.setDefinition(gen_paragraphs(2))
            term.reindexObject()

    def installMessekalendar(self, site):
        service = site.restrictedTraverse('deutschland/de/service')
        cal = invokeFactory(service, 'EventFolder', 'Messekalendar')
        for i in range(10):
            event = invokeFactory(cal, 'Event')
            event.setLocation('Schwendi')
            event.setText(gen_paragraphs(3))
            event.setEventUrl('http://www.deutschland.de')
            event.setContactName('Heinz Becker')
            event.setContactEmail('info@deutschland.de')
            start = DateTime(random.randrange(2012, 2018), random.randrange(1,12), random.randrange(1,28))
            end = start + random.randrange(1,4)
            event.setStartDate(start)
            event.setEndDate(start)
            event.reindexObject()

    def installDownloads(self, site):
        pdf_filename = os.path.join(os.path.dirname(__file__), '..', 'data', 'prospekt.pdf')        
        pdf_data = file(pdf_filename, 'rb').read()
        service = site.restrictedTraverse('deutschland/de/service')
        dl = invokeFactory(service, 'Folder', 'Downloads')
        for i in range(10):
            title = gen_sentence()
            id = Normalizer().normalize(unicode(title, 'utf-8').lower())
            download = invokeFactory(dl, 'File')
            download.setFile(pdf_data)
            download.reindexObject()


    def installAssets(self, site):

        service = site.restrictedTraverse('deutschland/de/service')
        assets = invokeFactory(service, 'Folder', 'Assets')
        for width,height in ((200,200), (400,400), (600, 400), (800, 600), (800,800), (1024, 768)):
            imagefolder_id = '%sx%s' % (width, height)
            images = invokeFactory(assets, 'Folder', imagefolder_id)
            for i in range(20):
                img = invokeFactory(images, 'Image')
                img.setImage(random_image(width, height))
                img.reindexObject()
                    

    def installPressRoom(self, site):
        service = site.restrictedTraverse('deutschland/de/presse')
        pr = invokeFactory(service, 'PressRoom', 'Presse')
        for id in ('press-releases', 'press-clips', 'press-contacts'):
            pr[id].unindexObject()
            pr.manage_delObjects(id)
        for yr in range(2009, 2013):
            pr_yr = invokeFactory(pr, 'Folder', title=str(yr))
            for i in range(5):
                release = invokeFactory(pr_yr, 'PressRelease')
                release.setSubhead(gen_sentence())
                release.setDescription(gen_paragraphs(1))
                release.setText(gen_paragraphs(3))
                release.setImage(random_image(400,300))
                release.setImageCaption(gen_sentence())
                release.setReleaseDate(DateTime(yr, random.randint(1,12), random.randint(1, 28)))
                release.reindexObject()

