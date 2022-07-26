import setuptools
import sys

version = '0.1'
homepage = 'https://github.com/jesfel/saferite'
description = 'Saferite Data Team Library'
requires = ['requests', 'boto3']

if sys.version_info < (3, 4):
    requires.append('enum34')

setuptools.setup(name='saferite',
      version=version,
      description=description,
      url=homepage,
      author='Saferite Data Team',
      author_email='jesfel@gmail.com',
      license='MIT',
      install_requires=requires,
      packages=['bcispapi', 'zohoapi', 'validation', 'googleRepricer', 'Information'],
      platforms=['OS Independent'],
      include_package_data=True,
      zip_safe=False)
