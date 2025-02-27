from setuptools import setup, find_packages

setup(
    name="lipid-risk-assessor",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        'tkinter',  # 通常内置于Python
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