#!/usr/bin/env python
import sys, math
#
nargv   = len(sys.argv)
command = sys.argv[0]
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
        print "GJF2XYZ - Convert gaussian input gjf/com file to xyz file"
        print "          Default file extension is .gjf. Must type full name for .com file"
        print ""
        print "usage: gjf2xyz [arguments] [file ..]       edit specified file(s)"
        print ""
        print "Arguments:"
        print "-h			Print Help (this message) and exit"
        print "-v			Print version information and exit"
        sys.exit(1)
    elif argv == '-v' or argv == '--version':
        print "Version 0.01 (11 Aug 2010, 12:28)"
        sys.exit(1)
    elif argv[0] != '-':
        FILLST.append(argv)
    else:
        print "gjf2xyz: arguments error: " + argv + "; for help type \"gjf2xyz -h or gjf2xyz --help\""
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

        if argv[0] != '-' and argp[0] != '-':
            FILLST.append(argv)
        elif argv[0] != '-' and argp[0] == '-':
            continue
        else:
            print "gjf2xyz: arguments error: " + argv + "; for help type \"gjf2xyz -h or gjf2xyz --help\""
            sys.exit(1)
#
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
    if FILEXT == 'gjf':
        INPNAM = FILNAM
        FILNAM = '.'.join(SBNAMS[:-1])
    elif FILEXT == 'com':
        INPNAM = FILNAM
        FILNAM = '.'.join(SBNAMS[:-1])
    else:
        INPNAM = FILNAM + '.gjf'
    OUTNAM = FILNAM + '.xyz'
    sys.stdout.write("%d %s --> %s  " %(i+1,INPNAM,OUTNAM))
#
    INPFIL = open(INPNAM, 'r')
    OUTFIL = open(OUTNAM, 'w')
#
    lines = INPFIL.readlines()
#
    NERR = 0
    NAT  = 0
    nlines = len(lines)
#
    nblank = 0
    for k in range(0,nlines,1):
        line = lines[k].upper().strip()
        m = len(line)
#       sys.stdout.write("# %s #\n" %line)
        if line == '':
            if nblank == 0:
               k0 = k+1
            elif nblank == 1:
               k1 = k+2
            elif nblank == 2:
               k2 = k
            nblank = nblank + 1
    title = lines[k0].strip()
#
    NAT = k2 - k1
    OUTFIL.write("%d\n" %NAT)
    OUTFIL.write("%s\n" %title)
#
    for k in range(k1,k2,1):
        line = lines[k]
        atminf = line.split()
#
        try:
#           nucl = float(atminf[1])
            x = float(atminf[1])
            y = float(atminf[2])
            z = float(atminf[3])
#
            L = len(atminf[0])
            if L == 1:
                atom = atminf[0].upper()
            else:
                atom = atminf[0][0].upper() + atminf[0][1:].lower()
#
            OUTFIL.write(" %-3s%25.16f%25.16f%25.16f\n" %(atom,x,y,z))
        except:
            continue
#
    sys.stdout.write("NATOM=%d  " %NAT)
    OUTFIL.write("\n")
#
    for line in lines[k2+1:nlines]:
        line = line.strip()
        OUTFIL.write(' '+line+'\n')
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
