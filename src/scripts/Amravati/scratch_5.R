a


df_tas <- 
  df %>% 
  filter(variable %in% c('tasmax', 'tasmin')) %>% 
  group_by(model, scen, yday, month, year, seas, tslice) %>% 
  summarise(value=mean(value, na.rm=T),
         variable = 'tas')

df <- 
  df %>% 
  full_join(df_tas) %>% 
  mutate(variable=as.factor(variable))

df_ensmean <- 
  df %>% 
  group_by(variable, scen, yday, month, year, seas, tslice) %>% 
  summarize(value=mean(value, na.rm=T),
         model='EnsMean_ALL21')


df <- 
  df %>% 
  full_join(df_ensmean) %>% 
  mutate(model=as.factor(model))

df <- 
  df %>% 
  group_by(model, variable, yday) %>% 
  mutate(delta = value - mean(value[tslice == 'baseline'], na.rm=T))
  
df_monmean <- 
  df %>% 
  group_by(model, variable, year, month, seas, scen, tslice) %>% 
  summarise(value=mean(value, na.rm=T)) %>%
  ungroup() %>%
  group_by(model, variable, month, seas) %>% 
  mutate(delta=value - mean(value[tslice == 'baseline']))
# 
df %>% 
  filter(tslice %in% c('near')) %>%
  filter(model == 'EnsMean_ALL21') %>% 
  filter(
    (variable == 'tasmax')&
    (seas == 'ON')) %>% 
  ggplot(aes(delta, color=scen, fill=scen))+
  geom_histogram(aes(y=..density..), alpha=0.1, 
                 position='identity',
                 bins=50)+
  scale_color_manual(values = c('blue', 'red'))+
  scale_fill_manual(values = c('blue', 'red'))
  
