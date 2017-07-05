# coding: utf-8
from setuptools import setup


with open('readme.rst') as f:
    readme = f.read()


setup(
    name='imgspy',
    version='0.1.1',
    description='Find the size or type of the image without '
                'fetching the whole content.',
    long_description=readme,
    url='https://github.com/nkanaev/imgspy',
    license='MIT',
    keywords='fastimage image size',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='Nazar Kanaev',
    author_email='nkanaev@live.com',
    py_modules=['imgspy'],
    test_suite='tests'
)
