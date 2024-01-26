from setuptools import setup, find_packages

setup(name='clusterer-core',
      version='1.0',
      description='Core for Bible clusterer application',
      author='Sophie Robert',
      packages=["clusterer_core"],
      entry_points = {
        'console_scripts': ['fill_database=gnt_core.database_filler:fill'],
    }
      )
