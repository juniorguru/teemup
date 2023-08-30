import json
from datetime import datetime
from typing import Any

from lxml import html


def parse(content: str) -> list[dict[str, Any]]:
    html_tree = html.fromstring(content)
    next_data = json.loads(html_tree.cssselect("#__NEXT_DATA__")[0].text_content())
    apollo_state = next_data["props"]["pageProps"]["__APOLLO_STATE__"]
    venues = {
        key: venue for key, venue in apollo_state.items() if key.startswith("Venue:")
    }
    return [
        dict(
            title=event["title"],
            description=event["description"],
            starts_at=datetime.fromisoformat(event["dateTime"]),
            ends_at=datetime.fromisoformat(event["endTime"]),
            venue=parse_venue(venues[event["venue"]["__ref"]]),
            url=event["eventUrl"],
        )
        for key, event in apollo_state.items()
        if (
            key.startswith("Event:")
            and event["status"] == "ACTIVE"
        )
    ]


def parse_venue(venue: dict) -> dict:
    return {
        "name": venue.get("name") or None,
        "address": venue.get("address") or None,
        "city": venue.get("city") or None,
        "state": venue.get("state") or None,
        "country": venue.get("country") or None,
    }
