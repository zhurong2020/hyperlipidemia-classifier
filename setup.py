from setuptools import setup, find_packages
import os

# 从VERSION文件读取版本号
with open('VERSION') as f:
    version = f.read().strip()

setup(
    name="lipid-risk-assessor",
    version=version,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'flask>=2.0.1',
        'gunicorn>=20.1.0',
    ],
    author="zhurong2020",
    author_email="zhurong0525@icloud.com",
    description="A lipid risk assessment tool based on Chinese guidelines",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhurong2020/hyperlipidemia-classifier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 