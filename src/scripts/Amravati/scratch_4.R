
df_anomaly_to_plot <- 
  df_anomaly %>%
  filter((seas == 'Annual')&
           (variable == 'tasmax')&
           (scen %in% c('rcp45', 'rcp85'))) %>% 
  filter((model != 'EnsMean_ALL21'))


scen_name <- 'rcp45'
scen_colors <- list(rcp45='blue', rcp85='red')

df_anomaly %>%
  filter((seas == 'Annual')&
           (variable == 'tasmax')&
           (scen  %in% c('historical', scen_name))) %>% 
  filter((model == 'EnsMean_ALL21')) %>% 
  ggplot(aes(year, delta, color=scen))+
  geom_line()+
  geom_line(data=df_anomaly_to_plot, 
            aes(year, delta, group=model, color=scen), 
            alpha=0.50)+
  scale_y_continuous(limits = c(-1, 6))

#%>% filter(scen == scen_name

levels_lst <- list()
cols <- list('seas', 'variable', 'model', 'scen', 'tslice')

for (col_name in cols){
  levels_lst[col_name] <- levels(df_anomaly[col_name])
}
seas_names <- levels(df_anomaly$seas)
variable_names <- levels(df_anomaly$variable)
model_names <- levels(df_anomaly$model)
scen_names <- levels(df_anomaly$scen)

get_df_anomaly <- function(seasons=seas_names, 
                           variables=variable_names, 
                           models=model_names, 
                           scens=scen_names){
  df_anomaly %>% 
    filter(
      (seas %in% seasons)&
      (variable %in% variables)&
      (model %in% models)&
      (scen %in% scens))
  
}

get_units <- function(var_name){
  if (var_name == 'pr'){
    units <- 'mm'
  }else if(var_name %in% c('tasmax', 'tasmin', 'tas')){
    units <- 'degC'
  }
  return(units)
}

get_trend_text <- function(var_name, seas_name,
                           scen_name, tslice_name,
                           model_name = 'EnsMean_ALL21',
                           trend_units='year'){
  est <- 
    df_anomaly_trend %>% 
    filter(
      (variable == var_name)&
      (seas == seas_name)&
      (tslice == tslice_name)&
      (scen == scen_name)&
      (model == model_name)&
      (term == 'year')
      ) %>% 
    .$estimate
  
  if(trend_units == 'year'){
    scale_factor <- 1
  }else if (trend_units == 'decade'){
    scale_factor <- 10
  }
  
  trend_text <- paste0(round(est*scale_factor, 3), 
                       ' ',
                      get_units(var_name), '/', trend_units
                      )
  
  return(trend_text)
  
}

var_names <- list(pr='Precipitation',
                  tasmax='Maximum Temperature',
                  tasmin='Minimum Temperature',
                  tas='Mean Temperature')

seas_name <- 'JJAS'
var_name <- 'tasmax'

make_ensemble_lineplot <- function(var_name, seas_name){
  

  p <- 
    ggplot()+
    geom_line(data=get_df_anomaly(seas_name, var_name, 
                                  "EnsMean_ALL21", c("historical", 
                                                     "rcp45")),
              aes(year, delta))+
    geom_line(data=get_df_anomaly(seas_name, var_name,
                                  "EnsMean_ALL21", c("historical",
                                                     "rcp85")),
              aes(year, delta))+
    geom_line(data=get_df_anomaly(seas_name, var_name,
                                  "EnsMean_ALL21"),
              aes(year, delta, color=scen))+
    scale_color_manual(values = c('green', 'blue', 'red'))+
    geom_ribbon(data=df_anomaly_error %>% filter(
                    (variable == var_name)&
                    (seas == seas_name)),
                aes(x=year, ymin=delta.lo, ymax=delta.up, fill=scen),
                alpha=0.2)+
    scale_fill_manual(values = c('green', 'blue', 'red'))+
    geom_rect(aes(xmin=1976, xmax=2005, ymin=-Inf, ymax=Inf), alpha=0.1)+
    geom_rect(aes(xmin=2021, xmax=2050, ymin=-Inf, ymax=Inf), alpha=0.1)+
    geom_rect(aes(xmin=2061, xmax=2090, ymin=-Inf, ymax=Inf), alpha=0.1)+
    scale_x_continuous(breaks = c(seq(1950, 2090, 10), 2099),
                       sec.axis = sec_axis(~ . * 1,
                                           breaks = c(1976, 2005,
                                                      2021, 2050,
                                                      2061, 2090)))+
    #TODO: Make adding of annotations DRY! (concise)
    annotate(geom='text',
             x=1990, y=8,
             label=paste('Trend:', 
                         get_trend_text(var_name,
                                        seas_name,
                                        'historical',
                                        'baseline')),
             color='darkolivegreen',
             size = 4)+
    annotate(geom='text',
             x=2035, y=8.5,
             label=paste('Trend:', 
                         get_trend_text(var_name,
                                        seas_name,
                                        'rcp45',
                                        'near')),
             color='blue',
             size = 4)+
    annotate(geom='text',
             x=2035, y=7.5,
             label=paste('Trend:', 
                         get_trend_text(var_name,
                                        seas_name,
                                        'rcp85',
                                        'near')),
             color='red',
             size = 4)+
    annotate(geom='text',
             x=2075, y=8.5,
             label=paste('Trend:', 
                         get_trend_text(var_name,
                                        seas_name,
                                        'rcp45',
                                        'far')),
             color='blue',
             size = 4)+
    annotate(geom='text',
             x=2075, y=7.5,
             label=paste('Trend:', 
                         get_trend_text(var_name,
                                        seas_name,
                                        'rcp85',
                                        'far')),
             color='red',
             size = 4)+
    annotate(geom='text',
             x=(1976+2005)/2,y=10,
             label='atop(bold("baseline"))',
             size=10,
             parse=T)+
    annotate(geom='text',
             x=(2021+2050)/2,y=10,
             label='atop(bold("near"))',
             size=10,
             parse=T)+
    annotate(geom='text',
             x=(2061+2090)/2,y=10,
             label='atop(bold("far"))',
             size=10,
             parse=T)+
    xlab('')+
    ylab('anomaly')+
      ggtitle(paste0(var_names[[var_name]], ':', ' ', seas_name))+
      theme(plot.title = element_text(size=20, face = 'bold', 
                                    hjust = 0.5,
                                    vjust = 2))+
      scale_y_continuous(breaks=c(-2, 0, 1, 1.5, 2, 4, 6, 8), limits=c(-4, 10))
  
  return(p)
}
for(seas_name in seas_names){
  for(var_name in c('tas')){
    
    p <- make_ensemble_lineplot(var_name, seas_name)
    outfile <- paste0('/home/abhi/Documents/mygit/NEX-Analysis/plots/Amravati/',
                      var_name, '_', seas_name, '.png')
    ggsave(outfile, p, width = 12, height = 10)
    
  }
}



df_anomaly_error <- 
  df_anomaly %>%
  filter(model != 'EnsMean_ALL21') %>% 
  group_by(variable, year, seas, scen, tslice) %>% 
  summarise(
    value.lo = min(value, na.rm = T),
    value.up = max(value, na.rm = T),
    delta.lo = min(delta, na.rm = T),
    delta.up = max(delta, na.rm = T),
    value = mean(value, na.rm=T),
    delta = mean(delta, na.rm=T)
  )

df_anomaly_trend <- 
  df_anomaly %>% 
  group_by(model, variable, seas, scen, tslice) %>% 
  do(tidy(lm(delta~year, data=.)))


