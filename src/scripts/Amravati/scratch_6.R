library(purrr)

df_pr %>%
  #na.omit() %>% 
  filter(
    (stringr::str_detect(metric, 'max_1_day_pr_amt'))&
    (seas == 'Annual')
    ) %>% 
  group_by(metric, scen)# %>%
  nest() %>% 
  mutate(bm=map(data, fevd))
  
