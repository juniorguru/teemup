# teemup

_If Meetup didn't become a walled garden, the world wouldn't need Teemup_

## Purpose and scope

This library takes HTML source of a meetup group page on Meetup and returns a list of their upcoming events.

## Usage

```python
>>> import urllib.request
>>> from teemup import parse
>>> with urllib.request.urlopen('https://www.meetup.com/dresdenjs-io-javascript-user-group/') as f:
...     html = f.read()
...
>>> events = parse(html)
>>> event = next(event for event in events if event['venue'] is not None)
>>> sorted(event.keys())
['description', 'ends_at', 'starts_at', 'title', 'url', 'venue']
>>> sorted(event['venue'])
['address', 'city', 'country', 'name', 'state']

```

The example above is [tested](https://docs.pytest.org/doctest.html) and thus doesn't contain any variable data, but should be enough to give you an idea.

## If something breaks

If the website changes, update the fixture:

```
curl https://www.meetup.com/reactgirls/ > test_fixtures/response_content.html
```

Then run `poetry run pytest`.
Change `teemup.py` and add unit tests to `test_teemup.py` as needed.
Then cut a new release:

-   Make sure the tests really pass: `poetry run pytest`
-   Format the code: `poetry run black .`
-   Raise the version number in `pyproject.toml`
-   Commit the changes: `git commit -am "release vX.Y.Z"`
-   Create a version tag: `git tag vX.Y.Z`
-   Push the tag: `git push --tags`

**Note:** If there are no upcoming events, choose a different group page for testing.
Do not remove live testing from the repository!
The whole purpose of the library is to be up-to-date with the current website.
It must be monitored every day and fixed as soon as it breaks.

## Why

Meetup used to be a nice and friendly platform where to host your events.
It used to have an iCalendar export, RSS export, Atom export.

Such exports are useful if one wants to follow certain meetup in their own calendar software, or if one wants to read the event feed by a program and automatically link to upcoming events from a website – effectively sending more people to the events and more potential users to Meetup.

In March 2023 they've put these exports behind login, basically rendering them useless.
You can download the files manually, but automatic fetching for future events is impossible.
They do have an API (with horrendous auth flow), but that API is reserved to paying users only.

After a long conversation with their support (June 2023), they confirmed the login is intentional, but they couldn't explain why they did such product decision and how it benefits their users.
From that point on, I consider Meetup to be a hostile walled garden, which contributes to harming the free and open internet.

All my integrations broke down, and [not only mine](https://wordpress.org/support/topic/trouble-with-meetup-calendars-please-read/).

I figured out they left [JSON-DL](https://schema.org/) meta data on the page.
Such meta data is good for search engines and other tooling and can be read by [extruct](https://github.com/scrapinghub/extruct/).
This allowed me to fix everything for a while, but in August 2023, the JSON-DL has also disappeared from the website.

All out war then!
I moved the code to this separate library so it's easier to develop, re-use, contribute to, and monitor.

## License

[MIT](LICENSE)
