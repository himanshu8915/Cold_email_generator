from setuptools import setup, find_packages

setup(
    name="cold-email-generator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.25.0",
        "langchain>=0.1.0",
        "langchain-groq>=0.1.0",
        "chromadb>=0.4.18",
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "pandas>=2.0.3",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        'console_scripts': [
            'cold-email-generator=app:main',
        ],
    },
)
