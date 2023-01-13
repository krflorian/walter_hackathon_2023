from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent

# This is THE standard way to share packages in Python world
# see https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html
setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    name="truck_agent",
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version="1.0.0",
    # This should be the name of the organization which owns the
    # project.
    author="WALTER GROUP",
    author_email="",
    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    package_dir={"": "src"},
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where="src"),
    # scripts=['bin/script1','bin/script2'],
    url="https://www.waltergroup.com",
    license="LICENSE",
    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Python truck agent for WALTER GROUP Hackathon: Sustainable Logistics",
    # Optional full description, that is usually matches README
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=(this_directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",  # Optional (see note above)
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will run_check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.8, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    #
    #
    # THIS is the minimal set of requirements that the model needs to PREDICT
    install_requires=["fastapi", "uvicorn"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'requests'],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `mycli` which
    # executes the cli entrypoint within the cli.py. It is built with click
    entry_points={  # Optional
        "console_scripts": ["run=truck_agent.main:main"],
    },
    zip_safe=False,
    # to include additional files from MANIFEST.in
    include_package_data=True,
)

