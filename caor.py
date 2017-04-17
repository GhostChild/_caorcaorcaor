import fileinput
import os
import re
import sys
import json
import threading
import getopt
import vapoursynth as vs

try:
    opts, args = getopt.getopt(sys.argv[1:], "hv:t:", ["help", "vpy=", "trimnum="])


except getopt.GetoptError:
    print("Error,please input <vpyfile> and <trimnum> like \'-v <xxx.vpy> -t <2>\'")



for opt,arg in opts:
    if opt == "-h":
        print
        '-v <vpyfile> -t <trimnum>'
        print
        'or: --vpy=<vpyfile> --trimnum=<trimnum>'

    if opt in ("-v","--vpy"):
        script=arg

    if opt in ("-t","--trimnum"):
        trim_num=arg
# vpypath=os.path.abspath(script)
# dirname=os.path.dirname(vpypath)


trim_num=int(trim_num)
os.system("copy %s vpy.py" % (script))
sys.path.append('./')

# script="caor0.vpy"
# trim_num=2

#=================get all frames=========================
# vpyname=re.match("(.*)\.",script).group(1)
# print(vpyname)


# vpy =__import__(vpyname)
from vpy import src
frames=src.num_frames
print("all frmaes is:%s,trim to %s clip"%(frames,trim_num))


with open("config.json", 'r') as j:
    config=json.load(j)


def get_sourceln(source):
    vpy = fileinput.input(source, mode="r")
    for line in vpy:
        str = re.match(".*Source.*", line)
        if str!=None:
                #result=str.group()
                #print(result)
                trim_point=vpy.lineno()
                #print(trim_point)
    return trim_point

def wirte_trim(source,trimln,start,end):
    vpy = fileinput.input(source, mode="r")
    for line in vpy:
        trimfile_name="%s.trim%d.vpy" % (script,t)
        write = open(trimfile_name, "a+")
        write.write(line)
        if vpy.lineno() == trimln:
            write.write("src=core.std.Trim(src,%d,%d)\n"%(start,end))
            write.close()
    return trimfile_name

def encode(trimscript,vspipepath,vspipe,x26xpath,x26x):
    encode=("%s %s %s - | %s %s -o %s.264 -" % (vspipepath, vspipe, trimscript, x26xpath, x26x,trimscript))
    print(encode)
    os.system("%s" % (encode))

class trimThread (threading.Thread):
    def __init__(self,trimfile):
        threading.Thread.__init__(self)
        self.trimfile=trimfile

    def run(self):
        encode(self.trimfile,config["vspipepath"],config["vspipe"],config["x26xpath"],config["x26x"])


trim_p=get_sourceln(script)
# print(trim_p)
trimlist=[]

# ================frame trim==============================
trim=frames//trim_num

start=0
for t in range(trim_num):
    if t == trim_num - 1:
        # print(start,frames-1)
        trim_file=wirte_trim(script, trim_p, start, frames-1)
        trimlist.append(trim_file)
        break

    end=trim+trim*t

    # print(start, end)
    trim_file =wirte_trim(script,trim_p,start,end)
    trimlist.append(trim_file)
    start=end+1

os.system("del /F vpy.py")
#
#
threads=[]
for list in trimlist:
    threads.append(trimThread(list))

for t in threads:
    t.start()






