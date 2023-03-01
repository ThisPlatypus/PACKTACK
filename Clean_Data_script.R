library(readr)

library(dplyr)

library(tidyr)

Data_Set= c('CTU-IoT-Malware-Capture-44-1','CTU-IoT-Malware-Capture-52-1','CTU-IoT-Malware-Capture-20-1','CTU-IoT-Malware-Capture-21-1','CTU-IoT-Malware-Capture-42-1','CTU-IoT-Malware-Capture-60-1','CTU-IoT-Malware-Capture-17-1','CTU-IoT-Malware-Capture-36-1','CTU-IoT-Malware-Capture-33-1','CTU-IoT-Malware-Capture-8-1','CTU-IoT-Malware-Capture-35-1','CTU-IoT-Malware-Capture-48-1','CTU-IoT-Malware-Capture-39-1','CTU-IoT-Malware-Capture-7-1','CTU-IoT-Malware-Capture-9-1','CTU-IoT-Malware-Capture-3-1','CTU-IoT-Malware-Capture-1-1', 'CTU-IoT-Malware-Capture-34-1','CTU-IoT-Malware-Capture-43-1', 'CTU-IoT-Malware-Capture-44-1','CTU-IoT-Malware-Capture-49-1')

for (i in 1:length(Data_Set)) {
  CleanData(Data_Set[i])
}



CleanData <-  function(name_file){
 
  
  TEMP <- read_delim(paste(paste("C:/Users/chiar/PycharmProjects/PACKTACK/Data/",name_file, sep=""),".txt",sep=""), 
                     delim = "\t", escape_backslash = TRUE, 
                     escape_double = FALSE, col_names = FALSE,  col_types = cols(X9 = col_number(), X1= col_character() ), 
                     comment = "#", trim_ws = TRUE, skip = 6)
  
  return(print(paste("\n Load il file: ",name_file, sep="") ))
  
  TEMP <- TEMP %>% separate(X21, c('css','lABEL', 'DETAIL.LABE'), sep="   ")
  
  return(print(paste("\n New variable done in: ",name_file, sep="") ))
  
  colnames(TEMP) <- c("ts","uid" ,"id.orig_h","id.orig_p","id.resp_h","id.resp_p" , "proto" ,"service" ,
                      "duration","orig_bytes","resp_bytes","conn_state" ,"local_orig","local_resp","missed_bytes",
                      "history","orig_pkts","orig_ip_bytes" ,"resp_pkts","resp_ip_bytes","tunnel_parents" ,"label", 
                      "detailed.label")
  
  return(print(paste("\n Start to save: ",name_file, sep="") ))
  
  write.table(TEMP, file = paste(paste("C:/Users/chiar/PycharmProjects/PACKTACK/Data/CleanData/",name_file, sep=""),".txt",sep="")
              , sep = "\t",
              row.names = FALSE)
  
  return(print(paste("\n Saved: ",name_file, sep="") ))
}
  
 