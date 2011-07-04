from setuptools import setup, find_packages
import re
def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links

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
      install_requires = parse_requirements('requirements.txt'),
      dependency_links = parse_dependency_links('requirements.txt'),
      version='1.3.3',
)
