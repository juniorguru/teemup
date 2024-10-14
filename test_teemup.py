import json
import pytest
from teemup import parse_next_state, parse_venue, parse


@pytest.fixture
def response_content() -> str:
    with open("test_fixtures/response_content.html") as f:
        return f.read()


def test_parse_produces_timezone_aware_starts_at(response_content: str):
    events = parse(response_content)

    assert all([event["starts_at"].tzinfo for event in events])


def test_parse_produces_timezone_aware_ends_at(response_content: str):
    events = parse(response_content)

    assert all([event["ends_at"].tzinfo for event in events])


def test_parse_produces_expected_keys(response_content: str):
    events = parse(response_content)

    assert sorted(events[0].keys()) == [
        "description",
        "ends_at",
        "starts_at",
        "title",
        "url",
        "venue",
    ]


def test_parse_produces_expected_venue_keys(response_content: str):
    events = parse(response_content)
    venue = events[0]["venue"]

    assert venue is not None
    assert sorted(venue.keys()) == [
        "address",
        "city",
        "country",
        "name",
        "state",
    ]


def test_parse_next_state_can_deal_with_missing_venue():
    with open("test_fixtures/next_state_missing_venue.json") as f:
        next_state = json.load(f)
    events = parse_next_state(next_state)
    event_with_missing_venue = [event for event in events if event["venue"] is None][0]

    assert sorted(event_with_missing_venue.keys()) == [
        "description",
        "ends_at",
        "starts_at",
        "title",
        "url",
        "venue",
    ]


def test_parse_next_state_can_deal_with_online_venue():
    with open("test_fixtures/next_state_online_venue.json") as f:
        next_state = json.load(f)
    events = parse_next_state(next_state)
    event_with_online_venue = [event for event in events if event["venue"] is None][0]

    assert sorted(event_with_online_venue.keys()) == [
        "description",
        "ends_at",
        "starts_at",
        "title",
        "url",
        "venue",
    ]


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

    assert parse_venue(venue) == {
        "name": "Pipedrive",
        "address": "Pernerova 697/35, Karlín",
        "city": "Praha-Praha 8",
        "state": None,
        "country": "cz",
    }


def test_parse_online_venue():
    venue = {
        "__typename": "Venue",
        "id": "26906060",
        "name": "Online event",
        "address": "",
        "city": "",
        "state": "",
        "country": "",
    }

    assert parse_venue(venue) is None
