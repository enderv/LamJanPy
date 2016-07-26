from Janitor import Janitor
import pytest
import copy
base_test_object = {'regions': ['us-east-1'],
               'resources_to_check': ['test'],
               'required_tags':
                   {'Lambda': ['name']},
               'use_rules':
                   {'Lambda': 1}}


def test_bad_regions_config():
    with pytest.raises(TypeError) as execinfo:
        test_object = copy.deepcopy(base_test_object)
        test_object['regions'] = 1
        Janitor(test_object)
    assert 'regions must be a list' in str(execinfo.value)


def test_bad_regions_data():
    with pytest.raises(ValueError) as execinfo:
        test_object = copy.deepcopy(base_test_object)
        test_object['regions'] = ['string']
        Janitor(test_object)
    assert 'string are not valid regions' in str(execinfo.value)


def test_bad_resources_data_type():
    with pytest.raises(TypeError) as execinfo:
        test_object = copy.deepcopy(base_test_object)
        test_object['resources_to_check'] = 1
        Janitor(test_object)
    assert 'resources_to_check must be a list' in str(execinfo.value)


def test_bad_resources():
    with pytest.raises(ValueError) as execinfo:
        test_object = copy.deepcopy(base_test_object)
        test_object['resources_to_check'] = ['test']
        Janitor(test_object)
    assert 'test is not a valid resource to check' in str(execinfo.value)


def test_bad_tags_data():
    with pytest.raises(TypeError) as execinfo:
        test_object = copy.deepcopy(base_test_object)
        test_object['required_tags'] = ['test']
        Janitor(test_object)
    assert 'required_tags must be a dict' in str(execinfo.value)

def test_bad_rules_data():
    with pytest.raises(TypeError) as execinfo:
        test_object = copy.deepcopy(base_test_object)
        test_object['use_rules'] = ['test']
        Janitor(test_object)
    assert 'use_rules must be a dict' in str(execinfo.value)


