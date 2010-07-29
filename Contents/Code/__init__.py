from PMS import Plugin, Log, XML, HTTP, JSON, Prefs, RSS, Utils
from PMS.MediaXML import *
from PMS.Shorthand import _L, _R, _E, _D

COMCENT_PLUGIN_PREFIX       = "/video/comedycentral"

####################################################################################################
def Start():
  Plugin.AddRequestHandler(COMCENT_PLUGIN_PREFIX, HandleRequest, "Comedy Central", "icon-default.jpg", "art-default.jpg")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", contentType="items")  
  Plugin.AddViewGroup("List", viewMode="List", contentType="items")
    
####################################################################################################

def HandleRequest(pathNouns, count):
  try:
    (pathNouns[count-1], title2) = pathNouns[count-1].split("||")
    title2 = _D(title2).encode("utf-8")
  except:
    title2 = ""
  dir = MediaContainer("art-default.jpg", viewGroup="List", title1="Comedy Central", title2=title2)
  if count == 0:
    for show in XML.ElementFromString(HTTP.GetCached("http://www.comedycentral.com/shows/index.jhtml"),True).xpath('//div[@class="hiddencontent"]/ul/li/a'):
      showurl = show.get("href")
      if showurl.count("http://") == 0 and showurl.count("katz") == 0 and showurl.count("scrubs") == 0 and showurl.count("wanda") == 0 and showurl.count("mad_tv") == 0 and showurl.count("colbert") == 0:
        Log.Add(showurl)
        thumb = "" 
        dir.AppendItem(DirectoryItem(_E(showurl) + "||" + _E(show.text_content().encode('utf-8')), show.text_content(), thumb))
      else:
        Log.Add("********* SITE SPECIFIC ENTRY: " + show.get("href"))
  elif count == 1:
    id = Utils.DecodeUrlPathToString(pathNouns[-1])
    id = ("http://www.comedycentral.com" + id).replace("index.jhtml","videos/index.jhtml")
    for menu_item in XML.ElementFromString(HTTP.GetCached(id),True).xpath('//div[@class="menu"]/a'):
      title = menu_item.xpath('following-sibling::table/tr/td/span')[0].text_content()
      Log.Add(menu_item.get("href"))
      dir.AppendItem(DirectoryItem(_E(menu_item.get("href")) + "||" + _E(title), title, "http://www.comedycentral.com" + menu_item.find("img").get("src")))

  elif count == 2:
      id = Utils.DecodeUrlPathToString(pathNouns[-1]).replace(" ","%20")
      id = ("http://www.comedycentral.com" + id)
      dir.SetViewGroup("InfoList")
      Log.Add(id)
      for vid_block in XML.ElementFromString(HTTP.GetCached(id),True).xpath('//div[@class="vid_block"]'):
        #Log.Add(XML.ElementToString(vid_block))
        id = vid_block.xpath("div[@class='image_holder']/a")[0].get("href")
        Log.Add("****URL:" + id)
        title = vid_block.xpath("div[@class='text_holder']/h4/a")[0].text_content()
        desc = vid_block.find("div[@class='text_holder']/p").text_content()
        duration = ""
        thumb = vid_block.find("div[@class='image_holder']/a/img").get("src").replace("height=75&width=100","height=225&width=300")
        subtitle = "Posted: " + vid_block.find("div/div[@class='block']/div").text_content()
        vidItem = WebVideoItem(id, title, desc, duration, thumb)
        vidItem.SetAttr("subtitle",subtitle)
        dir.AppendItem(vidItem)
  
  return dir.ToXML()
  