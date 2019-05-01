import pandas as pd
from urllib.parse import urlparse
internal_links=[]
external_links=[]
include_url=['','.']
def seperate_links(All_links,url):
  includeurl=urlparse(url).netloc
  if(All_links==[]) :
    return 'Empty string was passed'
  else:
    for link in All_links:
      link_netloc=urlparse(link[0]).netloc
      if (link_netloc == includeurl)| (link_netloc in include_url):
        internal_links.append(link)
      else:
        external_links.append(link)
      df=pd.DataFrame({'internal_links':pd.Series(internal_links),'external_links':pd.Series(external_links)})
      df.to_csv(f'{includeurl}.csv')
    return f'links saved into {includeurl}.csv'


#All_links is the extracted links from 'url', All_links should be a 
#list with tuple of ('link',anchor_text)
#e.g All_links = [('https://search.google.com/local/writereview?placeid=ChIJWWwOvtVhlR4R-Jbrh-bc8pM',
# 'Write a Review'),
# ('https://search.google.com/local/reviews?placeid=ChIJWWwOvtVhlR4R-Jbrh-bc8pM',
# 'Read More'),
# ('/about', 'Read More'),
# ('//www.google.com/maps/uv?pb=!1s0x1e9561d5be0e6c59:0x93f2dce687eb96f8!3m1!7e131!5s1202+on+Cowgill+Guest+Rooms&hl=en&imagekey=!1e3!2s-OgMAEbiUcxw%2FWhLiR0hdafI%2FAAAAAAAAAIY%2FVYE74WRBQX0Dekws0C60ClQ13o880XG2gCNwBGAYYCw',
# ''),
# ('//www.google.com/maps/uv?pb=!1s0x1e9561d5be0e6c59:0x93f2dce687eb96f8!3m1!7e131!5s1202+on+Cowgill+Guest+Rooms&hl=en&imagekey=!1e3!2s-LWk3956QVrk%2FWhLiLOQuJlI%2FAAAAAAAAAI4%2Fo_fEADKwV1AfniqK4EVi6ZLWKasZyy0gQCNwBGAYYCw',
# '')]

#url shld be the url where the All_links is scrapped from
