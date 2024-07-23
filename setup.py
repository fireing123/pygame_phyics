from setuptools import setup, find_packages

setup(
    name='pygame_phyics',
    version='1.1.3',
    author= 'fireing123',
    author_email= 'gimd82368@gmail.com',
    url= 'https://github.com/fireing123/pygame_phyics',
    install_requires=["pygame", "box2d", "box2d-py"],
    packages=find_packages(),
    long_description=open('README.md', 'r', encoding="UTF8").read(),
    long_description_content_type='text/markdown',
)
