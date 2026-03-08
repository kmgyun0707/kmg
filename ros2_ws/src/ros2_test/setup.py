from setuptools import find_packages, setup

package_name = 'ros2_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rokey',
    maintainer_email='kmgyun0707@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tile_rotation_node = ros2_test.tile_rotation_node:main',
            'make_dataset = ros2_test.make_dataset:main',
            'tile_rotation_node_ir = ros2_test.tile_rotation_node_ir:main',
        ],
    },
)
