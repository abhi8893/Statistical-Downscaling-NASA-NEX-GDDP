f <- '/home/abhi/Documents/mygit/NEX-Analysis/pickles/Amravati/Amravati_ALL21_allscens_df.csv'
df <- read.csv(f)

df %>% 
  group_by(year, seas) %>% 
  summarise(value=mean(value))


df_ymean <- 
  df %>% 
  group_by(model, variable, year, seas, scen, tslice) %>% 
  summarise(value=mean(value, na.rm=T)) %>%
  ungroup() %>% 
  full_join(df %>% group_by(model, variable, year, scen, tslice) %>% 
              summarise(value=mean(value, na.rm=T)) %>% mutate(seas='Annual')) %>% 
  mutate(seas=as.factor(seas)) %>% 
  arrange(model, variable, seas, year, scen) %>% 
  ungroup()

df_ymean <-
  df_ymean %>% 
  full_join(df_ymean %>% 
              group_by(variable, year, seas, scen, tslice) %>%
              summarise(value=mean(value, na.rm=T)) %>% 
              mutate(model='EnsMean_ALL21')) %>%
  mutate(model=as.factor(model)) %>% 
  ungroup()


library(ggplot2)

df_ymean_ensmean <- 
  df_ymean %>%
  filter((seas == 'Annual')&
         (variable == 'tasmax')&
         (scen %in% c('historical', 'rcp45'))) %>%
  filter((model == 'EnsMean_ALL21'))

df_ymean_ensmean <- 
  df_ymean %>%
  filter((seas == 'Annual')&
           (variable == 'tasmax')&
           (scen %in% c('historical', 'rcp45'))) %>%
  filter((model == 'EnsMean_ALL21'))

df_anomaly %>%
  filter((seas == 'Annual')&
         (variable == 'tasmax')&
         (scen %in% c('historical', 'rcp45'))) %>% 
  filter((model != 'EnsMean_ALL21')) %>% 
  ggplot(aes(year, delta, group=model), color='black')+
  geom_line(alpha=0.1)+
  geom_line(data = df_ymean_ensmean,
         aes(year, value))
  
  

df_anomaly %>% 
  mutate(diff=value-delta) %>% 
  group_by(modeltslice)


df_anomaly <- 
  df_ymean %>% 
  group_by(model, variable, seas) %>% 
  mutate(delta = value - mean(value[tslice == 'baseline']))



df_base_mean <- 
  df_ymean %>% 
  filter(tslice == 'baseline') %>% 
  group_by(model, variable, seas, scen, tslice) %>% 
  summarise(value=mean(value))



df_anomaly %>% 
  group_by(model, variable, seas, scen, tslice) %>% 
  summarise(delta=mean(delta))
