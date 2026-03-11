from setuptools import setup, find_packages

setup(
    name='shared-libs',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Không cần dependencies, hoặc liệt kê nếu có (Django, ...)
    ],
)