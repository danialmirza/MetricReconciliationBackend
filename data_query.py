met = {"_id":{"$oid":"6075a6c519cd6a4b0cc7966f"},"reporter":"dmirza509","metricName":"test_metric","source":"NSD","database":"MELD","schema":"test_schema","table":"test_table","metricId":"2","metricCol":"test_col","exclusions":{"excl_bulk":True,"excl_resi":True,"excl_courtesy":False},"geos":{"ned":True,"cen":False,"wes":False},"divisionCol":"division","regionCol":"","topGeoAgg":"NED","timeCol":"time_col","timeDensity":"M","dateRange":{"start_date":"2021-01-01T05:00:00.000Z","end_date":"2021-04-30T04:00:00.000Z"}}

def find_geography_options(met1, met2):
    #set local variables for division columns
    if met1['divisionCol'] == '':
        div1 = None
    else:
        div1 = met1['divisionCol']

    if met2['divisionCol'] == '':
        div2 = None
    else:
        div2= met2['divisionCol']

    #set local variables for region columns
    if met1['regionCol'] == '':
        reg1 = None
    else:
        reg1 = met1['regionCol']

    if met2['regionCol'] == '':
        reg2 = None
    else:
        reg2 = met2['regionCol']

    #need to create logic here for getting appropriate geographies
    if div1 and div2:
        west = True
        cen = True
        ned = True
        divcuts = True
    if reg1 and reg2:
        regcuts = True

    if met1['topGeoAgg'] == met2['topGeoAg']: # both are the same, so top geography is the same
        top_geo = met1['topGeoAgg']
    elif met1['topGeoAgg'] == 'ENT': #metric 1 is enteprise, metric 2 is division - overlap on that division
        top_geo = met2['topGeoAgg']
    elif met2['topGeoAgg'] == 'ENT': #metric 2 is enterprise, metric 1 is division - overlap on that division
        top_geo = met1['topGeoAgg']
    else:  #no overlap
        top_geo = 'NO OVERLAP'



def pull_data(met, division,):

    query = """ SELECT {metricCol}
                    , {denominatorCol}
                    , {numeratorCol}
                FROM {database}.{schema}.{table}
                WHERE {metricCol} = '{metricID}'"""

    return query