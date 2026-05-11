#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Health Stack System — Django Management Entry Point
"""
import os
import sys
import logging

logger = logging.getLogger(__name__)


def main():
    """
    Run administrative tasks for the Health Stack System.

    Sets the default Django settings module to 'healthstack.settings'
    and delegates all commands to Django's management framework.

    Usage:
        python manage.py runserver
        python manage.py migrate
        python manage.py createsuperuser
        python manage.py collectstatic
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthstack.settings')

    # Minimum Python version check
    if sys.version_info < (3, 8):
        sys.stderr.write(
            "[ERROR] Health Stack System requires Python 3.8 or higher.\n"
            f"        You are running Python {sys.version}\n"
        )
        sys.exit(1)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "\n[ERROR] Could not import Django.\n"
            "  → Make sure Django is installed:  pip install django\n"
            "  → Make sure your virtual environment is activated.\n"
            "  → Check that PYTHONPATH is configured correctly.\n"
        ) from exc

    logger.debug("Django settings module: %s", os.environ['DJANGO_SETTINGS_MODULE'])
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
