#!/usr/bin/python
############################################################################
#                                                                          #
#  Name: Kismet Log Viewer (KLV) v2                                        #
#                                                                          #
#  Description: KLV accepts one or more Kismet .netxml files, summarizes   #
#               & de-duplicatesthe data, and creates a readable summary    #
#               in either html or csv format.                              #
#                                                                          #
#  Usage: ./klv.py -h                                                      #
#         ./klv.py /root/kismet-logs/                                      #
#         ./klv.py -t csv /root/kismet-logs/                               #
#                                                                          #
#  Requirements: Python                                                    #
#                one or more Kismet .netxml log files                      #
#                                                                          #
#  Website: http://klv.professionallyevil.com                              #
#  Author:  Nathan Sweaney - nathan@sweaney.com                            #
#  Date:   July 9, 2013                                                    #
#                                                                          #
#                                                                          #
############################################################################

import os    
import sys
import datetime
import xml.etree.ElementTree as ET
import argparse

# variables
oui_file = open('oui.txt')
network_matrix = []
bssid_list = []
log_file_list = []

now = datetime.datetime.now()
# used on the HTML page output
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# process command-line arguments
parser = argparse.ArgumentParser(description='Kismet Log Viewer v2.01 creates a readable summary of Kismet .netxml log files.')
parser.add_argument('log_file_path', metavar='LogFilePath',
                   help='A directory containing one or more Kismet .netxml log files. KLV will process all .netxml files in the directory but will ignore all other files.')
parser.add_argument('-o', default="html", choices=['html', 'csv'],
                   help='Output format (default: html)')
parser.add_argument('-s', default="essid", choices=['essid', 'security', 'bssid', 'manufacturer', 'clients', 'packets'],
                   help='Sort output (default: essid) (***unfinished***)')
parser.add_argument('-g', default="no", choices=['yes', 'no'],
                   help='Group by essid (default: no) (***unfinished***)')
parser.add_argument('-t', default="beacon", nargs=1, choices=['beacon', 'request', 'response'],
                   help='Show network types (default: beacon only) (***unfinished***)')
args = parser.parse_args()
output_format = args.o

# add the ending slash in case it was left off
if args.log_file_path[-1:] <> "/":
   args.log_file_path = args.log_file_path + "/"

def main():
   # cycle through each file in the directory
   files_in_dir = os.listdir(args.log_file_path)
   for file_in_dir in files_in_dir:
      if file_in_dir[-7:] == ".netxml":
         print "Adding file: ", file_in_dir 
         log_file_list.append(file_in_dir)

         xml_tree = ET.parse(args.log_file_path + file_in_dir)
         xml_root = xml_tree.getroot()
   
         # loop through each XML node of type "wireless-network"
         for network in xml_root.findall('wireless-network'):
   
            network_type = network.get('type')
   
            # ignoring probes right now
            if network_type <> 'probe':
               network_essid = ""
               network_encryption = ""
               network_bssid = ""
               network_manufacturer = ""
               network_oui = ""
#Added by j0nk0
               network_client = ""
#/Added by j0nk0
               for network_detail in network:
   
                  if network_detail.tag == 'SSID':
                     for child_network in network_detail:
                        if child_network.tag == 'essid':
                           if child_network.attrib.get("cloaked") == "true":
                              cloaked = " &lt;cloaked&gt;"
                           else:
                              cloaked = ""
                           if child_network.text is None:
                              network_essid = "" + cloaked
                           else:
                              network_essid = child_network.text + cloaked
   
                        if child_network.tag == 'encryption':
                           network_encryption += child_network.text + "<br />"
   
                  elif network_detail.tag == 'BSSID':
                     network_bssid = network_detail.text
                     network_oui = network_bssid[0:2] + "-" + network_bssid[3:5] + "-" + network_bssid[6:8]
                     oui_file.seek(0)
                     #!@todo this is inefficient
                     for line in oui_file:
                        if network_oui in line:
                           network_manufacturer = line[20:]
                           break
               
#Added by j0nk0
                  if network_detail.tag == 'wireless-client':
                     for child_network in network_detail:
                        if child_network.tag == 'client-mac':
                           if child_network.text is None:
                              network_client = child_network.text
   
                        if child_network.tag == 'client-mac':
                           network_client += child_network.text + "<br />"
#/Added by j0nk0
                
                  elif network_detail.tag == 'channel':
                     network_channel = network_detail.text
   
               if network_bssid not in bssid_list:
                  bssid_list.append(network_bssid)
#Edited by j0nk0
                  network_matrix.append([network_essid, network_channel, network_encryption, network_bssid, network_manufacturer, network_client])
#/Edited by j0nk0
   

   if output_format == 'html':
      create_html_file(network_matrix)
   elif output_format == 'csv':
      create_csv_file(network_matrix)
   
#output to CSV
def create_csv_file(network_matrix):
   summary_file = open('kismet-log-summary.csv','w')
   for network in network_matrix:
      summary_file.write(network[0] + ',' +network[1] + ',' +network[2] + ',' +network[3] + ',' +network[5] + ',' +network[6] + '\n')
   summary_file.close()

# output to HTML
def create_html_file(network_matrix):

   summary_file = open('kismet-log-summary.html','w')

   # print header
   summary_file.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
   summary_file.write('<html>\n')
   summary_file.write('  <head>\n')
   summary_file.write('    <title>Kismet Log Summary</title>\n')
   summary_file.write('  </head>\n')
   summary_file.write('  <body>\n')
   summary_file.write('    <table width="760" border="0" align="center" cellpadding="5" cellspacing="1" bgcolor="#efefef">\n')
   summary_file.write('      <tr>\n')
   summary_file.write('        <td colspan=5 align="left">Kismet Log Summary</td>\n')
   summary_file.write('        <td colspan=2 align="right"><font size="1">Created: ' + timestamp + '</font></td>\n')
   summary_file.write('      </tr>\n')

   summary_file.write('      <tr bgcolor="#cecece">\n')
   summary_file.write('        <th></th>\n')
   summary_file.write('        <th align=left><font size="1">Name (ESSID)</font></th>\n')
   summary_file.write('        <th><font size="1">Channel</font></th>\n')
   summary_file.write('        <th><font size="1">Security</font></th>\n')
   summary_file.write('        <th><font size="1">BSSID</font></th>\n')
   summary_file.write('        <th><font size="1">Manufacturer</font></th>\n')
   summary_file.write('        <th><font size="1">&lt;Clients&gt;</font></th>\n')
   summary_file.write('        <th><font size="1">&lt;Packets&gt;</font></th>\n')
   summary_file.write('      </tr>\n')

   row_toggle = 1
   row = 1
   for network in network_matrix:

      # this flip-flops the background color for each row
      if row_toggle == 1:
         summary_file.write('      <tr>\n')
         row_toggle = 0
      else:
         summary_file.write('      <tr bgcolor="#FFFFFF">\n')
         row_toggle = 1

      summary_file.write('        <td align="center"><font size="1">' + str(row) + '</font></td>\n')
      summary_file.write('        <td><font size="1">' + network[0] + '</font></td>\n')
      summary_file.write('        <td align="center"><font size="1">' + network[1] + '</font></td>\n')
      summary_file.write('        <td align="center"><font size="1">' + network[2] + '</font></td>\n')
      summary_file.write('        <td align="center"><font size="1">' + network[3] + '</font></td>\n')
      summary_file.write('        <td align="center"><font size="1">' + network[4] + '</font></td>\n')
#Added by j0nk0
      summary_file.write('        <td align="center"><font size="1">' + network[5] + '</font></td>\n')
#/Added by j0nk0
      summary_file.write('        <td align="center"><font size="1">' +'</font></td>\n')
      summary_file.write('      </tr>\n')
      row += 1

   summary_file.write('    </table>\n')
   summary_file.write('<br />\n')
   
   # print list of log files
   summary_file.write('    <table width="760" border="0" align="center" cellpadding="5" cellspacing="1" bgcolor="#efefef">\n')
   summary_file.write('      <tr bgcolor="#cecece">\n')
   summary_file.write('        <td align="center">Log files included:</td>\n')
   summary_file.write('      </tr>\n')

   row_toggle = 1
   for log_file in log_file_list:
      # this flip-flops the background color for each row
      if row_toggle == 1:
         summary_file.write('      <tr>\n')
         row_toggle = 0
      else:
         summary_file.write('      <tr bgcolor="#FFFFFF">\n')
         row_toggle = 1
   
      summary_file.write('        <td align="center"><font size="1">' + log_file + '</font></td>\n')
      summary_file.write('      </tr>\n')
   
   summary_file.write('    </table>\n')

   # print footer
   summary_file.write('<br />\n')
   summary_file.write('    <table width="760" border="0" align="center" cellpadding="5" cellspacing="1" bgcolor="#efefef">\n')
   summary_file.write('      <tr>\n')
   summary_file.write('        <td></td>\n')
   summary_file.write('      </tr>\n')
   summary_file.write('      <tr bgcolor="#FFFFFF">\n')
   summary_file.write('        <td align="center"><font size="1">Kismet Log Viewer v2.01 - written by <a href="mailto:nathan@secureideas.com">Nathan Sweaney</a></font></td>\n')
   summary_file.write('      </tr>\n')
   summary_file.write('      <tr>\n')
   summary_file.write('        <td></td>\n')
   summary_file.write('      </tr>\n')
   summary_file.write('    </table>\n')
   
   summary_file.write('  </body>\n')
   summary_file.write('</html>\n')

   summary_file.close()


main()

"""
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
* Support GPS info
* create variable for version number instead of spreading it through code
"""
