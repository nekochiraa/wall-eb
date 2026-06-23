from setuptools import setup


package_name = "wall_e_audio"


setup(
    name=package_name,
    version="0.0.0",
    py_modules=["output"],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (
            f"share/{package_name}",
            ["fr_FR-gilles-low.onnx", "fr_FR-gilles-low.onnx.json"],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="nekochiraa",
    maintainer_email="nekochiraa@todo.todo",
    description="Wall-E audio node.",
    license="TODO",
    entry_points={
        "console_scripts": [
            "tts = output:main",
        ],
    },
)
