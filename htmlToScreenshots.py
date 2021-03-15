from pathlib import Path #to know where things are
import asyncio #async process for web load
from pyppeteer import launch #do the actual browser stuff

#note: Pyppeteer will install chromium, it needs it to work and should install it automatically if not present
async def main():
	p = Path("HTML") #get the HTML folder as an object
	mypath = Path().absolute() #figure out where we are
	browser = await launch() #launch the headless browser
	page = await browser.newPage()#get a new page for the browser
	for child in p.iterdir():#pathlib explore dir
		childStr=str(child)#convert path obj to string obj
		if childStr.casefold().endswith(".html"):#if the current file is html
			await page.goto(str(mypath)+"\\"+childStr)#open page
			await page.setViewport(dict(width=1920,height=1080))#set viewport size
			await page.screenshot({'path': "Screenshots/"+childStr.rstrip(".html").split("\\")[-1]+".jpg"})#take a screenshot
	await browser.close()#close the browser

asyncio.get_event_loop().run_until_complete(main())#py driver