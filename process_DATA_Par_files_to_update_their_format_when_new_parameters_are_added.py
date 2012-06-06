# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:00:00 2011
Updated on Fri Jun 5 2012

Processing of Par_file to update them to new format

Usage : "python PathTo/EXAMPLES/ProcessParFileParametersToNewRelease.py"
This will process all Par_file starting from current directory

@author: Cristini Paul, Laboratoire de Mecanique et d'Acoustique, CNRS, Marseille, France
"""
import os, string, sys
from os import listdir, walk
from string import capitalize
from shutil import copy, move
from os.path import exists

class InfoSEM:
    def __init__(self,titre='Simulation',f0=10.,source_type=1):
        self.title = titre
        self.f0 = f0
        self.source_type = source_type
    def __str__(self):
        return self.title+'\n'+'f0= '+str(self.f0)+' Hz'
#
def OuvreParFile(fic):
    SEM=InfoSEM()
    f = file(fic,'r')
    lignes= f.readlines()
    f.close()
    # Lists of variables
    if exists(fic):
        # Numerical variables
        VariableNum=['imagetype']
    else:
        print 'No Par_file found !'
        return
    #
    for var in VariableNum:
        print var
        for ligne in lignes:
            lsplit=string.split(ligne)
            if lsplit!= []:
                if lsplit[0]==var:
                    exec 'SEM.'+var+'='+string.replace(string.split(''.join(ligne))[2],'d','e')
                    break
    return SEM
#------------------------------------------------------------------------------
def LoadLig(Fichier):
    f = open(Fichier,'r')
    ligs= f.readlines()
    f.close()
    return ligs
#------------------------------------------------------------------------------
def mylister(currdir):
    for file in os.listdir(currdir):
        path=os.path.join(currdir, file)
        if not os.path.isdir(path):
            Fichiers.append(path)
        else:
            mylister(path)
#------------------------------------------------------------------------------
def ProcessParfile_r19201(fic):
    # Open the file and get all lines from Par_file
    ligs= LoadLig(fic)
    # Test if already processed
    for lig in ligs:
        if 'ADD_PERIODIC_CONDITIONS' in lig:
            print '----> '+fic+' already processed to r19201'            
            return
    # New additions to the Par_file
    a1='PERFORM_CUTHILL_MCKEE           = .false.        # perform ' + \
    'inverse Cuthill-McKee (1969) optimization/permutation for mesh ' + \
    'numbering (can be very costly and not very useful)\n'
    a2='USER_T0                         = 0.0d0          # use this t0' + \
    ' as earliest starting time rather than the automatically calculated one\n'
    a3='SU_FORMAT                       = .false.        # output ' + \
    'seismograms in Seismic Unix format (adjoint traces will be read' + \
    ' in the same format)\n'
    a4='factor_subsample_image          = 1              # factor to' + \
    ' subsample color images output by the code (useful for very large models)\n'+ \
    'POWER_DISPLAY_COLOR             = 0.30d0         # non linear ' + \
    'display to enhance small amplitudes in color images\n'+ \
    'DRAW_WATER_CONSTANT_BLUE_IN_JPG = .true.         # display acoustic' + \
    ' layers as constant blue in JPEG images, because they likely correspond to water\n'
    a5='US_LETTER                       = .false.        # US letter ' + \
    'paper or European A4\n'+ \
    'USE_SNAPSHOT_NUMBER_IN_FILENAME = .false.        # use snapshot ' + \
    'number in the file name of JPEG color snapshots instead of the time step\n'
    a6='\n# for horizontal periodic conditions: detect common points' + \
    ' between left and right edges\n'+ \
    'ADD_PERIODIC_CONDITIONS         = .false.\n\n'+ \
    '# horizontal periodicity distance for periodic conditions\n'+ \
    'PERIODIC_horiz_dist             = 0.3597d0\n\n'+ \
    '# grid point detection tolerance for periodic conditions\n'+ \
    'PERIODIC_DETECT_TOL             = 3.3334d-6\n'  
    #--------------------------------------------------------------------------
    # Add new parameters
    # 
    for ilg, lig in enumerate(ligs):
        if lig.startswith('partitioning'):
            ligs.insert(ilg+1,a1)

        if lig.startswith('deltat'):
            ligs.insert(ilg+1,a2)

        if lig.startswith('rec_normal'):
            ligs.insert(ilg+1,a3)

        if lig.startswith('subsamp'):
            ligs[ilg]=string.replace(ligs[ilg],'subsamp           ','subsamp_postscript',1)
            ligs.insert(ilg+1,a4)

        if lig.startswith('sizemax'):
            ligs.insert(ilg+1,a5)
            
        if lig.startswith('absorbing_conditions'):
            ligs.insert(ilg+1,a6)
    #
    move(fic,fic+'.before_update_to_r19201')
    fm = open(fic,'w')
    fm.writelines(ligs)
    fm.close()
    #
    print 'xxxxx------> '+fic+' processed to r19201'
    return
#------------------------------------------------------------------------------
def ProcessParfile_r19340(fic):
    # Open the file and get all lines from Par_file
    ligs= LoadLig(fic)
    # Test if already processed
    for lig in ligs:
        if 'nreceiversets' in lig:
            print '----> '+fic+' already processed to r19340'            
            return
    #
    # Add new parameters
    # 
    for ilg, lig in enumerate(ligs):
        if lig.startswith('nreceiverlines'):
            ligs[ilg]=ligs[ilg].replace('lines','sets ')
    #
    move(fic,fic+'.before_update_to_r19340')
    #
    fm = open(fic,'w')
    fm.writelines(ligs)
    fm.close()
    #
    print 'xxxxx------> '+fic+' processed to r19340'
    return
#------------------------------------------------------------------------------
def ProcessParfile_r19346(fic):
    # Open the file and get all lines from Par_file
    ligs= LoadLig(fic)
    # Test if already processed
    for lig in ligs:
        if 'ATTENUATION_PORO_FLUID_PART' in lig:
            print '----> '+fic+' already processed to r19346'            
            return
    #--------------------------------------------------------------------------
    # Add new parameters
    # 
    for ilg, lig in enumerate(ligs):
        if lig.startswith('TURN_ATTENUATION_ON'):
            ligs[ilg]=ligs[ilg].replace('TURN_ATTENUATION_ON           ', \
                            'ATTENUATION_VISCOELASTIC_SOLID')
        if lig.startswith('TURN_VISCATTENUATION_ON'):
            ligs[ilg]=ligs[ilg].replace('TURN_VISCATTENUATION_ON    ', \
                            'ATTENUATION_PORO_FLUID_PART')
    #
    move(fic,fic+'.before_update_to_r19346')
    #
    fm = open(fic,'w')
    fm.writelines(ligs)
    fm.close()
    #
    print 'xxxxx------> '+fic+' processed to r19346'
    return
#------------------------------------------------------------------------------
def ProcessParfile_r19521(fic):
    # Open the file and get all lines from Par_file
    ligs= LoadLig(fic)
    # Test if already processed
    for lig in ligs:
        if 'time_stepping_scheme' in lig:
            print '----> '+fic+' already processed to r19521'            
            return
    #
    a1='time_stepping_scheme            = 1   # 1 = Newmark (2nd order), \
    2 = LDDRK4-6 (4th-order 6-stage low storage Runge-Kutta), \
    3 = classical 4th-order 4-stage Runge-Kutta\n'

    #--------------------------------------------------------------------------
    # Add new parameters
    # 
    for ilg, lig in enumerate(ligs):
        if lig.startswith('USER_T0'):
            ligs.insert(ilg+1,a1)
    #
    move(fic,fic+'.before_update_to_r19521')
    #
    fm = open(fic,'w')
    fm.writelines(ligs)
    fm.close()
    #
    print 'xxxxx------> '+fic+' processed to r19521'
    return
#------------------------------------------------------------------------------
def ProcessParfile_r19804(fic):
    # Open the file and get all lines from Par_file
    ligs= LoadLig(fic)
    
    for ilg, lig in enumerate(ligs):
        if lig.startswith('PERFORM_CUTHILL_MCKEE'):
            ligs[ilg]=ligs[ilg].replace('.true.','.false.')

    # Test if already processed
    for lig in ligs:
        if 'ADD_SPRING_TO_STACEY' in lig:
            print '----> '+fic+' already processed to r19804'            
            return
    #
    a1='ADD_SPRING_TO_STACEY            = .true.\n'

    #--------------------------------------------------------------------------
    # Add new parameters
    # 
    for ilg, lig in enumerate(ligs):
        if lig.startswith('absorbing_conditions'):
            ligs.insert(ilg+1,a1)
    #
    move(fic,fic+'.before_update_to_r19804')
    #
    fm = open(fic,'w')
    fm.writelines(ligs)
    fm.close()
    #
    print 'xxxxx------> '+fic+' processed to r19804'
    return
#------------------------------------------------------------------------------
def ProcessParfile_r20307(fic):
    # Open the file and get all lines from Par_file
    ligs= LoadLig(fic)
    
    # Test if already processed
    for lig in ligs:
        if 'NSTEP_BETWEEN_OUTPUT_SEISMOS' in lig:
            print '----> '+fic+' already processed to r20307'            
            return
            
    # Change the jpeg imagetype accordingly to the original values
    if Data.imagetype==1: imagetype_new = 3  
    if Data.imagetype==2: imagetype_new = 6
    if Data.imagetype==3: imagetype_new = 9
    if Data.imagetype==4: imagetype_new = 10
    
    # Change first line
    ligs[0]='# title of job\n'
    
    # New parameters
    a0='NSTEP_BETWEEN_OUTPUT_SEISMOS    = 5000000        # every how many' + \
    ' time steps we save the seismograms (costly, do not use a very small' + \
    ' value; if you use a very large value that is larger than the total ' + \
    'number of time steps of the run, the seismograms will automatically ' + \
    'be saved once at the end of the run anyway)\n' + \
    'save_ASCII_seismograms          = .true.         # save seismograms ' + \
    'in ASCII format or not\n' + \
    'save_binary_seismograms_single  = .true.         # save seismograms ' + \
    'in single precision binary format or not (can be used jointly with' + \
    ' ASCII above to save both)\n' + \
    'save_binary_seismograms_double  = .false.        # save seismograms' + \
    ' in double precision binary format or not (can be used jointly with' + \
    ' both flags above to save all)\n'
    #
    a1='subsamp_seismos                 = 1              # subsampling of ' + \
    'the seismograms to create smaller files (but less accurately ' + \
    'sampled in time)\n'
    #
    a2='NSTEP_BETWEEN_OUTPUT_IMAGES     = 100            # every how ' + \
    'many time steps we draw JPEG or PostScript pictures of the ' + \
    'simulation (costly, do not use a very small value)\n'
    #
    a3='imagetype_JPEG                  = '+str(imagetype_new)+'     ' + \
    '         # display ' + \
    '1=displ_Ux 2=displ_Uz 3=displ_norm 4=veloc_Vx 5=veloc_Vz ' + \
    '6=veloc_norm 7=accel_Ax 8=accel_Az 9=accel_norm 10=pressure\n'
    #
    a4='DRAW_SOURCES_AND_RECEIVERS      = .true.         # display ' + \
     'sources as orange crosses and receivers as green squares in' + \
     ' JPEG images or not\n'
    #
    a5='imagetype_postscript            = 1     ' + \
    '         # display 1=displ vector 2=veloc vector 3=accel vector;' + \
    ' small arrows are displayed for the vectors\n'
    #
    a6='NSTEP_BETWEEN_OUTPUT_WAVE_DUMPS = 100            # every how ' + \
    'many time steps we dump results of the simulation as ASCII or ' + \
    'binary files (costly, do not use a very small value)\n' + \
    'output_wavefield_dumps          = .false.        # output wave' + \
    ' field to a text file every NSTEP_BETWEEN_OUTPUT_TEXT_DUMPS time' + \
    ' steps (creates very big files)\n' + \
    'imagetype_wavefield_dumps       = 1              # display 1=displ' + \
    ' vector 2=veloc vector 3=accel vector 4=pressure\n' + \
    'use_binary_for_wavefield_dumps  = .false.        # use ASCII' + \
    ' or single-precision binary format for the wave field dumps\n####\n'
    a7='output_grid_ASCII               = .false.        # dump the' + \
    ' grid in an ASCII text file consisting of a set of X,Y,Z points or not\n'
    #
    for ilg, lig in enumerate(ligs):
        if lig.startswith('seismotype'):
            ligs[ilg] = ligs[ilg].replace('# record 1=displ 2=veloc' + \
            ' 3=accel 4=pressure','# record 1=displ 2=veloc 3=accel ' + \
            '4=pressure 5=curl of displ 6=the fluid potential')
            ligs.insert(ilg+1,a0)
            ligs.insert(ilg+2,a1)
        
        if lig.startswith('SU_FORMAT'):
            ligs[ilg] = ligs[ilg].replace('# output seismograms in Seismic' + \
            ' Unix format','# output single precision binary seismograms' + \
            ' in Seismic Unix format')
            ligs.insert(ilg-5,ligs.pop(ilg))
            
        if lig.startswith('NTSTEP_BETWEEN_OUTPUT_INFO'):
            ligs[ilg] = ligs[ilg].replace('NTSTEP','NSTEP')
            ligs[ilg] = ligs[ilg].replace('# display frequency in time ' + \
            'steps','# every how many time steps we display information' + \
            ' about the simulation (costly, do not use a very small value)')
            ligs.insert(ilg+1,a2)
            ligs.insert(ilg+5,ligs.pop(ilg+2)) #move output_postscript-snapshot
            ligs.insert(ilg+4,ligs.pop(ilg+2)) #move output_color_image
            ligs[ilg+4] = ligs[ilg+4].replace('# output color image of' + \
            ' the results','# output JPEG color image of the results' +\
            ' every NSTEP_BETWEEN_OUTPUT_IMAGES time steps or not')
            ligs.insert(ilg+4,'\n#### for JPEG color images ####\n')
            ligs.pop(ilg+2)
            ligs.insert(ilg+5,a3)
            ligs.insert(ilg+6,ligs.pop(ilg+13)) # move factor_subsample_image
            ligs.insert(ilg+7,ligs.pop(ilg+14)) # move POWER_DISPLAY_COLOR
            ligs.insert(ilg+8,ligs.pop(ilg+15)) # move DRAW_WATER...
            ligs[ilg+8] = ligs[ilg+8].replace('DRAW_WATER_CONSTANT' + \
            '_BLUE_IN_JPG =','DRAW_WATER_IN_BLUE              =')
            ligs.insert(ilg+8,a4)
            ligs.insert(ilg+10,ligs.pop(ilg+19)) # move USE_SNAPSHOT-NUMBER_IN
            ligs.insert(ilg+11,'\n#### for PostScript snapshots ####\n')
            ligs.insert(ilg+13,a5)
            
        if lig.startswith('US_LETTER'):
            ligs.insert(ilg+1,'\n#### for wavefield dumps ####\n')
            ligs.insert(ilg+2,a6)
            
        if lig.startswith('gnuplot                         ='):
            ligs.pop(ilg)
            
    for ilg, lig in enumerate(ligs):
        if lig.startswith('cutsnaps                        ='):
            ligs[ilg] = ligs[ilg].replace('# minimum amplitude in % for' + \
            ' snapshots','# minimum amplitude kept in % for the JPEG and' + \
            ' PostScript snapshots; amplitudes below that are muted')
            
        if lig.startswith('DRAW_WATER_IN_BLUE              ='):
            ligs[ilg] = ligs[ilg].replace('# display acoustic layers as' + \
            ' constant blue in JPEG images, because they likely correspond' + \
            ' to water','# display acoustic layers as constant blue in JPEG'+ \
            ' images, because they likely correspond to water in the case' + \
            ' of ocean acoustics or in the case of offshore oil industry' + \
            ' experiments (if off, display them as greyscale, as for ' + \
            'elastic or poroelastic elements, for instance for acoustic-' + \
            'only oil industry models of solid media)')
            
        if lig.startswith('output_grid '):
            ligs[ilg] = ligs[ilg].replace('output_grid        ','output_grid_Gnuplot')
            ligs.insert(ilg+1,a7)
            
        if lig.startswith('output_wavefield_snapshot       ='):
            ligs.pop(ilg)
              
    #
    move(fic,fic+'.before_update_to_r20307')
    #
    fm = open(fic,'w')
    fm.writelines(ligs)
    fm.close()
    #
    print 'xxxxx------> '+fic+' processed to r20307'
    return    
#------------------------------------------------------------------------------
if __name__=='__main__':
    ## List of all files of current directory
    Fichiers=[]
    mylister('.')
    #
    print '~'*80
    Ct_Par_file=0
    for fic in Fichiers:
        repert, ficname = os.path.split(fic)
        if not( ('.svn' in repert) or ('unused' in repert) or \
                '.before_update_to_' in ficname):
            if ficname.startswith('Par_file'):
                if not (ficname.endswith('~')):
                    print 'Analysis of file : '+fic
                    Ct_Par_file+=1
                    Data = OuvreParFile(fic)
                    ProcessParfile_r19201(fic)
                    ProcessParfile_r19340(fic)
                    ProcessParfile_r19346(fic)
                    ProcessParfile_r19521(fic)
                    ProcessParfile_r19804(fic)
                    ProcessParfile_r20307(fic)
                print '~'*80
    #                
    print 'Number of Par_file analysed : ', Ct_Par_file   
    print 'END OF Par_file PROCESSING'
    
