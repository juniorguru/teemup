import json
from datetime import datetime
from typing import Any

from lxml import html


def parse(response_content: str) -> list[dict[str, Any]]:
    html_tree = html.fromstring(response_content)
    next_state = json.loads(html_tree.cssselect("#__NEXT_DATA__")[0].text_content())
    return parse_next_state(next_state)


def parse_next_state(next_state: dict) -> list[dict[str, Any]]:
    apollo_state = next_state["props"]["pageProps"]["__APOLLO_STATE__"]
    venues = {
        key: venue for key, venue in apollo_state.items() if key.startswith("Venue:")
    }
    return [
        dict(
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


def parse_venue(venue: dict) -> dict | None:
    result = {}
    for key in ["name", "address", "city", "state", "country"]:
        result[key] = venue.get(key) or None
    if (
        result["name"]
        and result["name"].lower() == "online event"
        and result["address"] is None
        and result["city"] is None
        and result["state"] is None
        and result["country"] is None
    ):
        return None
    return result
