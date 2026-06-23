from setuptools import setup


package_name = "wall_e_content"


setup(
    name=package_name,
    version="0.0.0",
    py_modules=["content"],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="nekochiraa",
    maintainer_email="nekochiraa@todo.todo",
    description="Wall-E content node.",
    license="TODO",
    entry_points={
        "console_scripts": [
            "content = content:main",
        ],
    },
)
