require(ggplot2)
require(plotly)
dt_ <- read.csv("Australian_Post_Codes_Lat_Lon.csv")


vic_ <- dt_[dt_$state == "VIC",]


rnorm.between <- function(n, minimum = 0, maximum = 1)
{
  ## CREDIT :: https://gist.github.com/tomhopper/19f07fc96db8d149b24f
  
  x <- rnorm(n)
  max_x <- max(x)
  min_x <- min(x)
  x <- x - min_x
  x <- x / (max_x - min_x)
  x <- x * (maximum - minimum)
  x <- x + minimum
  
  return(x)
}

clipToNormBound <- function(x,bound=1000,clip = 0){
  if (x <= clip ){
    return(rnorm(1,bound,bound/25))
  } else {
    return(x)
  }
}

vic_[,"Population"] <- rnorm.between(nrow(vic_),10,41000)
vic_[,"Population"] <- sapply(vic_[,"Population"],ceiling)


vic_[,"Area"] <- rnorm(n = nrow(vic_),mean = 5,1)


vic_[,"PRent"] <- rnorm.between(nrow(vic_),4,95) # Percentage Renting

vic_[,"AgeMedian"] <- rnorm(n = nrow(vic_),mean = 30,10) # Median Age

vic_[,"AgeMedian"]<- sapply(vic_[,"AgeMedian"] ,clipToNormBound,bound = 3)


vic_[,"IncMedian"] <- rnorm.between(nrow(vic_),15323,73122) # Median Income

vic_[,"EduAvg"] <- rnorm.between(nrow(vic_),10,25) # Average years of education 


vic_[,"EduAvg"] <- sapply(vic_[,"EduAvg"],floor)


vic_[,"PRCrime"] <- rnorm.between(nrow(vic_),232,6439)  # Crimes against property.

vic_[,"PRCrime"] <- sapply(vic_[,"PRCrime"],ceiling)


vic_[,"PSCrime"] <- rnorm.between(nrow(vic_),164,8231)
vic_[,"PSCrime"] <- sapply(vic_[,"PSCrime"],floor)

# write.csv(vic_,"generated_Vic_suburb_data.csv")


