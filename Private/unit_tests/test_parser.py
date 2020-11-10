from Private.parser import get_private_parser
from arpeggio import NoMatch
import pytest

valid_input_lines = ['winter = [e.Temperature for e in Events if "Winter" in e.Keywords and e.hasField("Temperature")]',
                     'summer = [e.Temperature for e in Events if "Summer" in e.Keywords and e.hasField("Temperature")]',
                     'winter ~ Normal(muWinter, sigma1)',
                     'summer ~ Normal(muSummer, sigma2)',
                     'muWinter ~ Normal(0, var1)',
                     'var1=100',
                     'muSummer ~ Normal(0, 100)',
                     'sigma1 ~ HalfNormal(100)',
                     'sigma2 ~ HalfNormal(100)',
                     'CILower = percentile(diff, 2.5)',
                     'CIUpper = percentile(diff, 97.5)',
                     'diff = muSummer - muWinter']
invalid_input_lines = [
    'winter = [e.Temperature for e in Events if "Winter" in e.Keywords and e.hasField("Temperature"), ]',
    'winter 8~ Normal(muWinter, sigma1,)*5',
    'muWinter ~ Normal(0, var1))',
    'muSummer ~ Normal(0, 100) * 5',
    'CILower = percentile(diff, 2.5 5)',
    'diff += muSummer - muWinter']


def test_valid_assignments():
    for input_line in valid_input_lines:
        parser = get_private_parser()
        parser.parse(input_line)
        assert True


def test_invalid_assignments():
    for input_line in invalid_input_lines:
        with pytest.raises(NoMatch):
            parser = get_private_parser()
            parser.parse(input_line)
