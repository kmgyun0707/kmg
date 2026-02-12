from setuptools import find_packages, setup

package_name = 'my_first_package'

# Setup function to define the package
# 이 부분은 패키지 설정을 정의하는 setup 함수입니다.
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']), # 'test' 디렉토리를 제외한 모든 패키지를 찾습니다.
    data_files=[ # 패키지에 포함될 데이터 파일들을 정의합니다.
        ('share/ament_index/resource_index/packages', #(복사할 경로, 복사될 경로) 형식의 튜플 리스트입니다.
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='i',
    maintainer_email='i@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_first_node = my_first_package.my_first_node:main', # my_first_node라는 콘솔 스크립트를 정의합니다.
            'my_subscriber = my_first_package.my_first_subscriber:main',
            'my_publisher  = my_first_package.my_first_publisher:main',
            'my_temp_sub  = my_first_package.my_second_subscriber:main',
            'my_temp_pub  = my_first_package.my_second_publisher:main'
        ],
    },
    #엔트리 포인트는 패키지 내에서 실행 가능한 스크립트를 정의하는 데 사용됩니다.
    #-> 콘솔에서 직접 실행할 수 있는 명령어를 지정합니다.<-
)
