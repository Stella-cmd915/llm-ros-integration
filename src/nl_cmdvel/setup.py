from setuptools import setup

package_name = "nl_cmdvel"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/nl_cmdvel.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Maintainer",
    maintainer_email="maintainer@example.com",
    description="Natural-language command to /cmd_vel bridge for ROS 2 (Jazzy)",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "nl_cmdvel_node = nl_cmdvel.nl_cmdvel_node:main",
        ],
    },
)
