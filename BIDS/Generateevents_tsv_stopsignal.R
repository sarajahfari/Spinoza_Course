################
# generate events file for stopsignal task BIDS
# S. Jahfari 10-2018
################

rm(list=ls()) # empty dir

# open master loop, install packages
install.packages('MASS')
install.packages('plotrix')
install.packages('lattice')
install.packages('foreign')
install.packages('openxlsx')

# load libraries
library(MASS)
library(plotrix)
library(lattice)
library(foreign)
library(openxlsx)

#################################
#### setwd to run function from
#################################

# change this path to your directory 3T data
#datadir = "/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/raw_data/pilot/behavior"
# change this path to your directory 7Tdata
#datadir = "/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/raw_data/3T/behavior"
#outputdir="/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/bids_data/3T/sub-001/func"
#bidsname='sub-001'

Make_stopevents=function(datadir,bidsname,outputdir)	
{
  # go to file directory
  setwd(datadir)
  
  # list the files in file dir
  sdata = list.files()
  
  
  data = list.files()[grep('face',list.files())]
  
  if (length(data[grep('face2_st150.log',data)])==1)
  {ppn = gsub('-face2_st150.log','',data[1])} else
  {ppn = gsub('-face_st150.log','',data[1])}
  
  # read in the files of interest
  log1 = read.table(data[grep('.txt',data)],h=T)
  #PS1 = read.xlsx(data[grep('.xlsx',data)])
  PS1 = read.table(data[grep('*.log',data)],sep='\t',skip=3,strip.white=T,header=T,fill=T)
  
  
  #######################################################################
  ###### start preparing timing files ###################################
  #######################################################################
  
  ###### block 1 ###############
  
  Null1 = as.numeric(paste(PS1[1,'Time'])) # select timing of start scan
  
  dur_t1 = PS1[PS1$Event.Type=='Picture',]
  dur_t1 = dur_t1[2:(length(dur_t1[,1])-1),] # rem info and end slide
  dur_t1 = dur_t1[dur_t1$Code!= 'te laat',] # remove te laat slides
  
  # select stim (go,stop) trials and null trials
  dur_t1_stim = dur_t1[(dur_t1[,'Code']!= 'null'&dur_t1[,'Code']!= 'miss'),c('Time','Duration')]
  dur_t1_null = dur_t1[dur_t1[,'Code']=='null',c('Time','Duration')]
  
  dur_t1_stim[,'Time'] = as.numeric(paste(dur_t1_stim[,'Time'])) - Null1 # link timing with volume 1 t=0
  dur_t1_null[,'Time'] = as.numeric(paste(dur_t1_null[,'Time'])) - Null1 # link timing with volume 1 t=0
  
  as.numeric(paste(dur_t1_stim$Duration))->dur_t1_stim$Duration
  as.numeric(paste(dur_t1_null$Duration))->dur_t1_null$Duration
  
  # change time to sec
  dur_t1_stim = dur_t1_stim/10000
  dur_t1_null = dur_t1_null/10000
  
  # make timing matrix
  col3_stim = rep(1, length(dur_t1_stim[,1]))
  col3_null = rep(1, length(dur_t1_null[,1]))
  
  blog1_stim = cbind(log1[1:length(dur_t1_stim[,1]),-which(colnames(log1)=='Time')],dur_t1_stim,weight=col3_stim)
  blog1_null = cbind(dur_t1_null, col3_null)
  
  ################################################################
  ######## select events of interest #############################
  ################################################################
  
  ST_LOG= blog1_stim[,c('Time','Duration','weight','GoStop','RT','ResT','SSD1')]
  Trial_type=ifelse(ST_LOG[,'GoStop']==0,'Go','Stop')
  SSD=ifelse(ST_LOG[,'SSD1']==99,'n/a',ST_LOG[,'SSD1'])
  Response=c()
  
  for (t in 1:length(ST_LOG[,1]))
  {
    if (Trial_type[t]=='Go'){
      if (ST_LOG[t,'ResT']==2) Response[t]='omission' else
        if (ST_LOG[t,'ResT']==1) Response[t]='Incorrect' else
          if (ST_LOG[t,'ResT']==0) Response[t]='correct' } else
            if (Trial_type[t]=='Stop'){
              if (ST_LOG[t,'ResT']==2) Response[t]='succesful_stop' else
                Response[t]='Failed_stop'}
    
  }	
  
  TT=c()
  for (event in 1:length(Trial_type))
  {
    if(Trial_type[event]=='Go')
    { if(Response[event]=='correct') TT[event]='GoCorrect' else
      if(Response[event]=='Incorrect') TT[event]='ChoiceError' else
        if(Response[event]=='omission') TT[event]='Omission'} else
          
          if(Trial_type[event]=='Stop'){
            if(Response[event]=='succesful_stop') TT[event]='succesful_stop' else
              if(Response[event]=='Failed_stop') TT[event]='Failed_stop'} 
  }
  
  LOG=cbind(ST_LOG[,c('Time','Duration','weight','RT')], TT, SSD)
  colnames(LOG)=c('onset','duration','weight','RT','trial_type','SSD')
  LOG$RT=LOG$RT/1000 # transform RT column to seconds
  
  # create tsv file
  
  
  setwd(outputdir)
  
  write.table(LOG,paste(bidsname,'_task-StopSignal_run-1_events.tsv',sep=''),sep='\t',row.names=F,quote=FALSE)
  print('conversion to events done')
  
}


# datadir = "/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/raw_data/3T/behavior"
# outputdir="/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/bids_data/3T/sub-001/func"
# bidsname='sub-001'
# 
# Make_stopevents(datadir,bidsname,outputdir)
	
		