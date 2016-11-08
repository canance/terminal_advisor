from setuptools import setup, find_packages
setup(
    name="terminal_advisor",
    version="1.0",
    packages=find_packages(),
    scripts=['terminal_advisor.py'],
    install_requires=['bs4', 'configparser', 'keyring', 'pdfkit', 'selenium'],
    package_data={
        '': ['LICENSE.txt'],
    },
    entry_points = {
        'console_scripts': ['terminal_advisor=terminal_advisor:main'],
    },
    # metadata for upload to PyPI
    author="Cory Nance",
    author_email="canance@coastal.edu",
    description="This script aims to automate mundane tasks in Webadvisor for faculty advisors.",
    license="MIT",
    keywords="webadvisor terminal_advisor",
    url="https://github.com/canance/terminaladvisor",   
)