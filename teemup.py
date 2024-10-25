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
    group_name: str | None


def parse(response_content: str) -> list[Event]:
    html_tree = html.fromstring(response_content)
    next_state = json.loads(html_tree.cssselect("#__NEXT_DATA__")[0].text_content())
    return parse_next_state(next_state)


def parse_next_state(next_state: dict) -> list[Event]:
    page_props = next_state["props"]["pageProps"]
    apollo_state = page_props["__APOLLO_STATE__"]
    groups = select_typename(apollo_state, "Group")
    venues = select_typename(apollo_state, "Venue")
    return [
        Event(
            title=event["title"],
            url=event["eventUrl"],
            description=event["description"],
            starts_at=datetime.fromisoformat(event["dateTime"]),
            ends_at=datetime.fromisoformat(event["endTime"]),
            venue=(
                parse_venue(venues[event["venue"]["__ref"]]) if event["venue"] else None
            ),
            group_name=groups[event["group"]["__ref"]]["name"],
        )
        for event in select_typename(apollo_state, "Event").values()
        if event["status"] == "ACTIVE"
    ]


def select_typename(apollo_state: dict, typename: str) -> dict[str, dict]:
    return {
        key: value
        for key, value in apollo_state.items()
        if value["__typename"] == typename
    }


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
