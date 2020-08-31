df_anomaly_trend %>% 
  filter(
    (model == 'EnsMean_ALL21')&
    (tslice %in% c('baseline', 'near', 'far'))&
    (term == 'year')
    ) %>% 
  select(-statistic) %>% 
  write.csv('/home/abhi/Documents/mygit/NEX-Analysis/pickles/Amravati/anomaly_trend/EnsMean_ALL21_anomaly_trend.csv',
            row.names=FALSE)
