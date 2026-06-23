from setuptools import setup


package_name = "wall_e_bringup"


setup(
    name=package_name,
    version="0.0.0",
    py_modules=["bringup_launch"],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", ["launch/bringup.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="nekochiraa",
    maintainer_email="nekochiraa@todo.todo",
    description="Wall-E bringup package.",
    license="TODO",
)
