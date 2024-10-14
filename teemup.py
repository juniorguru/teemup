import json
from datetime import datetime
from typing import TypedDict

from lxml import html


class Venue(TypedDict):
    name: str
    address: str | None
    city: str | None
    state: str | None
    country: str | None


class Event(TypedDict):
    title: str
    url: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue: Venue | None


def parse(response_content: str) -> list[Event]:
    html_tree = html.fromstring(response_content)
    next_state = json.loads(html_tree.cssselect("#__NEXT_DATA__")[0].text_content())
    return parse_next_state(next_state)


def parse_next_state(next_state: dict) -> list[Event]:
    apollo_state = next_state["props"]["pageProps"]["__APOLLO_STATE__"]
    venues = {
        key: venue for key, venue in apollo_state.items() if key.startswith("Venue:")
    }
    return [
        Event(
            title=event["title"],
            description=event["description"],
            starts_at=datetime.fromisoformat(event["dateTime"]),
            ends_at=datetime.fromisoformat(event["endTime"]),
            venue=(
                parse_venue(venues[event["venue"]["__ref"]]) if event["venue"] else None
            ),
            url=event["eventUrl"],
        )
        for key, event in apollo_state.items()
        if (key.startswith("Event:") and event["status"] == "ACTIVE")
    ]


def parse_venue(venue: dict) -> Venue | None:
    data = {}
    for key in ["name", "address", "city", "state", "country"]:
        data[key] = venue.get(key) or None
    if (
        data["name"]
        and data["name"].lower() == "online event"
        and data["address"] is None
        and data["city"] is None
        and data["state"] is None
        and data["country"] is None
    ):
        return None
    return Venue(**data)
