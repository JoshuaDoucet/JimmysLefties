from django.shortcuts import render
from shoes.models import Shoe, SearchRequest, SiteUser
import re

#For Web Scraping
import bs4
import requests

# for graph visualization
import plotly.express as px
import pandas

# MUST RUN COMMAND BEFORE FIRST USE
#pip install -U kaleido

# Create your views here.

# view for displaying shoe results
def shoes(request):
  # Clear existing shoes delattr
  Shoe.objects.all().delete()

  # get shoe search form values from srddion
  if 'form' in request.session:
    shoeForm = request.session['form']
    del request.session['form']
  else:
    shoeForm = "NA"  

  #DEBUG
  print("User shoe search Form " + str(shoeForm))

  # If there is no user shoe criteria, search all shoes
  if(shoeForm == "NA"):
    sr = None
  else:
  # else create a SearchRequest with user input criteria
    if(request.user.is_authenticated and not request.user.is_superuser):
      siteUser = SiteUser.objects.filter(authUser=request.user)[0]
    else:
      siteUser = SiteUser.objects.first()
    
    if shoeForm['size']:
      shoeSize = shoeForm['size']
    else:
      shoeSize = 0 

    sr = SearchRequest(phrase=shoeForm['phrase'], size=shoeSize, sex="NA", userID=siteUser)
    sr.save()

  # Get shoe data from shoe sites
  # Test fake search request for scraping
  getUnpairedSolesShoeData(sr)
  getOddSoleFinderShoeData(sr)
  
  # Refine shoe search using user search criteria
  if(sr == None):
    shoes = Shoe.objects.all().order_by('title')
  else:
    if (sr.size != None):
      size = float(sr.size)
    else:
      size = 0
    # both phrase and size criteria provided
    if(sr.phrase != "" and sr.size != 0):
      shoes = Shoe.objects.filter(title__icontains=sr.phrase).filter(length=size).order_by('title') | Shoe.objects.filter(title__icontains=sr.phrase).filter(length=size).order_by('title')
    # phrase provided, size not
    elif sr.phrase != "" and sr.size == 0:
      shoes = Shoe.objects.filter(title__icontains=sr.phrase).order_by('title')
    # phrase not provided, size is
    else:
      shoes = Shoe.objects.filter(length=size) | Shoe.objects.filter(length=size).order_by('title')

  # Generate found shoe size count graph
  generateShoeCountBySizeGraphImg(shoes)

  #get number of shoe results
  shoeCount = shoes.count()

  # pair the shoes in a list of tuples
  pairedShoes = []
  itr = iter(shoes)
  for shoe in itr:
    try:
      pairedShoes.append((shoe, next(itr)))
    except:
      pairedShoes.append((shoe, ""))
  shoes = pairedShoes

  # render shows.html
  return render(request, 'shoes.html', {'shoes': shoes, "shoeForm": shoeForm, 'shoeCount': shoeCount, "count": 0})

# get shoe data from odd shoe finder
def getGenderedOddShoeFinderShoeData(gender):
  #DEBUG
  print("Entering Odd Shoe Finder Scraper")

  #Mens shoe URL
  menURLStr = "https://www.oddshoefinder.com/mens-shoes/"
  #Womans shoe URL
  womanURLStr = "https://www.oddshoefinder.com/womens-shoes/"

  #Determine if Men or Woman shoes should be fetched
  if(gender == "M"):
    genderedURL = menURLStr
    shoe_sex = "M"
  elif (gender == "W"):
    genderedURL = womanURLStr
    shoe_sex = "W"
  else:
    shoe_sex = "NA"
  
  # Init web scraping resource for Mens shoes site
  res = requests.get(genderedURL)
  res.raise_for_status()

  # get HTML of mens shoe site
  shoeSoup = bs4.BeautifulSoup(res.text, features="html.parser")

  #DEBUG
  print("Odd Shoe Finder HTML fetched")

  # get shoe title class HTML
  shoeClassLink = ".listing-title"
  shoes = shoeSoup.select(shoeClassLink)
  #get shoe description class HTML
  shoeDescClassLink = ".listing-detail.left"
  descs = shoeSoup.select(shoeDescClassLink)
  # get shoe images HTML
  imageClass = ".imgb > div"
  images = shoeSoup.select(imageClass)

  # store shoe image URLS in list
  imageURLs = []
  for image in images:
    imgElm = image.select("img")
    imgURL = imgElm[0].get("data-src")
    imageURLs.append(imgURL)

  # store shoe descrptions in list
  descList = []
  for desc in descs:
    descPar = desc.select("p")
    if(len(descPar) >= 1):
      descStr = descPar[0].getText()
      descList.append(descStr)
    else:
      descList.append(" ")

  # var to iterate through shoe data
  shoeIndex = 0
  # for each shoe on the web page
  for shoe in shoes:
    # grab the purchase URL for the shoe
    link = shoe.select("a")
    purchaseURL = link[0].get("href")
    # get the title for the shoe
    title = link[0].get("title")
    # get image URL for the shoe
    imgURL = imageURLs[shoeIndex]

    # get description
    shoeDescript = descList[shoeIndex]

    # get shoe size info
    #pattern for finding shoe size
    rightSizeRe = re.compile(r"Right Shoe: \d+(.\d*)?")
    leftSizeRe = re.compile(r"Left Shoe: \d+(.\d*)?")
    numRe = re.compile(r"(\d+.(\d)*|\d+)")

    #get right foot size from description
    matches = rightSizeRe.search(str(shoeDescript))
    if(matches != None):
      matches = numRe.search(matches.group())
      if(matches != None):
        rightSize = float(matches.group())
      else:
        rightSize = None
    else:
      rightSize = None

    #get left foot size from description
    matches = leftSizeRe.search(str(shoeDescript))
    if(matches != None):
      matches = numRe.search(matches.group())
      if(matches != None):
        leftSize = float(matches.group())
      else:
        leftSize = None
    else:
      leftSize = None

    shoeIndex += 1

    # Add new shoe to database table shoes
    shoe = Shoe(title=title, purchaseURL=purchaseURL, description=shoeDescript, sex=shoe_sex, imageURL=imgURL, length=leftSize, length2=rightSize)
    shoe.save()

  
def getGenderedUnpairedSoles(gender):
  #DEBUG
  print("Enter Unpaired Soles Scraper")
  #Site base URL
  baseURL = "https://www.unpairedsoles.com"
  #Mens shoe URL
  menURLStr = "https://www.unpairedsoles.com/men"
  #Momens shoe URL
  womenURLStr = "https://www.unpairedsoles.com/women"

  #Determine if Men or Woman shoes should be fetched
  if(gender == "M"):
    genderedURL = menURLStr
    shoe_sex = "M"
  elif (gender == "W"):
    genderedURL = womenURLStr
    shoe_sex = "W"
  else:
    shoe_sex = "NA"

  # Init web scraping resource for Mens shoes site
  res = requests.get(genderedURL)
  res.raise_for_status()

  # get HTML of mens shoe site
  menShoeSoup = bs4.BeautifulSoup(res.text, features="html.parser")
    
  # DEBUG
  print("Unpaired Soles HTML fetched")

  #get shoe purchase link path elements from BeautifulSoup
  shoeLinkClass = ".grid-item-link"
  links = menShoeSoup.select(shoeLinkClass)

  #for each shoe link found on the page
  for link in links:
    #get the shoe title and path to shoe page
    shoeName = link.get("aria-label")
    shoePath = link.get("href")

    #make purchaseURL for shoe
    purchaseURL = baseURL + shoePath

    #Create a new soup for shoe pages
    # Init web scraping resource for Mens shoes site
    # add user-agent to prevent HTTP error 429
    shoeRes = requests.get(purchaseURL, headers = {'User-agent': 'One-Off Shoe finder'})
    shoeRes.raise_for_status()

    # get HTML of gendered shoe site
    shoeSoup = bs4.BeautifulSoup(shoeRes.text, features="html.parser")


    #scrap data from shoe page to get shoe image URL
    img = shoeSoup.select('img[class="ProductItem-gallery-slides-item-image"]')
    if(len(img) > 0):
      shoeImg = img[0].get("data-src")
    else:
      shoeImg = None

    #scrape data from shoe page to get description
    meta = shoeSoup.select('meta[itemprop="description"]')
    if(len(meta) > 0):
      shoeDesc = meta[0].get("content")
    else:
      shoeDesc = ""
    # remove whitespace around desc    
    shoeDesc.strip()

    #pattern for finding shoe size
    sizeRe = re.compile(r"(size|sz)+( )*\d+(.\d*)?", re.I)
    numRe = re.compile(r"(\d+.(\d)*|\d+)")
    #get size from description
    matches = sizeRe.search(str(shoeDesc))
    if(matches != None):
      matches = numRe.search(matches.group())
      if(matches != None):
        size = float(matches.group())
      else:
        size = None
    else:
      size = None

    # Add new shoe to database table shoes
    shoe = Shoe(title=shoeName, purchaseURL=purchaseURL, description=shoeDesc, sex=shoe_sex, length=size, imageURL=shoeImg,)
    shoe.save()




def getUnpairedSolesShoeData(shoeCriteria):
  #Get Mens shoe data from UnpairedSoles
  getGenderedUnpairedSoles("M")
  #Get Womens shoe data from UnpairedSoles
  getGenderedUnpairedSoles("W")
  #DEBUG
  print("Unpaired Soles, shoe scraping complete")
  
def getOddSoleFinderShoeData(shoeCriteria):
  #Get Mens shoe data from Odd Shoe Finder
  getGenderedOddShoeFinderShoeData("M")
  #Get Womens shoe data from Odd Shoe Finder
  getGenderedOddShoeFinderShoeData("W")
  #DEBUG
  print("Odd Shoe Finder, shoe scraping complete")

#TODO
def generateShoeCountBySizeGraphImg(shoes):
  # Generate shoe size count bar chart
  # Stores unique shoe sizes
  sizeArr = [0]
  # Store count of size found
  countArr = [0]
  # for each shoe model object add size to graph data
  for shoe in shoes:
    # Get sizes from shoes
    size1 = shoe.length;
    size2 = shoe.length2;
    if(size1 != None):
      try:
        # Size found already, increment shoe count
        sizeIndex = sizeArr.index(size1)
        countArr[sizeIndex] = countArr[sizeIndex] + 1
      except ValueError:
      # if size not found yet, add to sizeArr, init new element in countArr to 1
        sizeArr.append(size1)
        countArr.append(1)
    if(size2 != None):
      try:
        # Size found already, increment shoe count
        sizeIndex = sizeArr.index(size2)
        countArr[sizeIndex] = countArr[sizeIndex] + 1
      except ValueError:
      # if size not found yet, add to sizeArr, init new element in countArr to 1
        sizeArr.append(size2)
        countArr.append(1)

  shoe_size_data = {'Size':sizeArr,'Count':countArr,}
  fig = px.bar(shoe_size_data, x='Size', y='Count', title="Number of Shoes found by Shoe Size")
  fig.write_image("./static/images/barchart.jpeg")

