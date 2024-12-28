from setuptools import setup, find_packages

setup(
    name="aittps",
    version="1.1.0",
    description="AITTPS SDK: Autonomous HTTPS for AI Agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/aittps",
    packages=find_packages(),
    install_requires=[
        "cryptography>=41.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
