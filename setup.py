from setuptools import setup

setup(
    name="grpcapi",
    version="0.2.0",
    author="Alexander Reynolds",
    author_email="alex@theory.shop",
    description="Define gRPC methods with decorators",
    packages=["grpcapi"],
    install_requires=["grpcio", "protobuf"],
    extras_require={"dev": ["black", "mypy", "grpcio-tools"]},
    license="MIT",
    package_data={
        "grpcapi": ["py.typed"],
    },
)
