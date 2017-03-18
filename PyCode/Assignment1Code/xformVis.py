# Just do some transforms for kicks.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import math
import re

_dt = pd.read_csv("C:\\Users\\tillera\\Documents\\FIT5147\\FIT5147A1\\census2011_with_crime.csv")

sb.jointplot(_dt['A'], _dt['B'], kind='scatter')

_dtSub = _dt[['Code', 'A', 'B']]

_dtSubMelt = pd.melt(_dtSub, ['Code'], ['A', 'B'])

_dtSubMelt.columns = ['POSTCODE', 'CRIMETYPE', 'CRIMES']


def crimeType(x):
    if x == 'A':
        return 'Personal'
    elif x == 'B':
        return 'Property'
    else:
        return None


_dtSubMelt['CRIMETYPE'] = _dtSubMelt['CRIMETYPE'].apply(lambda x: crimeType(x))

_dtSubMelt.to_csv("C:\\Users\\tillera\\Documents\\FIT5147\\FIT5147A1\\crimePCodeMelt.csv", index=False)

_dtAges = _dt[
    ['Code', '0-9F', '0-9M', '10-19F', '10-19M', '20-29F', '20-29M', '30-39F', '30-39M', '40-49F', '40-49M', '50-59F',
     '50-59M', '60-69F', '60-69M', '70-79F', '70-79M', '80-89F', '80-89M', '90+F', '90+M', 'A', 'B'
     ]]


def xFormMax(dataFrame):
    df = dataFrame.copy()

    ss = df.ix[:, 1:21]

    for i, r in ss.iterrows():
        df.set_value(i, 'MAXAGEFREQ', r.idxmax(axis=1))

    return df


_dtAges = xFormMax(_dtAges)

_dtAges = _dtAges[['Code', 'A', 'B', 'MAXAGEFREQ']]

_dtAges = pd.melt(_dtAges, ['Code', 'MAXAGEFREQ'], ['A', 'B'])

_dtAges.columns = ['POSTCODE', 'FREQUENTAGE', 'CRIMETYPE', 'CRIMES']

_dtAges['CRIMETYPE'] = _dtAges['CRIMETYPE'].apply(lambda x: crimeType(x))

_dtAges.to_csv("C:\\Users\\tillera\\Documents\\FIT5147\\FIT5147A1\\crimeWithAge.csv", index=False)

_dtEdu = _dt.copy()

_dtEdu = _dtEdu[['Code','Non_sch_quals_PostGrad_Dgre_M', 'Non_sch_quals_PostGrad_Dgre_F', 'Non_sch_quals_Gr_Dip_Gr_Crt_M', 'Non_sch_quals_Gr_Dip_Gr_Crt_F', 'Non_sch_quals_Bchelr_Degree_M', 'Non_sch_quals_Bchelr_Degree_F', 'Non_sch_quls_Advncd_Dip_Dip_M', 'Non_sch_quls_Advncd_Dip_Dip_F', 'Non_school_quals_Cert_Level_M', 'Non_school_quals_Cert_Level_F']]

_dtEdu = pd.melt(_dtEdu,['Code'])


_dtEdu.to_csv("C:\\Users\\tillera\\Documents\\FIT5147\\FIT5147A1\\eduCrime.csv", index=False)

_dtcst = _dt.copy()

_dtcst = _dtcst[['Code', 'A', 'B']]

for i, r in _dtcst.iterrows():
    if r['A'] > r['B']:
        _dtcst['PTYPE'] = 'A'
    else:
        _dtcst['PTYPE'] = 'B'

_dtcst['PTYPE'] = _dtcst['PTYPE'].apply(lambda x: crimeType(x))

_dtcst.to_csv("C:\\Users\\tillera\\Documents\\FIT5147\\FIT5147A1\\PrCrime.csv", index=False)
