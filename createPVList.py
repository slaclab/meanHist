import os
import meme.names

def createPVList():
  # creates a list of lists - each smaller one is a list of PVs for 
  # a given requested plot like insulating vacuum, Line A temps, etc.
  # The big list is in order of the pulldown on the GUI.
  # The items in the smaller lists are sorted by unit number
  # Beware: CM H1 & H2 come at the end. I'm not clever enough to fix

  #  need to be on a machine with mcc-dmz in EPICS_CA_ADDR_LIST for 
  #  meme.names to work

  # Going to double up the duty here and have it pass back a list of 
  #  which is the interesting parts of the pv name 
  #  for the xaxis named juicyBits
  #  If juicyBits = 1, then just use the 2nd field of PVN, if it's 2
  #  then use the 2nd and 3rd fields
  #  with apologies to anyone trying to read this.

  # Triple duty...
  #  Add ylabel for that plot type

  # Start with the vacuum lists

  #these will be lists of pvs for vac devices in the following systems:
  #   coupler, beamline, insulating, and scavenger pump, respectively.
  pvcplr=[]
  pvbl=[]
  pvins=[]
  pvscav=[]
  pvls=[]
  juicyBits=[]
  yLabels=[]

  # Double check that we're on the dmz network
  caAddrList=os.environ['EPICS_CA_ADDR_LIST']
  if 'mcc-dmz' not in caAddrList:
    print('Need to be on an mccdmz machine (srv01, mcclogin, lcls-prod02, etc)')
    return []

  # this is the 2nd part of the PV name in rough Z order (thanks DIAG0!)
  areas=['L0B','HTR','COL0','DIAG0','L1B','BC1B','COL1','L2B','BC2B','EMIT2',
  'L3B','EXT','DOG']

  for nn in range(13,28):
    areas.append('BPN'+str(nn))
  areas.append('SPH')
  areas.append('SPD')
  areas.append('SPS')

  # cycle through areas
  for area in areas:
    # fetch list of vac PVs in area
    pvl=meme.names.list_pvs('V%:'+area+':%:P')
    #print('area {0} npvs {1}'.format(area,len(pvl)))
    #Check for vgcc/vgpr that feed into VGXX
    for pvxx in pvl:
      if 'VGXX' in pvxx:
        for idpv,pv in enumerate(pvl):
          if 'VGCC' in pv or 'VGPR' in pv:
            if pv[4:]==pvxx[4:]:
              pvl[idpv]=''
    # VGXX:L2B:1449 doesn't exist
    if area=='L2B':
      pvl.remove('VGXX:L2B:1449:P')
    # remove empty strings i.e. VGCC and VGPR that are covered by a VGXX
    pvl=list(filter(None,pvl))

    # make VPIOs end with PMON
    # and VGXX end with COMBO_P
    for id,pv in enumerate(pvl):
      if 'VGXX' in pv:
        pvl[id]=pvl[id][:-1]+'COMBO_P'
      elif 'VPIO' in pv:
        pvl[id]=pvl[id]+'MON'

    # sort by unit number
    def sortThird(pvn):
      unitnostr=pvn.split(':')[2]
      try:
        unitno=int(unitnostr)
      except:
        try:
          unitnostr='1'+unitnostr[1:]
          unitno=int(unitnostr)
        except:
          unitno=9999
      return unitno

    # sort by unit number - feels awfully clever
    pvl.sort(key=sortThird)

    # figure out if device is for
    #    beamline, coupler, insulating vacuum, or scav pump system
    coupler=['09', '14', '19', '39', '49']

    for pv in pvl:
      # split the pv at the colons and scrutinize the unit number (field [2])
      pvspl=pv.split(':')
      # find four digit unit numbers
      if len(pvspl[2])==4:
        # put in right list based on last two digits
        if pvspl[2][-2:] in coupler:
          pvcplr.append(pv)
        # insulating vac devices
        elif pvspl[2][-2:]=='96':
          pvins.append(pv)
        # scav pump system
        elif pvspl[2][-2:]=='95':
          pvscav.append(pv)
        # beamline devices
        else:
          pvbl.append(pv)
      # if not a 4-digit number, then it's a beamline device
      else:
        pvbl.append(pv)

  # Packup return variables
  pvls.append(pvins)
  juicyBits.append(2)
  yLabels.append('Pressure (Torr)')

  pvls.append(pvscav)
  juicyBits.append(2)
  yLabels.append('Pressure (Torr)')

  pvls.append(pvcplr)
  juicyBits.append(2)
  yLabels.append('Pressure (Torr)')

  pvls.append(pvbl)
  juicyBits.append(2)
  yLabels.append('Pressure (Torr)')

# CRYO - so much easier than vacuum...
  pvls.append(meme.names.list_pvs('CTE:%:UH:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:DH:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('ACCL:%:%:STEPTEMP'))
  juicyBits.append(2)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('ACCL:%:%:CPLRTEMP1'))
  juicyBits.append(2)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('ACCL:%:%:CPLRTEMP2'))
  juicyBits.append(2)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:V%:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:A1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:B1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:B2:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:C1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:D1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:E1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:F1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CTE:%:%:S1:TEMP'))
  juicyBits.append(1)
  yLabels.append('Temperature ($^\circ$K)')

  pvls.append(meme.names.list_pvs('CLL:CM%:%:%:LVL'))
  juicyBits.append(1)
  yLabels.append('Liquid Level (%)')

  pvls.append(meme.names.list_pvs('CPT:CM%:%:%S:PRESS'))
  juicyBits.append(1)
  yLabels.append('Two-phase line pressure (bara)')

  pvls.append(meme.names.list_pvs('CHTR:%:%:HV:POWER_RBV'))
  juicyBits.append(1)
  yLabels.append('Heater Power (Watts)')

  pvls.append(meme.names.list_pvs('CPV:%:3001:JT:POS_RBV'))
  juicyBits.append(1)
  yLabels.append('Valve Percentage Open (%)')

  return pvls, juicyBits, yLabels

