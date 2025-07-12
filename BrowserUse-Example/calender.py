import os, asyncio
from browser_use import Agent, BrowserProfile
from langchain_openai import ChatOpenAI   # or any LLM you prefer


async def main():
    profile = BrowserProfile(
        # launch the Chrome I already use
        executable_path="/usr/bin/google-chrome",

        # reuse the profile that is already signed-in
        user_data_dir=os.path.expanduser("~/.config/google-chrome"),
        chromium_args=["--profile-directory=Default"],

        # window / sandbox / display settings
        headless=False,
        chromium_sandbox=False, # required on most Ubuntu Chrome installs
        env={
            "DISPLAY": os.environ["DISPLAY"],
            "XAUTHORITY": os.environ.get("XAUTHORITY", "")
        },
        keep_alive=True, # keep Chrome open after the agent finishes
    )

    initial_actions = [
        {"open_tab": {"url": "https://calendar.google.com/calendar/u/0/r?pli=1"}},
    ]

    event_details = {
        "title": "Meeting with Ali",
        "date": "2025-07-13",  # YYYY-MM-DD format
        "start_time": "06:00 PM",  # Time must be in 12-hour format (e.g., 08:00 PM)
        "end_time": "06:30 PM",    # Time must be in 12-hour format (e.g., 09:30 PM)
        "guest_email": "hassan@gmail.com"
    }


    agent = Agent(
    task=f"""
            open Google Calendar (https://calendar.google.com/calendar/u/0/r?pli=1)
            click on create button,
            click on event,
            add title '{event_details["title"]}',
            set date to today '{event_details["date"]}',
            set time to '{event_details["start_time"]}' to '{event_details["end_time"]}',
            add guest email address: {event_details["guest_email"]},
            click save button,
            then open the calendar and check if the event is created correctly.
            during the process when asked by Google calender:"Would you like to send invitation emails to Google Calendar guests?" Click on "Send" button.
    """,
        browser_profile=profile,
        llm=ChatOpenAI(model="gpt-4o"),
        #initial_actions=initial_actions,
    )
    await agent.run()

asyncio.run(main())
