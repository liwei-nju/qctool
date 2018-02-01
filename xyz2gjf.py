#!/usr/bin/env python
import sys, math
#
nargv   = len(sys.argv)
command = sys.argv[0]
#headdef = ''
HEADNAM = ''
itype   = 0
FILLST = []
#
ELEMNT = [ 'H' ,'He','Li','Be','B' ,  'C' ,'N' ,'O' ,'F' ,'Ne',
           'Na','Mg','Al','Si','P' ,  'S' ,'Cl','Ar','K' ,'Ca',
           'Sc','Ti','V' ,'Cr','Mn',  'Fe','Co','Ni','Cu','Zn',
           'Ga','Ge','As','Se','Br',  'Kr','Rb','Sr','Y' ,'Zr',
           'Nb','Mo','Tc','Ru','Rh',  'Pd','Ag','Cd','In','Sn',
           'Sb','Te','I' ,'Xe','Cs',  'Ba','La','Ce','Pr','Nd',
           'Pm','Sm','Eu','Gd','Tb',  'Dy','Ho','Er','Tm','Yb',
           'Lu','Hf','Ta','W' ,'Re',  'Os','Ir','Pt','Au','Hg',
           'Tl','Pb','Bi','Po','At',  'Rn','Fr','Ra','Ac','Th',
           'Pa','U' ,'Np','Pu','Am',  'Cm','Bk','Cf','Es','Fm',
           'Md','No','Lr','Rf','Db',  'Sg','Bh','Hs','Mt','Ds',
           'Rg', 'Uub','Uut','Uuq','Uup',  'Uuh']
nelem = len(ELEMNT)

#
# --- Read FILNAMs and arguments or print information for the program ---
#
if nargv == 2:
    argv = sys.argv[1]
    if argv == '-h' or argv == '--help':
        print "XYZ2GJF - Convert xyz file to gaussian input file"
        print ""
        print "usage: xyz2gjf [arguments] [file ..]       edit specified file(s)"
        print ""
        print "Arguments:"
        print "-h			Print Help (this message) and exit"
        print "-v			Print version information and exit"
        print "--type k		Defined GAMESS head (k=0,1,2)"
        print "			k=0: mp2/6-31G(d) 6d"
        print "			k=1: ccsd/6-31G(d) 6d"
        print "			k=2: ccsd(t)/6-311++G(d,p) 5d"
        print "--headfile HEADNAM	Use GAMESS headfile HEADNAM"
        sys.exit(1)
    elif argv == '-v' or argv == '--version':
        print "Version 0.01 (11 Aug 2010, 12:29)"
        sys.exit(1)
    elif argv[0] != '-':
        FILLST.append(argv)
    else:
        print "xyz2gjf: arguments error: " + argv + "; for help type \"xyz2gjf -h or xyz2gjf --help\""
        sys.exit(1)
else:
#   for arg in sys.argv[1:]:
    for k in range(1, nargv, 1):
        if k == 1:
            argp = ' '
            argn = sys.argv[k+1]
        elif k == nargv-1:
            argp = sys.argv[k-1]
            argn = ' '
        else:
            argp = sys.argv[k-1]
            argn = sys.argv[k+1]
        argv = sys.argv[k]

#       if argv == '--head':
#           headdef = argn
#           if headdef == ' ':
#               print "xyz2gjf: arguments error: undefined head; for help type \"xyz2gjf -h or xyz2gjf --help\""
#               sys.exit(1)
        if argv == '--headfile':
            if argn[0] == '-':
                print "xyz2gjf: arguments error: wrong gamess head file"
                sys.exit(1)
            else:
                HEADNAM = argn
        elif argv == '--type':
            if argn == ' ':
                argn = 'NONE'
            try:
                itype = int(argn)
            except:
                print "xyz2gjf: arguments error: wrong itype="+argn+"; for help type \"xyz2gjf -h or xyz2gjf --help\""
                sys.exit(1)
        elif argv[0] != '-' and argp[0] != '-':
            FILLST.append(argv)
        elif argv[0] != '-' and argp[0] == '-':
            continue
        else:
            print "xyz2gjf: arguments error: " + argv + "; for help type \"xyz2gjf -h or xyz2gjf --help\""
            sys.exit(1)
#
# --- Get GAUSSIAN Head ---
# ----------------------------
nproc  = "%nprocshared=4\n"
if itype == 0:
    memory = "%mem=900mw\n"
#   system = "# opt dftba\n"
    system = "# wB97XD/6-311++g(d,p) TD=(NStates=5,root=1) pop=npa density=current\n"
#   system = "# opt wB97XD/6-311++G(d,p)\n"
#   system = "# hf/6-31G(d,p) pop=(npa,esp)\n"
#   system = "# m06l/6-31G** nosymm temperature=298.0\n# Bomd(GradOnly,Rtemp=0,Ntraj=1,Maxpoints=2000,StepSize=1000)\n"
#   system = "# m062x/6-31g scf(conver=5) nosymm\n"
#   system = "# ccsd(t)=fulldir/aug-cc-pVDZ\n"
elif itype == 1:
    memory = "%mem=250mw\n"
    system = "#p ccsd/6-31G(d)\n"
elif itype == 2:
    memory = "%mem=500mw\n"
    system = "#p ccsd(t)/6-311++G(d,p)\n"
else:
    print "xyz2gjf: arguments error: wrong value itype="+ itype +"; for help type \"xyz2gjf -h or xyz2gjf --help\""
    sys.exit(1)
#title  = "lsqc{charge dis=3 [nosymm] prog=111}\n"
#title  = "lsqc{frag=read combcha maxsubfrag=3 dis=3 tkmd [scf(conver=5)] dim1}\n"
title  = "lsqc{dis=3 maxsubfrag=4 twofrag trifrag prog=111}\n"
ichmul = "0 1\n"
blank  = "\n" 
#
if HEADNAM != '':
    HEADFIL = open(HEADNAM, 'r')
    heads = HEADFIL.read()
#
# ----------------------------
#
nfiles = len(FILLST)
nerrfl = 0
#
# ----------------------------
#
for i in range(0, nfiles, 1):
    FILNAM = FILLST[i]
    SBNAMS = FILNAM.split('.')
    FILEXT = SBNAMS[-1].lower()
    if FILEXT == 'xyz':
        INPNAM = FILNAM
        FILNAM = '.'.join(SBNAMS[:-1])
    else:
        INPNAM = FILNAM + '.xyz'
    OUTNAM = FILNAM + '.gjf'
#   print "%3i  Input/output files = %s %s" %(i+1,INPNAM,OUTNAM)
    sys.stdout.write("%d %s --> %s  " %(i+1,INPNAM,OUTNAM))
#
    INPFIL = open(INPNAM, 'r')
    OUTFIL = open(OUTNAM, 'w')
#
    lines = INPFIL.readlines()
    nlines = len(lines)
    NAT = int(lines[0])
    sys.stdout.write("NATOM=%d  " %NAT)
#
# ----------------------------
    SBNAMS = FILNAM.split('/')  # new added 2016-04-24
    FILNAM = SBNAMS[-1]         # new added 2016-04-24
#
    chkpnt = "%chk=" + FILNAM +'.chk\n'
    if HEADNAM == '':
#       heads = memory + nproc
        heads = chkpnt + memory + nproc
        if nlines > 2*(NAT+1):
            heads = heads + system.strip() + ' geom=connectivity\n'
        else:
            heads = heads + system
        heads = heads + blank + title + blank + ichmul
#
    OUTFIL.write(heads)
#
    NERR = 0
    for line in lines[2:NAT+2]:
        IERR = 0
        atminf = line.split()
        L = len(atminf[0])
        if L == 1:
           atom = atminf[0].upper()
        else:
           atom = atminf[0][0].upper() + atminf[0][1:].lower()
#
        nucl = 0
        for i in range(0,nelem,1):
            if atom == ELEMNT[i]:
                nucl = i + 1
#
        if nucl == 0:
            IERR = IERR + 1
            OUTFIL.write("#%d xyz2gjf: can not find %s in periodoc table\n" %(IERR,atom))
#
        try:
            x = float(atminf[1])
            y = float(atminf[2])
            z = float(atminf[3])
        except:
            IERR = IERR + 1
            OUTFIL.write("#%d xyz2gjf: format error; \"ATOM X Y Z\" is required\n" %IERR)
#
        if IERR == 0:
            OUTFIL.write(" %-3s%20.10f%20.10f%20.10f\n" %(atom,x,y,z))
        else:
            OUTFIL.write("Total %d error(s) find in line: %s" %(IERR,line))
            NERR = NERR + IERR
#
    OUTFIL.write("\n")
#   OUTFIL.write("@GAUSS_EXEDIR:dftba.prm\n")
#   OUTFIL.write("\n")
    line = lines[NAT+2].strip()
    if line != '':
        NERR = NERR + 1
        OUTFIL.write("#%d xyz2gjf: line %d in xyz file is not blank\n" %(IERR,NAT+3))
#
#   for k in range(0,nlines,1):
    for line in lines[NAT+3:nlines]:
        line = line.strip()
        OUTFIL.write(' '+line+'\n')
#   OUTFIL.write("\n")
#
    if NERR == 0:
        sys.stdout.write("Sucessful!\n")
    else:
        sys.stdout.write("Failed: %d error(s) found!\n" %NERR)
        nerrfl = nerrfl + 1
#
    INPFIL.close()
    OUTFIL.close()
#
sys.stdout.write("%d of %d files failed!\n" %(nerrfl,nfiles))
#
