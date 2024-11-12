from setuptools import setup, find_packages
from mental_math_bot.version import VERSION


# Function to read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line and not line.startswith('#')]


requirements = parse_requirements('requirements.txt')

setup(
    name='mental_math_bot',
    version=VERSION,
    packages=find_packages(),
    install_requires=requirements,  # List of dependencies
    entry_points={'console_scripts': ['mental-math-bot=mental_math_bot:start_bot']},
    include_package_data=False,  # package data is not defined in MANIFEST.in for a moment
    python_requires='>=3.10',
    platforms=['any'],
)
