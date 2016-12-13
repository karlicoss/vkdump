from setuptools import setup, find_packages

setup(
    name='vkdump',
    version='0.1.1',
    description='Tool for backing up VK favorites and walls',
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

        'vk>=2.0.2',

        'click',  # CLI

        'pytz',  # time zones handling

        'injector',  # dependency injector

        'typing',
    ],
    zip_safe=False,
)
