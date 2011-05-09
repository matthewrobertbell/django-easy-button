from setuptools import setup, find_packages

DESCRIPTION = "django-easy-button: making rapid django development suck less"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django',
    'Topic :: Database',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: BSD License',
]

setup(name='django-easy-button',
      packages=find_packages(exclude=('tests', 'tests.*')),
      author='Leeward Bound Corp',
      author_email='code@lwb.co',
      url='http://www.github.com/linked/django-easy-button',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      classifiers=CLASSIFIERS,
      install_requires=[],
      version='1.3.3',
)
