from hashlib import sha256
import secrets

import pytest

from src.sha256 import calculate_sha256


test_case_list =  [{'message': i.encode(), 'correct_result': sha256(i.encode()).hexdigest()} for i in [secrets.token_hex(i)for i in range(25)]]


@pytest.fixture
def case(request):
    return request.param



@pytest.mark.parametrize('case', test_case_list, indirect=True)
def test_calculate_sha256_message_digest(case):
    message = case['message']
    message_digest = case['correct_result']

    assert calculate_sha256(message) == message_digest

