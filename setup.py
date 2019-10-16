from setuptools import setup

setup(
    name="alignschema",
    version="0.0.1",

    author="Neil Freeman",
    author_email="contact@fakeisthenewreal.org",
    packages=["alignschema"],
    entry_points={
        'console_scripts': [
            'alignschema=alignschema.__main__:main',
        ],
    },
)
