from setuptools import setup

setup(name='valhallapy',
      version='0.1.1',
      description='Python Wrapper for the MapZen\'s routing engine Valhalla ',
      url='http://github.com/stuartlynn/valhallapy',
      author='Stuart Lynn',
      author_email='slynn@cartodb.com',
      license='MIT',
      install_requires=['shapely','json','requests'],
      packages=['valhallapy'],
      zip_safe=False)
