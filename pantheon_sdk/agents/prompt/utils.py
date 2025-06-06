from jinja2 import Environment, PackageLoader


def get_environment(package_name: str) -> Environment:
    return Environment(loader=PackageLoader(package_name=package_name))
