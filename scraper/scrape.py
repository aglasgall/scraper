#!/usr/bin/env python3
import json
import sys


from playwright.sync_api import sync_playwright

# Uncomment for debug logging
# os.environ['DEBUG'] = 'pw:api'

# Dependencies: `playwright` from pypi

# You must run `playwright install` in your virtualenv before using
# this!


def scrape_hunt_state(login_url,
                      puzzles_url,
                      username,
                      password,
                      browser_type="webkit"):
    """ Returns a dict representing the state of Hunt of the form
    { "round1":
        "Puzzle 1": {
          "name": "Puzzle 1",
          "url":  "https://www.example.com/puzzle/puzzle1",
          "solved": True|False,
          "answer": "answer if any"|None
        },
        ...
    }
    """
    hunt_state = {}

    with sync_playwright() as p:
        try:
            browser = getattr(p, browser_type).launch()
            ctx = browser.new_context()
            page = ctx.new_page()

            # log in
            page.goto(login_url)
            page.locator("#username").fill(username)
            page.locator("#password").fill(password)
            with page.expect_navigation():
                page.get_by_role("button", name="Submit").click()
            page.goto(puzzles_url)

            # scrapey scrapey
            rounds = page.locator("section.puzzle-list > div").all()
            for hunt_round in rounds:
                round_puzzles = {}
                name = hunt_round.locator("h3").inner_text()
                puzzles = hunt_round.locator(".puzzle").all()
                for p in puzzles:
                    link = p.locator("a")
                    pname = link.inner_text()
                    answer = (p.locator("pre").inner_text()) or None
                    round_puzzles[pname] = {"name": pname,
                                            "url": link.get_attribute("href"),
                                            "solved": answer is not None,
                                            "answer": answer }
                hunt_state[name] = round_puzzles
            return hunt_state
        finally:
            browser.close()


if __name__ == "__main__":
    res = scrape_hunt_state()
    json.dump(res, sys.stdout, indent=2)
    print()
