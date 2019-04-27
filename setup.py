# coding: utf-8
from setuptools import setup
from setuptools.command.test import test as TestCommand

import imgspy


class PyTestCommand(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def run_tests(self):
        import sys, pytest
        sys.exit(pytest.main([]))


setup(
    name='imgspy',
    version=imgspy.__version__,
    description='Find the size or type of the image without '
                'fetching the whole content.',
    long_description=imgspy.__doc__,
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
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={"test": PyTestCommand},
)
