import asyncio
from datetime import datetime
from pprint import pprint
from urllib.parse import urlparse
from aiohttp import ClientConnectorError, ClientSession

from simplified_scrapy.spider import SimplifiedDoc

def extract_extention(path):
    extention = path.split('.')
    return "" if len(extention) < 2 else extention[-1].lower()

def is_enterable(base_url: str, url: str) -> bool:
    base_url_parsed = urlparse(base_url)
    url_parsed = urlparse(url)

    base_netloc = base_url_parsed.netloc
    netloc = url_parsed.netloc

    extention = extract_extention(url_parsed.path)
    if not extention or ("html.jsp.aspx.php".find(extention) >= 0):
        return netloc.endswith(base_netloc) or base_netloc.endswith(netloc)
    else:
        return False


# def is_page_url(url):
#     if (not url):
#         return False
#     if ("html.htm.jsp.asp.php".find(url[-4:].lower()) >= 0):
#         return True

#     if ('.jpg.png.gif.bmp.rar.zip.pdf.doc.xls.ppt.exe.avi.mp4'.find(
#             url[-4:].lower()) >= 0
#             or '.jpeg.xlsx.pptx.docx'.find(url[-5:].lower()) >= 0
#             or '.rm'.find(url[-3:].lower()) >= 0):
#         return False
#     return True


seen = set()
sema = asyncio.Semaphore(10)
base_url = "https://alasdevcenter.com/"

def add_url(url):
    seen.add(url)
    

async def extract_html(session: ClientSession, url: str) -> str:
    try:
        async with session.get(url) as response:
            if not response.ok:
                print(f"Failed to fetch {url}")
                return ""
            html = await response.text()
            return html
    except ClientConnectorError as e:
        print(f"Failed to connect to {url}")
        return ""

async def extract(session: ClientSession, url: str) -> None:
    print(f"Extracting {url}")
    if url in seen:
        return
    else:
        seen.add(url)

    if not is_enterable(base_url, url):
        print(f"Skipping {url}")
        return
    
    async with sema:
        html = await extract_html(session, url)
    
    if not html:
        return

    doc = SimplifiedDoc(html)
    lstA = doc.listA(url=url)
    fs = [extract(session, url["url"]) for url in lstA]
    await asyncio.gather(*fs)


async def extract_all(url: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    async with ClientSession(headers=headers) as session:
        await extract(session, url)

print(f"Starting {datetime.now()}")
asyncio.run(extract_all(base_url))
print(f"Starting {datetime.now()}")

with open("output.txt", "w") as f:
    pprint(seen, stream=f)
