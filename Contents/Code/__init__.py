COMCENT_PLUGIN_PREFIX       = "/video/comedycentral"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(COMCENT_PLUGIN_PREFIX, MainMenu, "Comedy Central", "icon-default.jpg", "art-default.jpg")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")  
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  MediaContainer.art = R("art-default.jpg")
  DirectoryItem.thumb = R("icon-default.jpg")
    
####################################################################################################

def MainMenu():
  dir = MediaContainer(viewGroup="List", title1="Comedy Central")
  for show in HTML.ElementFromURL("http://www.comedycentral.com/shows/index.jhtml").xpath('//div[@class="hiddencontent"]/ul/li/a'):
    showurl = show.get("href")
    if showurl.count("http://") == 0 and showurl.count("katz") == 0 and showurl.count("scrubs") == 0 and showurl.count("wanda") == 0 and showurl.count("mad_tv") == 0 and showurl.count("colbert") == 0:
      Log(showurl)
      dir.Append(Function(DirectoryItem(Level1, title = show.text_content()),url=showurl,title = show.text_content().encode('utf-8')))
    else:
      Log("********* SITE SPECIFIC ENTRY: " + show.get("href"))
        
  return dir
  
def Level1(sender, url, title):
  dir = MediaContainer(viewGroup="List", title2=title.encode("utf-8"))        
  id = ("http://www.comedycentral.com" + url).replace("index.jhtml","videos/index.jhtml")
  for menu_item in HTML.ElementFromURL(id).xpath('//div[@class="menu"]/a'):
    title = menu_item.xpath('following-sibling::table/tr/td/span')[0].text_content()
    Log(menu_item.get("href"))
    dir.Append(Function(DirectoryItem(Level2, title=title , thumb = "http://www.comedycentral.com" + menu_item.find("img").get("src")), url= menu_item.get("href"), title = title))
  return dir

def Level2(sender, url, title):
  dir = MediaContainer(viewGroup="InfoList", title1="Comedy Central", title2=title.encode("utf-8"))
  id = ("http://www.comedycentral.com" + (url).replace(" ","%20"))
  Log.Add(id)
  for vid_block in HTML.ElementFromURL(id).xpath('//div[@class="vid_block"]'):
    #Log.Add(XML.ElementToString(vid_block))
    id = vid_block.xpath("div[@class='image_holder']/a")[0].get("href")
    Log.Add("****URL:" + id)
    title = vid_block.xpath("div[@class='text_holder']/h4/a")[0].text_content()
    desc = vid_block.find("div[@class='text_holder']/p").text_content()
    duration = None
    thumb = vid_block.find("div[@class='image_holder']/a/img").get("src").replace("height=75&width=100","height=225&width=300")
    subtitle = "Posted: " + vid_block.find("div/div[@class='block']/div").text_content()
    dir.Append(WebVideoItem(id, title = title, summary = desc, subtitle = subtitle, duration = duration, thumb = thumb))
  
  return dir
  