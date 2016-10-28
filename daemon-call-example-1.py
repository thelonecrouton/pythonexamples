#!/usr/bin/python
# ^^ tells the system that this is a python script, at least on *nix, no idea about Win

# comments in python begin with a '#' - in C++ it's a '//' - the interpereter (python) or compiler (C++) ignores these

# we'll be using strings a bit, note that python doesn't care about you using '' or "" to define a string, in fact it's often neccessary to use both if you're building a complex API call... ;)

# shoulders of giants... we're going to be needing some pre-written libraries
import sys, os, subprocess, json, urllib2

# we'll get the current working directory
cwd = os.getcwd()  #  what 'import os' was for... so.. we need to place this script in the same directory as the daemon / server and run it from there with 'python daemon-call-example1.py' 

# here's the command we want to pass to the daemon (crown-cli / crown-cli.exe)
cmd = "getinfo"

# let's build the string we send to the daemon (crown-cli / crown-cli.exe) 
# *nix version:
commandstring = (os.path.join(cwd, 'dash-cli') + ' ' + cmd)
# win version:
#commandstring = (os.path.join(cwd, 'dash-cli.exe') + ' ' + cmd)  # UNTESTED, you may need to meddle a little !

# we'll print this to console as a debugging aid, to see what we're doing
print 'this is what we will programatically pass to the daemon:' + '\n' + commandstring  # note the special char we insert here, a newline ('\n') 

# OK, assuming this script is running in the same directory as the software we want to query -ie, you've saved it there and called it consequently from that directory -  we can now actually query it and get a response...

# however, we need to make sure that the piece of software we're talking to will talk back to us, so we need to have a crown(or whatever).conf file with the folowing lines in there:
#rpcuser=blah
#rpcpassword=blahblah
#rpcallowip=127.0.0.1
#server=1
# (take out the '#'s' in the .conf file!
# then restart your wallet / daemon so it takes account of the new .conf file!

# so let's run our system call to the daemon
q = subprocess.check_output(commandstring, shell=True) 
# we imported the subprocess module up top... the variable 'q' (arbitrary, can be called anything you like) is what we're storing the output of our system call in - the 'shell=True' bit I'll get into later, unless I forget

# so, we've queried the daemon, let's print our 'q' which is the daemon's response...
print q

# this outputs a json formatted chunk of data that will look something like this:
#{
#    "version" : 120060,
#    "protocolversion" : 70030,
#    "walletversion" : 60000,
#    "balance" : 14123.34542738,
#    "darksend_balance" : 0.00000000,
#    "blocks" : 1103671,
#    "timeoffset" : 0,
#    "connections" : 8,
#    "proxy" : "",
#    "difficulty" : 7609961.52130730,
#    "testnet" : false,
#    "keypoololdest" : 1476289805,
#    "keypoolsize" : 999,
#    "unlocked_until" : 0,
#    "paytxfee" : 0.00000000,
#    "relayfee" : 0.00010000,
#    "errors" : ""
#}

# Now let's use python's json module, which we imported up above at the start, to separate out a particular chunk of that output that we might be interested in...
# here's how we get just our balance, not also the darksend_balnce, with json...
jdata = json.loads(q) # we load the daemon output q into a json object we'll call jdata with the json.loads() function

# then we can extract values based on their json key name...
print "Balance: " + str((jdata['balance'])) # although we can print the jdata object directly, like we do the next two, we need to cast it as a str() before we can concatenate it with another string
print (jdata['difficulty'])
print (jdata['blocks'])



# OK, now let's hit up a remote server and pull some data from it...
site = 'https://bittrex.com/api/v1.1/public/getticker?market=BTC-DASH'  # let's get the current Dash price from Bittrex
req = urllib2.Request(site)
page = urllib2.urlopen(req)
data = page.read()
print data
# this should output something like
# {"success":true,"message":"","result":{"Bid":0.01405588,"Ask":0.01424508,"Last":0.01411040}}

# a lot of servers dish out requested data in json format, so we'll use json again to pull out a chunk that we may be interested in, in this example the current Ask price...
jdata = json.loads(data) # we're repurposing the jdata variable we used earlier but we could have used a new one, it would have cost a tiny bit more RAM
print "Current Bittrex Dash Ask price: " + str((jdata['result'] ["Ask"])) # note how we pull out nested json data with concatenated key values, we can't just do a 'print (jdata['Ask'] we have to reference it via its parent nesting

# some sites won't serve you without you 'pretending to be a browser' - like any site with cloudflare ddos protection
# here's how you deal with that:

# let's get a CRW balance from the chainz block explorer...
address = '1JAaUtzK8dHKVGTqKDT4m8peMniyjxBNH9'
site = ("http://chainz.cryptoid.info/crw/api.dws?q=getbalance&a=" + address) # build the API call
######################################################### need to fool cloudflare!
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}
req = urllib2.Request(site, headers=hdr) # we pass the fake headers when we make the call
######################################################### cloudflare hoodwinked!
# we'll chuck in some basic error handling this time...
try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()
data = page.read() # whatever the server returns, in this case it's a simple number, so we don't need to do any json postprocessing, just cast it as a str() so we can concatenate it with other strings in our output:
print "Balance of CRW address " + address + ": " + str(data)

# here endeth this lesson! :)







