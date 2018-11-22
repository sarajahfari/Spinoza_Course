# generate bfsl files for design

#base="/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/"
#datadir="/Users/sarajahfari/Aeneas_shared/2018/visual/fMRIcourse/bids_data/3T/sub-001/func"
#outputdir=c('FSL','3T','Firstlevel',"sub-001","events")

make_fslevents=function(base,datadir,outputdir)
{
  setwd(datadir)
  events=read.table(list.files()[grep('.tsv',list.files())],h=T)

  EVs=as.character(unique(events$trial_type))
  
  # 
  # paste('timing_',(EVs[1]),sep='')=events[events$trial_type==EVs[1],c('onset','duration','weight')]
  # write.table()
  
  # make a loop to create path you want
  setwd(base)
  for (f in outputdir)
  {
    wd=getwd()
    dir.create(f,overwrite=T)
    setwd(paste(wd,'/',f,'/',sep=''))
  }
  
  # make event files for FSL
  for (i in EVs)
  {  
    write.table(events[events$trial_type==(i),c('onset','duration','weight')],
                file=paste('timing_',(i),'.bfsl',sep=''),
                sep='\t',row.names=F,quote=FALSE,col.names=F)
  }
}  