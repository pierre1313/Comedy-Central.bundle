import re

COMCENT_PLUGIN_PREFIX       = "/video/comedycentral"
YAHOO_NAMESPACE  = {'media':'http://search.yahoo.com/mrss/'}

RSS_PATH = "http://www.comedycentral.com/comedycentral/video/data/mrss.jhtml?uri=%s"

ICON = "icon-default.png"
ART = "art-default.jpg"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(COMCENT_PLUGIN_PREFIX, MainMenu, "Comedy Central", ICON, ART)
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")  
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  MediaContainer.art = R(ART)
  DirectoryItem.thumb = R(ICON)
    
####################################################################################################

def MainMenu():
  dir = MediaContainer(viewGroup="List", title1="Comedy Central")
  for show in HTML.ElementFromURL("http://www.comedycentral.com/shows/index.jhtml").xpath('//div[@class="hiddencontent"]/ul/li/a'):
    showurl = show.get("href")
    if showurl.count("http://") == 0 and showurl.count("katz") == 0 and showurl.count("scrubs") == 0 and showurl.count("wanda") == 0 and showurl.count("mad_tv") == 0 and showurl.count("colbert") == 0:
      dir.Append(Function(DirectoryItem(Level1, title = show.text_content()),url=showurl,title = show.text_content().encode('utf-8')))
        
  return dir
  
def Level1(sender, url, title):
  dir = MediaContainer(viewGroup="List", title2=title.encode("utf-8"))        
  showurl = ("http://www.comedycentral.com" + url)
  try:
    showpage =  HTTP.Request(showurl).content
    idpos = showpage.find("mgid:cms:video:comedycentral.com:")
    id =  showpage[idpos:idpos+39].replace(":","%3A")
    rssfeed = HTTP.Request(RSS_PATH %id).content.replace('media:','media-')
    for item in XML.ElementFromString(rssfeed).xpath('//item'):#namespaces = YAHOO_NAMESPACE
      title = item.xpath('title')[0].text.replace('|',' - ')
      subtitle = item.xpath('pubDate')[0].text
      summary = item.xpath('description')[0].text
    
      stringified = XML.StringFromElement(item)
    
      try:
        duration = int(re.search('duration="([0-9]+)"', stringified).group(1))*1000
      #duration = int(item.xpath('media-content')[0].get('duration'))*1000
      except:
        duration = None
      
      try:
        thumb = re.search('media-thumbnail url="([^&?]+.jpg)', stringified).group(1)
   #     thumb = item.xpath('media-thumbnail')[0].get('url')
      except:
        thumb = R(ICON)
      url = item.xpath('link')[0].text
      dir.Append(WebVideoItem(url, title=title , subtitle=subtitle, summary=summary, duration=duration, thumb = thumb))

    if len(dir) == 0:
      return MessageContainer("Error","This category does not contain any video.")
    else:
      return dir
  except:
    return MessageContainer("Error","This category does not contain any video.")