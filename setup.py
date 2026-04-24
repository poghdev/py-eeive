from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="py-eeive",
    version="1.1.0",
    author="Poghoosyann",
    author_email="poghoosyann@gmail.com",
    description="Monitor your Python scripts with one decorator — retries, timing, and smart error explanations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poghdev/py-eeive",
    license="MIT",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.7",
    install_requires=[
        "psutil>=5.0.0",
    ], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="monitor, retry, decorator, logging, error-handling",
    project_urls={
        "Bug Tracker": "https://eeive.com",
    },
)