from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')

setup(
   name='speteval',
   version='0.0.1',
   description='A useful module',
   license="MIT",
   author='Mahmoud Salhab',
   author_email='mahmoud@salhab.work',
   packages=['speteval'],
   install_requires=requirements,
   exclude=[
       'env',
       'speteval/__pycache__'
       ]
)
