import requests as r
import pandas as pd
import json
import datetime
import time

stime = time.time()
key = 
listid = '182214'

#using this date range for time time being bc January started on a Monday and Sept. ended on a Sunday.
startdate = datetime.datetime(2018,1,1)
enddate = datetime.datetime(2018,9,30)
end = enddate

starts = []
ends = []

pull = 0
print('Creating periods...')
while end <= enddate:    
    start = startdate
    starts.append(datetime.datetime.strftime(start,'%Y-%m-%d'))
    end = start + datetime.timedelta(days=27)
    ends.append(datetime.datetime.strftime(end,'%Y-%m-%d'))
    pull = pull+1
    print('Period '+str(pull)+' created.')
    startdate = end + datetime.timedelta(days=1)

dataframe = pd.DataFrame({'start': starts,
                          'end':ends
                          })

names = []
pers = []
interactionrates = []
linkposts = []
lpinteractionrates = []
photoposts = []
photopostinteractionrates = []
nativevideos = []
nativevideointeractionrates = []
followerstarts = []
followersends = []
folgrowths = []  
pctchanges = []

loop = 0
def pullai(start,end):
   query = 'https://api.crowdtangle.com/leaderboard?token='+key+'&count=100&endDate='+str(end)+'&startDate='+str(start)+'&listId='+listid+'&sortBy=interaction_rate'
   pull = r.get(query)
   jsonfile = json.loads(pull.content)
   ai = jsonfile['result']['accountStatistics']
   for a in ai:
       per = start
       pers.append(per)
       name = a['account']['name']
       names.append(name)
       try:
           interactionrate = a['summary']['interactionRate'] / 100
           interactionrates.append(interactionrate)
       except KeyError:
           interactionrate = None 
           interactionrates.append(interactionrate)
       try:
           linkpostcount = a['breakdown']['link']['postCount']
           linkposts.append(linkpostcount)
       except KeyError:
           linkpostcount = 0
           linkposts.append(linkpostcount)
       try:
           lpinteractionrate = a['breakdown']['link']['interactionRate'] / 100
           lpinteractionrates.append(lpinteractionrate)
       except KeyError:
           lpinteractionrate = None
           lpinteractionrates.append(lpinteractionrate)
       try:
           photopostcount = a['breakdown']['photo']['postCount']
           photoposts.append(photopostcount)
       except KeyError:
           photopostcount = 0
           photoposts.append(photopostcount)
       try:
           ppinteractionrate = a['breakdown']['photo']['interactionRate'] / 100
           photopostinteractionrates.append(ppinteractionrate)
       except KeyError:
           ppinteractionrate = None
           photopostinteractionrates.append(ppinteractionrate)
       try:
           nvcount = a['breakdown']['native_video']['postCount']
           nativevideos.append(nvcount)
       except KeyError:
           nvcount = 0
           nativevideos.append(nvcount)
       try:
           nvir = a['breakdown']['native_video']['interactionRate'] / 100
           nativevideointeractionrates.append(nvir)
       except KeyError:
           nvir = None
           nativevideointeractionrates.append(nvir)
       folstart = a['subscriberData']['initialCount']
       followerstarts.append(folstart)
       folend = a['subscriberData']['finalCount']
       followersends.append(folend)
       folgrowth = folend-folstart
       folgrowths.append(folgrowth)
       pctchange = folgrowth / folstart
       pctchanges.append(pctchange)

for i in range(len(starts)):
    pullai(starts[i],ends[i])
    print('Loop '+str(i)+' completed.')
    #time.sleep(10)
        
dataframe = pd.DataFrame({'period': pers,
                          'account':names,
                          'interaction_rate_overall':interactionrates,
                          'link_posts':linkposts,
                          'lp_ir':lpinteractionrates,
                          'photo_posts':photoposts,
                          'pp_ir':photopostinteractionrates,
                          'native_videos': nativevideos,
                          'nv_ir': nativevideointeractionrates,
                          'followers_start': followerstarts,
                          'followers_end': followersends,
                          'net_follower_growth':folgrowths,
                          'pct_change':pctchanges
                          })
print(dataframe)
dataframe.to_csv('crowdtangle_accountgrowth_'+str(startdate)+'_'+str(enddate)+'.csv') 