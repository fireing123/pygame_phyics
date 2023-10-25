from setuptools import setup, find_packages

setup(
    name='pygame_phyics',
    version='0.4.0',
    author= 'fireing123',
    author_email= 'gimd82368@gmail.com',
    url= 'https://github.com/fireing123/pygame_phyics',
    install_requires=["pygame", "box2d-py"],
    packages=find_packages(),
)