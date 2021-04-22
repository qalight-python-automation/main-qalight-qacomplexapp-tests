import logging
import random


def pytest_runtest_setup(item):
    """Prepare test"""
    log = logging.getLogger(item.name)
    item.cls.logger = log
    item.cls.variety = str(random.randint(10000000, 99999999))


class BaseTest:
    """BaseTest class for inheritance. Implements test class default variables."""
    # Defined to fix `unresolved attribute` warning
    # Default values to provide autocomplete
    logger = logging.getLogger(__name__)
    variety = str(random.randint(10000000, 99999999))
