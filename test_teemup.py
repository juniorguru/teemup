import pytest
from teemup import parse_venue, parse


@pytest.fixture
def content():
    with open("test_fixture.html") as f:
        return f.read()


def test_parse_produces_timezone_aware_starts_at(content: str):
    events = parse(content)

    assert all([event["starts_at"].tzinfo for event in events])


def test_parse_produces_timezone_aware_ends_at(content: str):
    events = parse(content)

    assert all([event["ends_at"].tzinfo for event in events])


def test_parse_produces_expected_keys(content: str):
    events = parse(content)

    assert sorted(events[0].keys()) == ['description', 'ends_at', 'starts_at', 'title', 'url', 'venue']


def test_parse_produces_expected_venue_keys(content: str):
    events = parse(content)

    assert sorted(events[0]['venue'].keys()) == ['address', 'city', 'country', 'name', 'state']


def test_parse_venue():
    venue = {
        "__typename": "Venue",
        "id": "27152599",
        "name": "Pipedrive",
        "address": "Pernerova 697/35, Karlín",
        "city": "Praha-Praha 8",
        "state": "",
        "country": "cz",
    }

    assert (
        parse_venue(venue)
        == {
            "name": "Pipedrive",
            "address": "Pernerova 697/35, Karlín",
            "city": "Praha-Praha 8",
            "state": None,
            "country": "cz",
        }
    )
