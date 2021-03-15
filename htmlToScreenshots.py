# import imgkit
from pathlib import Path


# config = imgkit.config(wkhtmltoimage='HTML/wkhtmltox/bin/wkhtmltoimage.exe')
# options = {
# 	'allow':'HTML/static/otree/css',
# 	'enable-local-file-access':None,
# 	'crop-w':'1920'
# }
# p = Path("HTML")
# for child in p.iterdir():#pathlib explore dir
# 	childStr=str(child)
# 	if childStr.casefold().endswith(".html"):#if the current file is html
# 		print("Screenshots/"+childStr.split("/")[-1]+".jpg")
# 		imgkit.from_file(childStr,"Screenshots/"+childStr.rstrip(".html").split("\\")[-1]+".jpg", config=config, options=options)

import asyncio
from pyppeteer import launch

async def main():
	p = Path("HTML")
	mypath = Path().absolute()
	browser = await launch()
	page = await browser.newPage()
	for child in p.iterdir():#pathlib explore dir
		childStr=str(child)
		if childStr.casefold().endswith(".html"):#if the current file is html
			print(str(mypath)+"\\"+childStr)
			await page.goto(str(mypath)+"\\"+childStr)
			await page.setViewport(dict(width=1920,height=1080))
			await page.screenshot({'path': "Screenshots/"+childStr.rstrip(".html").split("\\")[-1]+".jpg"})
	await browser.close()

asyncio.get_event_loop().run_until_complete(main())