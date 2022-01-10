from setuptools import find_packages, setup

requirements = ["python-decouple==3.5", "pika==1.2.0"]

setup(
    name="rabbit_queue",
    version="0.0.0",
    description="Service to facilitate and centralize libraries used to access RabbitMQ.",
    author="Luiz",
    author_email="luiz.silva@ccc.ufcg.edu.br",
    url="https://github.com/luiz-fs/desafio-dev/tree/main/rabbit_queue",
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest",
        "pytest-flake8",
        "pytest-cov",
        "retry",
        "freezegun",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
