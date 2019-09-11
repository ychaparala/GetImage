from requests_html import HTMLSession
import random
from PIL import Image
import requests
from io import BytesIO
import os.path
import subprocess

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

def getCategory():
    session = HTMLSession()
    vlad_website = session.get('https://vlad.studio/wallpapers')
    categories = []
    for category in vlad_website.html.find('p')[1].find('a'):
        categories.append(category.text)
    session.close()
    return random.choice(categories)

def getArtWorkURL(cat):
    session = HTMLSession()
    artWorkUrl = []
    cat_website = session.get(f'https://vlad.studio/wallpapers/?filter={cat}')
    for artwork in cat_website.html.find('#artworks-list')[0].find('a'):
        artWorkUrl.append(artwork.attrs['href'])
    session.close()
    return random.choice(artWorkUrl)

def saveImage(url):
    image_url = f'https://vlad.studio/fullscreen-preview/?f={url.split("/")[-1]}&w=1280&h=800'
    response = requests.get(image_url)
    filepath = f'{os.path.expanduser("~")}/vlad-studio/{url.split("/")[-1]}.jpg'
    Image.open(BytesIO(response.content)).save(filepath)
    return filepath

def changeDesktopImage(fileURI):
    subprocess.Popen(SCRIPT%fileURI, shell=True)
    subprocess.Popen("killall Dock", shell=True)

if __name__ == "__main__":
    category = getCategory()
    artWorkURL = getArtWorkURL(category)
    filepath = saveImage(artWorkURL)
    changeDesktopImage(filepath)