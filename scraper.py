from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def scrape_jobs():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        # LinkedIn Login
        page.goto("https://www.linkedin.com/login")

        time.sleep(2)

        page.fill("#username", EMAIL)
        page.fill("#password", PASSWORD)

        page.click("button[type='submit']")

        time.sleep(5)

        # Search Jobs
        page.goto(
            "https://www.linkedin.com/jobs/search/?keywords=Java%20Developer"
        )

        time.sleep(8)

        jobs = []

        cards = page.locator(".job-card-container")

        count = cards.count()

        print(f"Found {count} jobs")

        for i in range(min(count, 10)):

            card = cards.nth(i)

            try:

                title = card.locator(".job-card-list__title").inner_text()

            except:
                title = "N/A"

            try:

                company = card.locator(".artdeco-entity-lockup__subtitle").inner_text()

            except:
                company = "N/A"

            try:

                link = card.locator("a").first.get_attribute("href")

            except:
                link = "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "recruiter_email": "recruiter@example.com"
            })

            print(title, "-", company)

        df = pd.DataFrame(jobs)

        df.to_csv("jobs.csv", index=False)

        print("jobs.csv created successfully")

        time.sleep(5)

        browser.close()

scrape_jobs()