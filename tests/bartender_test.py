import pytest
import json
import argparse
from .context import Bartender
from pytestqt import qtbot

@pytest.fixture
def bartenderFixture(qtbot):
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", dest="sim",help="Run bartender without GPIO", action="store_true")
    args = parser.parse_args()
    args.sim = True
    bartender = Bartender(args)
    return bartender

def test_pump_config_1(bartenderFixture: Bartender):
    testPath = "./utils/support_test_files/pumpConfig1.json"
    pumpConfig = bartenderFixture.readPumpConfiguration(testPath)
    tempConfig = json.load(open(testPath))  
    pumpConfig, tempConfig = json.dumps(pumpConfig, sort_keys=True), json.dumps(tempConfig, sort_keys=True)   
    assert tempConfig == pumpConfig  

def test_pump_config_2(bartenderFixture: Bartender):
    testPath = "./utils/support_test_files/pumpConfig2.json"
    pumpConfig = bartenderFixture.readPumpConfiguration(testPath)
    tempConfig = json.load(open(testPath))
    pumpConfig, tempConfig = json.dumps(pumpConfig, sort_keys=True), json.dumps(tempConfig, sort_keys=True)   
    assert tempConfig == pumpConfig
