from setuptools import setup, find_packages # type: ignore

setup(
    name='vkdump',
    version='0.4',
    description='Tool for backing up VK favorites, walls and profiles',
    url='https://github.com/karlicoss/vkdump',
    author='Dmitrii Gerasimov',
    author_email='karlicoss@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Multimedia',
    ],
    license='MIT',
    keywords='vk backup download',

    packages=find_packages(),

    # TODO data_files ???

    test_suite='nose.collector',

    tests_require=[
        'nose',
        'pyhamcrest',
    ],
    install_requires=[
        'atomicwrites',
        'backoff',

        'vk>=2.0.2',

        'click',  # CLI
        'coloredlogs',

        'pytz',  # time zones handling

        'injector',  # dependency injector

        'typing',
    ],
    zip_safe=False,
)
