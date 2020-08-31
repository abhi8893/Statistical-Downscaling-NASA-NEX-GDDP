imd_file <- '/home/abhi/Documents/mygit/NEX-Analysis/pickles/Amravati/IMD/Amravati_allvars_seas_ymean_1976-2016.csv'
df_imd <- 
  read.csv(imd_file) %>% 
  as_tibble()

df_imd_anomaly <- 
  df_imd %>% 
  group_by(variable, seas) %>% 
  mutate(delta= value - mean(value[tslice == 'baseline'], na.rm=T))

df_imd_anomaly %>% 
  filter(
    (variable == 'tasmax')&
    (seas == 'Annual')
    ) %>% 
  ggplot(aes(year, delta))+
  geom_line()

p <- make_ensemble_lineplot('tasmin', 'Annual')
p+
  geom_line(data=df_imd_anomaly %>% filter(
                (variable == 'tasmin')&
                  (seas == 'Annual')),
            aes(year, delta))

for(seas_name in seas_names){
  for(var_name in c('tasmin', 'tasmax', 'tas')){
    
    p <- make_ensemble_lineplot(var_name, seas_name)+
    geom_line(data=df_imd_anomaly %>% filter(
      (variable == var_name)&
        (seas == seas_name)),
      aes(year, delta))
    outfile <- paste0('/home/abhi/Documents/mygit/NEX-Analysis/plots/Amravati/',
                      var_name, '_', seas_name, '_with_IMD', '.png')
    ggsave(outfile, p, width = 12, height = 10)
    
  }
}
