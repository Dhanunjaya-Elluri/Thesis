__author__ = "Dhanunjaya Elluri"
__mail__ = "dhanunjaya.elluri@tu-dortmund.de"

import pytest
from utils.config import load_config


def test_config():
    config = load_config(file_name="params.yaml")
    assert config["training"]["epochs"] == 100
