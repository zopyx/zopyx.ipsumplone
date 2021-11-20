from setuptools import setup, find_packages
import os

version = '0.4.0'

setup(name='zopyx.ipsumplone',
      version=version,
      description="Lorem ipsum text and image demo content for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        ],
      keywords='Plone Loremipsum',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/zopyx.ipsumplone',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zopyx'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'requests',
          'lorem-text',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
