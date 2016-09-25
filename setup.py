from setuptools import setup, find_packages

setup(
    name='vkdump',
    version='0.1',
    description='Tool for backing up VK favorites',
    url='https://bitbucket.org/karlicoss/vkdump',
    author='Dmitrii Gerasimov',
    author_email='karlicoss@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Multimedia',
    ],
    license='MIT',
    keywords='vk backup download',

    packages=find_packages('vkdump'),

    package_data={'vkdump': ['resources/*']},
    include_package_data=True,

    # TODO data_files ???

    test_suite='nose.collector',

    tests_require=[
        'nose',
        'pyhamcrest',
    ],
    install_requires=[
        'vk>=2.0.2',

        # 'dataset',  # database helper
        # 'jsonpickle',  # for [de]serialization
        # TODO: sqlalchemy?

        'click',  # CLI

        'dominate',  # rendering
        'dominatepp>=0.2',

        'pytz',  # time zones handling

        'injector',  # dependency injector

        'typing',
    ],
    dependency_links=[
        'git+https://github.com/karlicoss/dominatepp.git#egg=dominatepp-0.2',
    ],
    zip_safe=False,
)
