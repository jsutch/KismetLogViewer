![Alt text](logo.png?raw=true "Title")
#### Kismet Log Viewer v3.1.1 Tool (http://klv.professionallyevil.com/)
Combines multiple Kismet log files in the .netxml format, summarizes the data, and outputs an easy-to-read html or csv file.

Kismet Log Viewer v2 Was written in Python, with limited functionality.  
The original KLV was written in 2003 by Brian Foy of Mindflip.org, but w/o support for newer versions of .netxml format.  
Updated to use python3 in 2021 by Jeff Sutch of Collett Park Networks.  

```
 ############################################################################
 #  Name: Kismet Log Viewer (KLV) (w/ extended features)                    #
 #                                                                          #
 #  Description: KLV accepts one or more Kismet .netxml files, summarizes   #
 #               & de-duplicatesthe data, and creates a readable summary    #
 #               in either html or csv format.                              #
 #                                                                          #
 #  Requirements:                                                           #
 #                Python                                                    #
 #                One or more Kismet .netxml log files                      #
 #                                                                          #
 #   Extended features:                                                     #
 #       @NEW GPS,SignalInfo,HTML code on HTML creation (clean CSV)         #
 #            -n argument, Modify HTML, Clean \n on CSV, CSV headers        #
 #            -o default mode change                                        #
 #                                                                          #
 #  Website: http://klv.professionallyevil.com                              #
 #  Author:  Nathan Sweaney - nathan@sweaney.com                            #
 #  Date:   July 9, 2013                                                    #
 ############################################################################
```
#### Usage:
```
klv.py [-h] [-o {html,csv}] [-s {essid,security,bssid,manufacturer,clients,packets}] [-g {yes,no}] [-t {beacon,request,response}] LogFilePath

         -h, --help show this help message and exit
         -o {html,csv} Output format (default: html)
      *  -s {essid,security,bssid,manufacturer,clients,packets} Sort output (default: essid) (unfinished)
      *  -g {yes,no} Group by essid (default: no) (unfinished)
      *  -t {beacon,request,response} Show network types (default: beacon only) (unfinished)
LogFilePath A directory containing one or more Kismet .netxml log files, other files will be ignored
         -n Name for the processed files. Filename default: Kismet-Log-Summary'
      *=unfinished
      
 Example usage:
          ./klv.py -h                                                      
          ./klv.py /root/kismet-logs/                                      
          ./klv.py -t csv /root/kismet-logs/                               
```
#===#
```
From https://blog.secureideas.com/2013/07/kismet-log-viewer-v2-tool-released.html :

Secure Ideas actively supports open source and giving back
to the community. In that light, we’re announcing the release of an updated tool
for parsing and viewing Kismet log files.

Kismet is a fantastic tool for wireless network assessments.
It passively detects networks, SSIDs, and with enough time can even decloak
hidden networks by capturing the name from clients that connect. And with an
extensible plugin architecture, it can even sniff other, non-802.11, types of
wireless traffic.

One common use during a wireless assessment is to walk or
drive the facilities of a client to determine what wireless traffic is actually
being used. Then that information can be compared to documentation of what the
client believes should be in use. Often times we find misconfigurations,
unapproved use, and even unauthorized devices that have been added to the
network.

One area that Kismet stumbles though is the ability to
easily review log files after the assessment. During the assessment, viewing
data and activity is very easy and accessible, but later when you’re trying to
analyze the results it’s more difficult. Kismet creates a LOT of log data, and
most of it is in XML or CSV format that makes it easy to parse, but there is no
native functionality to view those logs.

Several years ago a number of tools had been released that
parsed and presented this log data in an easy-to-read HTML format. Unfortunately
with changes to the Kismet structure and log format, none of those tools still
work correctly. 

To remedy that, today I’m releasing Kismet Log Viewer v2, an
update to the original Kismet Log Viewer released by Brian Foy in 2003. KLV v2
reads in multiple Kismet .netxml files, summarizes the data, and outputs an
HTML or CSV file.

This initial release has some limitations. Like most
development, functional priority was based on necessity; I wrote what I needed
first. But I plan to continue extending the tool to add more functionality.

So without further ado, here’s the links you care about:

Kismet Log Viewer v2:
http://klv.professionallyevil.com/

And here’s an example report:
http://klv.professionallyevil.com/kismet-log-summary.html

Hopefully you’ll find this tool useful. If you find
problems, or have suggestions, please feel free to contact me.

Nathan Sweaney is a Senior Security Consultant for Secure Ideas. If you are in need of a penetration test or other security consulting services you can contact him at nathan@secureideas.com or visit the Secure Ideas – Professionally Evil site for services provided.
```
#==#

```
Todo:
* add client data
  - To start, just summarize the number of clients for each network.
* add packet data
  - Count of packets seen on each network
* better handling of wireless security - currently only works well for html
  - Maybe use bit counting to keep track of types, then handle output in the output functions.
* add options for sorting
* add option to group BSSIDs
  - effectively de-duplicating SSIDs with all BSSIDs in one table.
  - not sure how this looks in CSV format
* add option to show only specific network types
  - do probe requests & responses need additional information?
* check to see if summary file exists before creating
* name summary file with timestamp
* allow input of specific files, not just a folder
* cool stylesheets
* gracefully handle missing oui.txt file
* gracefully handle no .netxml files
* download updated oui.txt file?
* (*done*) Support GPS info
* create variable for version number instead of spreading it through code
```
