df %>% 
  filter(value == 90)

df_pr <- read.csv('/home/abhi/Documents/mygit/NEX-Analysis/pickles/Amravati/Indices/metric_df_precipitation.csv')
df_pr <- as_tibble(df_pr)

df_tas <- read.csv('/home/abhi/Documents/mygit/NEX-Analysis/pickles/Amravati/Indices/metric_df_temperature.csv')
df_tas <- as_tibble(df_tas)

df <- full_join(df_pr, df_tas) %>% 
  mutate(metric=as.factor(metric),
         variable=as.factor(variable))

my.t.test <-  function(...){
  res <- out <- tryCatch(
    {
      t.test(...)
    },
    error=function(cond) {
      return(NA)
    }
  )
  
}

ttest_res %>% 
  filter(seas == 'Annual') %>% 
  print(n = 100)
  filter(metric == 'max_3_day_tas_mean')

  

ttest_res %>% 
  gather(seas
