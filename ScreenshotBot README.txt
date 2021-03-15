ScreenshotBot Requirements

Py Libraries:
asyncio (Install on: Client, Version: no specific version)
pyppeteer (Install on: Client, Version: no specific version, Notes: will install its own prereqs at runtime)
pathlib (Install on: Client and Server, Version: no specific version, Notes: has to be added to requirements.txt ex: pathlib>=1.0.0)

Directories:
Folder called HTML with otree source stylers and bootstrap folders included as well as the global folder from _static
Folder called Screenshots

Code:
"snap" and "semantic_diff" functions in custom_funcs.py
"from custom_templates.custom_funcs import snap" in the tests.py for every traversed app
"snap()" before every "yield" or "pass" statement (if you want the page to capture) in the tests.py for every traversed app
"screenshot=False, use_browser_bots=False," in the SESSION_CONFIG_DEFAULTS dict in settings.py
htmlToScreenshots.py in the dir at the same level as settings.py (not in a subfolder)

Use Notes:
Create a new session as if you're running it with browser bots
(I recommend the minimum number of players for the selected group size)
Make sure to check the "screenshot" and "use_browser_bots" buttons under "Configure session"
Run as you would normally opening a tab for each of the bots
(You do not have to have any particular tab focused, or even any of them)
Once the bots finish, run the "htmlToScreenshots.py" file, either through the command line or by double clicking it
This will take a few moments (especially on the first run)
After the process completes the screenshots of each page will be in the Screenshots folder

Please remember to delete all the HTML files in the "HTML" folder between uses (but do not delete anything inside the "static" sub folder)

The screenshots in the Screenshots folder will be overwritten automatically so grab any you'll need later before running "htmlToScreenshots.py"

Do not try to run this on a deployed server like Heroku, using browser bots will still be fine, and nothing will break if you accidentally check "screenshot" 
but "htmlToScreenshots.py" will not work properly (if at all) because:
-pyppeteer is not in the requirements.txt so it won't be installed on the server at launch
(it also uses headless chrome which might not have appropriate carry over)
-the internal folder structure for the server is more subject to change
-manually deleting the HTML from the server between uses complicates things
-most importantly: server setups like Heroku often don't allow for direct file access unless you jump through some extra hoops
(none of these are insurmountable if for some reason the code needs to be able to be run on the server, but it may require a major rework)