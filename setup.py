from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='dtroslib',
    version='1.2.0',
    author='Hanyang University',
    url='https://github.com/DeepTaskHY/ROS.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
