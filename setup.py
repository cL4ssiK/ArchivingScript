from setuptools import setup
setup(
    name='arkistoi',
    version='0.0.1',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'arkistoi=arkistoi:main'
        ]
    }
)