import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
import sys
import askbot_audit

setup(
    name = "askbot_audit",
    version = askbot_reports.__version__,#remember to manually set this correctly
    description = 'Module allowing auditing of content in Askbot',
    packages = find_packages(),
    author = 'Evgeny.Fadeev',
    author_email = 'evgeny.fadeev@gmail.com',
    url = 'http://askbot.org/en/questions/',
    include_package_data = True,
)
