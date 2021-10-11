from setuptools import setup, find_packages

setup(name='gnt-core',
      version='1.0',
      description='Core for SBLGNT clusterer application',
      author='Sophie Robert',
      find_packages=find_packages(),
      entry_points = {
        'console_scripts': ['fill_database=gnt_core.database_filler:fill'],
    }
      )
