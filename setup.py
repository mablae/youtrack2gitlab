from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='youtrack2gitlab',
      version='0.0.1',
      description=u"Set of scripts to migrate youtrack issues to gitlab",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Malte Blättermann",
      author_email='mbl@svb.de',
      url='https://github.com/mablae/youtrack2gitlab',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click', 'requests', 'pyapi-gitlab'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      y2g_import=youtrack2gitlab.scripts.cli:cli
      y2g_projects=youtrack2gitlab.scripts.getProjects:cli
      y2g_users=youtrack2gitlab.scripts.getUsers:cli
      """
      )
