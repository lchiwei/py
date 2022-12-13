import subprocess
import argparse
import pathlib
import os
import shutil

# # subprocess.run(("ssh", "<REMOTE UNAME>@<REMOTE IP/HOSTNAME>", "free", "-m"))
# subprocess.run(("ssh", "astro00@140.114.94.176", "free", "-m"))


def movessh():
    maciup = "/Users/lchiwei/Downloads/astro/iup/"
    dest = "astro00@140.114.94.176:"
    linuxiup = "/home/astro00/2022Fall_ObsCourse/Myprecious/iup/"
    ipfile = "/Users/lchiwei/Downloads/astro/ip/"
    global files
    files = os.listdir(maciup)
    if files == []:
        return
    else:
        for file in files:
            iupfile = maciup + file

            command = ["scp", iupfile, dest + linuxiup]
            subprocess.run(command)

            os.remove(iupfile)
        return

def sextractor():
    linuxiup = "/home/astro00/2022Fall_ObsCourse/Myprecious/iup/"
    linuxip = "/home/astro00/2022Fall_ObsCourse/Myprecious/ip/"
    dest = "astro00@140.114.94.176"
    images = files
    global movename
    movename = []
    for image in files:
        oname = image.replace('.fits', '')
        name = 'p_' + oname

        movename.append(name)
        configname = name + ".config"
        code = 's/test/' + name + '/g'
        target ='/home/astro00/2022Fall_ObsCourse/Myprecious/iup/test.config'
        sed = "sed " + code + ' ' + target + " > " + linuxiup + configname
        cmd = ['ssh', dest, sed]
        subprocess.run(cmd)
        sex = 'sex ' + image + ' -c ' + configname
        mkdir = 'mkdir ' + linuxip + name
        mv = 'mv ' + '*' + oname + '* ' + linuxip + name
        cd = 'cd ' + linuxiup
        cmd = ['ssh', dest, cd, '&&', sex, '&&', mkdir, '&&', mv]
        subprocess.run(cmd)
    return

def moveback():
    linuxip = "/home/astro00/2022Fall_ObsCourse/Myprecious/ip/"
    dest = "astro00@140.114.94.176:"
    macip = '/Users/lchiwei/Downloads/astro/ip/'
    for name in movename:
        cmd = ['scp', '-r', dest + linuxip + name + '*', macip]
        subprocess.run(cmd)
    return

movessh()
sextractor()
moveback()
