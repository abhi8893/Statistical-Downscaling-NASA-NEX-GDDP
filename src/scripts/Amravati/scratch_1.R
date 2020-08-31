scen_name <- 'rcp45'
tslice_name <- 'far'

ttest_res <- 
  df %>% 
  filter((scen %in% c(scen_name, 'historical')) & 
           (tslice %in% c(tslice_name, 'baseline'))) %>% 
  group_by(metric, seas, variable) %>% 
  do(tidy(my.t.test(value~scen, data=.))) %>%
  mutate(estimate=-estimate,
         conf.low2=-conf.high,
         conf.high=-conf.low,
         scen=scen_name,
         tslice=tslice_name) %>%
  select(-conf.low) %>% 
  rename(conf.low=conf.low2) %>% 
  select(metric, seas, variable, scen, tslice, 
         estimate, conf.low, conf.high, p.value)

make_ttest_df <- function(scen_name, tslice_name){
  ttest_res <- 
    df %>% 
    filter((scen %in% c(scen_name, 'historical')) & 
             (tslice %in% c(tslice_name, 'baseline'))) %>% 
    group_by(metric, seas, variable) %>% 
    do(tidy(my.t.test(value~scen, data=.))) %>%
    mutate(estimate=-estimate,
           conf.low2=-conf.high,
           conf.high=-conf.low,
           scen=scen_name,
           tslice=tslice_name) %>%
    select(-conf.low) %>% 
    rename(conf.low=conf.low2) %>% 
    select(metric, seas, variable, scen, tslice, 
           estimate, conf.low, conf.high, p.value)
  
  return(ttest_res)
}

ttest_res <- 
  make_ttest_df('rcp45', 'near') %>% 
  make_ttest_df('rcp45', 'far') %>% 
  make_ttest_df('rcp85', 'near') %>% 
  make_ttest_df('rcp85', 'far') %>% 
  mutate(scen=as.factor(scen),
         tslice=as.factor(tslice))


ttest_dfs <- list(
  df1 = make_ttest_df('rcp45', 'near'),
  df2 = make_ttest_df('rcp45', 'far'),
  df3 = make_ttest_df('rcp85', 'near'),
  df4 = make_ttest_df('rcp85', 'far')
  
)

ttest_df <- Reduce(full_join, ttest_dfs)
  
  


df %>% 
  filter(metric == 'max_5_day_pr_amt', scen == 'rcp45', seas == 'Annual') %>%
  ggplot(aes(year, value))+
  geom_line()+
  geom_smooth(method = 'lm')


v.fut <- 
  df %>% 
  filter(metric == 'max_5_day_pr_amt', scen == 'rcp45', seas == 'Annual') %>% 
  .$value

v.base <- 
  df %>% 
  filter(metric == 'max_5_day_pr_amt', scen == 'historical', seas == 'Annual') %>% 
  .$value

return.level(fevd(v.fut, units = 'mm/5day'))
return.level(fevd(v.base, units = 'mm/5day'))


  

ttest_res %>% 
  filter(metric == 'days_above_1mm')
