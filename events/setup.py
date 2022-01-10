from setuptools import find_packages, setup

setup(
    name="events",
    version="1.0.0",
    description="Events",
    author="Luiz",
    author_email="luiz.silva@ccc.ufcg.edu.br",
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest",
        "pytest-flake8",
        "pytest-cov",
        "retry",
        "freezegun",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["runevent=events.main:main"]},
)
