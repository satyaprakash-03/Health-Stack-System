import setuptools
from pathlib import Path

# Read long description from README
long_description = Path("README.md").read_text(encoding="utf-8")

setuptools.setup(
    # ── Package Identity ──────────────────────────────────────────
    name             = "sslcommerz-lib",
    version          = "1.2.0",
    description      = "SSLCommerz Payment Gateway integration library for Python",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    # ── Author Info ───────────────────────────────────────────────
    author       = "SSLCOMMERZ Developers",
    author_email = "sajan.sslwireless@gmail.com",
    url          = "https://github.com/sajanPoddar/sslcommerz-lib-py",

    # ── Keywords & Packages ───────────────────────────────────────
    keywords = ["sslcommerz", "payment", "gateway", "bangladesh", "fintech"],
    packages = setuptools.find_packages(exclude=["tests*", "data*", "build*"]),

    # ── Dependencies ──────────────────────────────────────────────
    python_requires  = ">=3.8",
    install_requires = [
        "requests>=2.25.0",
    ],

    # ── PyPI Classifiers ──────────────────────────────────────────
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
    ],

    # ── Project URLs ──────────────────────────────────────────────
    project_urls = {
        "Bug Tracker" : "https://github.com/sajanPoddar/sslcommerz-lib-py/issues",
        "Documentation": "https://developer.sslcommerz.com/",
        "Source Code" : "https://github.com/sajanPoddar/sslcommerz-lib-py",
    },
)
