def preprocess( df,prov='Córdoba',
                curr='USD',
                IQR=5,
                ):
    df = df[df['l2']==prov]
    df = df[df['currency']==curr]
    df = df[df['operation_type']=='Venta']
    colstodrop=['lat','lon','l1','l2','start_date','end_date','id',
                'ad_type','description','title','property_type','operation_type',
                'price_period','l3','l4','l5','l6','created_on']
    df = df.drop(columns=colstodrop)
    df.dropna(inplace=True)
    df2 = drop_outliers(df,['surface_covered','surface_total','price'],IQR=IQR)
    X = df2[['surface_covered']]
    if 'price' in df2.columns:
        y = df2['price']
    else:
        y= None
    return X,y


def drop_outliers(df,listacols,IQR):
    for col in listacols:
        IQRVAL = df[col].quantile(0.75)-df[col].quantile(0.25)
        IQRVAL = IQRVAL * IQR
        df = df.loc[df[col]<IQRVAL]
    return df
