#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# The Initial Developer of the original Code is
# Murali Krishna Nandigama
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# 
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import os,fnmatch,re,sys

def get_child_files(filename):
    yield filename
    for line in open(filename,"r").readlines():
        if line.startswith("include"):
            childfilename=os.path.join(os.path.dirname(filename),line.split()[1])
            for child in get_child_files(childfilename):
                yield child
            

def find_unlisted_files(manifestFileName):
    
   
    manifestFileName = sys.argv[1]
    
    refTestfiles = list(get_child_files(manifestFileName))
    # open two output files to write the results
    f1 = open('found.txt','w')
    f1.truncate()
    f2 = open('notfound.txt','w')
    f2.truncate()
    for file in refTestfiles:
        print file
        # Get the base directory of the reftest.list file and scan all files.
        dirpath= os.path.dirname(file)
        excludeList= manifestFileName + "|Makefile|passinner|DS_Store|[Rr][Ee][Aa][Dd][Mm][Ee]|[Ll][Ii][Cc][Ee][Nn][Ss][Ee]|\^headers\^"
        for eachFile in os.listdir(dirpath):
            if os.path.isfile(os.path.join(dirpath,eachFile)) and not re.search(excludeList,eachFile):
                #print eachFile
                maxindex = 0
                for myfile in refTestfiles:
                    infile=open(myfile,"r")
                    text=infile.read()
                    infile.close()
                    index = text.find(eachFile)
                    if index > 0:
                        print >> f1, "found", eachFile, "in", os.path.join(dirpath,myfile)
                        maxindex=index
                if maxindex == 0:
                    # So, this file is not present in any reftest.list files.
                    # Now let us check if any of the files at this file's level
                    # or sub directory level contain this file.
                    mindex=0
                    for eachFile2 in os.listdir(dirpath):
                        if os.path.isfile(os.path.join(dirpath,eachFile2)) and not re.search(eachFile,eachFile2):
                            infile=open(os.path.join(dirpath,eachFile2),'r')
                            text=infile.read()
                            infile.close()
                            index = text.find(eachFile)
                            if index > 0:
                                print >> f1, "found", eachFile, "in", os.path.join(dirpath,eachFile2)
                                mindex=index
                    if mindex == 0:
                         print >>f2, os.path.join(dirpath,eachFile),"is not referenced in any file"
                
            
    f1.close()
    f2.close()
    
# Let us get the list of all reflist.list files from src directory now!!

if __name__ == '__main__':
     find_unlisted_files(sys.argv[1])

