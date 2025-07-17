from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="currency-telegram-bot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sophisticated Telegram bot providing real-time currency exchange rates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/currency-telegram-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-telegram-bot[job-queue]>=21.10",
        "requests>=2.32.3",
    ],
    keywords="telegram bot currency exchange rates forex",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/currency-telegram-bot/issues",
        "Source": "https://github.com/yourusername/currency-telegram-bot",
        "Documentation": "https://github.com/yourusername/currency-telegram-bot#readme",
    },
)