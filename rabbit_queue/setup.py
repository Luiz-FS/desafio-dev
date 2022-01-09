from setuptools import find_packages, setup

requirements = ["python-decouple==3.4", "pika==1.2.0"]

setup(
    name="rabbit_queue",
    version="0.0.0",
    description="Service to facilitate and centralize libraries used to access RabbitMQ.",
    author="Nuveo",
    url="https://github.com/luiz-fs/desafio-dev/tree/master/rabbit_queue",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
