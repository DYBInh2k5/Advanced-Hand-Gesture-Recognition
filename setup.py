from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="advanced-hand-gesture-recognition",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Advanced Hand Gesture Recognition with AI, Computer Control and Recording",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DYBInh2k5/Advanced-Hand-Gesture-Recognition",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video :: Capture",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "isort>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gesture-recognition=advanced_main:main",
            "gesture-trainer=gesture_trainer:main",
        ],
    },
    keywords="hand gesture recognition computer vision AI mediapipe opencv",
    project_urls={
        "Bug Reports": "https://github.com/DYBInh2k5/Advanced-Hand-Gesture-Recognition/issues",
        "Source": "https://github.com/DYBInh2k5/Advanced-Hand-Gesture-Recognition",
        "Documentation": "https://github.com/DYBInh2k5/Advanced-Hand-Gesture-Recognition#readme",
    },
)