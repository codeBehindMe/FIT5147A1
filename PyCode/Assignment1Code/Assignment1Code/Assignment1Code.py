################################
##                            ##
## Assignment 1               ##
##                            ##
################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re



def __getSex(x):
        _lst = x.split('_')
        _sex = _lst[len(_lst)-1]

        return _sex

def __getAge(x):
    
    _lst = [int(s) for s in x.split('_') if s.isdigit()]

    return '-'.join(str(z) for z in _lst)



def splitAgeParam(x):

    _lst = x.split('-')

    _res = segmentAge(max(_lst))
    

    return _res


def segmentAge(x):
    if '-' in x:
        return splitAgeParam(x)
    elif int(x) >=0 and int(x) <10:
        return "0-9"
    elif int(x) >=10 and int(x) <20:
        return "10-19"
    elif int(x) >= 20 and int(x) < 30:
        return "20-29"
    elif int(x) >= 30 and int(x) < 40:
        return "30-39"
    elif int(x) >= 40 and int(x) < 50:
        return "40-49"
    elif int(x) >= 50 and int(x) < 60:
        return "50-59"
    elif int(x) >= 60 and int(x) < 70:
        return "60-69"
    elif int(x) >= 70 and int(x) < 80:
        return "70-79"
    elif int(x) >= 80 and int(x) < 90:
        return "80-89"
    elif int(x) >=90:
        return "90+"


# Read in the meta data
geo_loc = pd.read_excel("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\Metadata\\2011Census_geog_desc_1st_and_2nd_release.xlsx")
geo_loc.shape
geo_loc.head()

# Read in the person data
pop_data = pd.read_csv("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\2011 Census BCP Postal Areas for VIC\\VIC\\2011Census_B01_VIC_POA_short.csv")
pop_data.shape
pop_data.head()

# Drop unncessary axis, just keep the major population statistics.
pop_data = pop_data.ix[:,:4]

# Quick plot to see whats going on.
sb.jointplot(pop_data['Tot_P_M'],pop_data['Tot_P_F'],kind='scatter')
plt.show()

# Drop duplicate indexes from the geographic locations file. Duplicates are for unknown areas.
geo_loc.drop_duplicates(["Code"],inplace=True)

# Set indexes for joins
geo_loc.set_index("Code",False,False,True,True)
pop_data.set_index("region_id",False,False,True,True)

# Do the join
_fdf = pd.concat([geo_loc,pop_data],axis=1,join='inner')

# Assert left join to pop_data did not drop obs. Check head / tail to see key match accuracy.
assert _fdf.shape[0] == pop_data.shape[0]
_fdf.head()
_fdf.tail()

# Drop unecessary columns
_fdf.drop(['Level','Label','region_id'],1,inplace=True)
assert _fdf.shape[1] < (geo_loc.shape[1] + pop_data.shape[1])
assert _fdf.shape[0] == pop_data.shape[0]

# Release memory. (Optional)
geo_loc = None
pop_data = None


# Bring in housing data
_hsing = pd.read_csv("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\2011 Census BCP Postal Areas for VIC\\VIC\\2011Census_B32_VIC_POA_short.csv")

_hsing.head()
_hsing.shape
_hsing.set_index("region_id",False,False,True,True)
# Only keep the total columns and filter out the others.
_hsing = _hsing[['O_OR_Total','O_MTG_Total','R_Tot_Total']]
_hsing.head()



# Combine the mortgage owned and the outright owned to make a total owned
_hsing['O_Tot_Total'] = _hsing['O_OR_Total'] + _hsing['O_MTG_Total']

assert sum(_hsing['O_Tot_Total']) == sum(_hsing['O_OR_Total'] + _hsing['O_MTG_Total'])
_hsing.head()

# Drop the extra columns
_hsing.drop(['O_OR_Total','O_MTG_Total'],axis=1,inplace=True)

# Merge the dataframes with our main dataframe.
assert _fdf.shape[0] == _hsing.shape[0]
_fdf = pd.concat([_fdf,_hsing],axis = 1, join = 'inner' )
assert _fdf.shape[0] == _hsing.shape[0]

_fdf.head()

# See what the distribution area looks like to peeps
sb.jointplot(_fdf['Area sqkm'],_fdf['Tot_P_P'],kind ='scatter')
plt.show()
# See what houses look like
sb.jointplot(_fdf['Area sqkm'],_fdf['R_Tot_Total']+_fdf['O_Tot_Total'],kind='scatter')
plt.show()

# Eh both look like no real correlation. Makes sense, since there are 3 distinct housing densities and no idea of what those distributions are.

# Bring in the age data
age_dta = pd.read_csv("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\2011 Census BCP Postal Areas for VIC\\VIC\\2011Census_B04A_VIC_POA_short.csv")
age_dtb = pd.read_csv("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\2011 Census BCP Postal Areas for VIC\\VIC\\2011Census_B04B_VIC_POA_short.csv")

age_dta.set_index('region_id',inplace=True)
age_dtb.set_index('region_id',inplace=True)

assert age_dta.shape[0] == age_dtb.shape[0]
age_dt = pd.concat([age_dta,age_dtb],axis=1,join='inner')
assert age_dt.shape[0] == age_dta.shape[0] == age_dtb.shape[0]

# Melt
age_dt_melt = age_dt.reset_index(level=0)
age_dt_melt = pd.melt(age_dt_melt,id_vars=['region_id'])
# Drop non sex based
filter = age_dt_melt['variable'].str.contains('_(M|F)')
age_dt_melt = age_dt_melt[filter]

age_dt_melt['variable'].unique()

# Drop totals
filter = age_dt_melt['variable'].str.contains('Tot_')
age_dt_melt = age_dt_melt[~filter]

age_dt_melt['variable'].unique()

# Get sex column
age_dt_melt['sex'] = age_dt_melt['variable'].apply(lambda x: __getSex(x))
# Get age column
age_dt_melt['age'] = age_dt_melt['variable'].apply(lambda x: __getAge(x))

# Drop variable column
age_dt_melt.drop(['variable'],axis=1,inplace=True)


age_dt_melt['ageSegment'] = age_dt_melt['age'].apply(lambda x:segmentAge(x))

# Group object
groupObj = age_dt_melt.groupby(['region_id','sex','ageSegment'])

# Get results
sumGroup = groupObj.sum().unstack().unstack()

# adjust multi index
_idx = pd.Index([e[1] + e[2] for e in sumGroup.columns.tolist()])

sumGroup.columns = _idx

# Bind to full frame.
assert _fdf.shape[0] == sumGroup.shape[0]
_fullWithAge = pd.concat([_fdf,sumGroup],axis=1,join='inner')
assert _fullWithAge.shape[1] == _fdf.shape[1] + sumGroup.shape[1]

# Bring in the median household income data.
med_house_inc = pd.read_csv("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\2011 Census BCP Postal Areas for VIC\\VIC\\2011Census_B02_VIC_POA_short.csv")

# Subset
med_house_inc = med_house_inc[['region_id','Median_Tot_fam_inc_weekly']]

med_house_inc.set_index('region_id',inplace=True)

assert _fullWithAge.shape[0] == med_house_inc.shape[0]
_fdf = pd.concat([_fullWithAge,med_house_inc],axis=1,join='inner')
assert _fdf.shape[1] == _fullWithAge.shape[1] + med_house_inc.shape[1]

# Bring in some educational information
edu_inf = pd.read_csv("C:\\Users\\aaron\\Downloads\\FIT5147A1\\2011_BCP_POA_for_Vic_short-header\\2011 Census BCP Postal Areas for VIC\\VIC\\2011Census_B37_VIC_POA_short.csv")

# Extract columns with education information
edu_inf = edu_inf[['region_id','Non_sch_quals_PostGrad_Dgre_M','Non_sch_quals_PostGrad_Dgre_F','Non_sch_quals_Gr_Dip_Gr_Crt_M','Non_sch_quals_Gr_Dip_Gr_Crt_F','Non_sch_quals_Bchelr_Degree_M','Non_sch_quals_Bchelr_Degree_F','Non_sch_quls_Advncd_Dip_Dip_M','Non_sch_quls_Advncd_Dip_Dip_F','Non_school_quals_Cert_Level_M','Non_school_quals_Cert_Level_F']]

edu_inf.set_index('region_id',inplace=True)

# Join to full
assert edu_inf.shape[0] == _fdf.shape[0]
_fullWithDets = pd.concat([_fdf,edu_inf],axis=1,join='inner')
assert _fullWithDets.shape[1] == edu_inf.shape[1] + _fdf.shape[1]



# Make postcode
_full = _fullWithDets.copy()
_full['Code'] = _full['Code'].apply(lambda x : int(x[3:]))


# Read in some crime data
_crime = pd.read_csv("C:\\Users\\aaron\\OneDrive\\Documents\\Monash Data Science\\Data Visualisation\\A1\\CrimeBySuburb.csv")

# Shrink Crime type
_crime['TYPE'] = _crime['TYPE'].apply(lambda x: x[0])

# Filter A/B {A:Against Person, B:Against Property}

ab_crime = _crime.loc[_crime['TYPE'].isin(['A','B'])]

# Drop city
ab_crime = ab_crime.drop('CITY',axis=1)

# Group by postcode and type

crime_group = ab_crime.groupby(['POSTCODE','TYPE'])

crime_by_code = crime_group.sum().unstack()

# Set index
_idxCrime = pd.Index(e[1] for e in crime_by_code.columns.tolist())

crime_by_code.columns = _idxCrime

# join with our cencus data.
_idx_full = pd.Index(_full['Code'])
_idx_full.name = 'CODE'
_full.index = _idx_full

full_with_crime = pd.concat([_full,crime_by_code],axis=1,join='inner',join_axes= [_full.index])
assert full_with_crime.shape[1] == _full.shape[1] + crime_by_code.shape[1]

full_with_crime.to_csv("C:\\Users\\aaron\\OneDrive\\Documents\\Monash Data Science\\Data Visualisation\\A1\\census2011_with_crime.csv",index=False)