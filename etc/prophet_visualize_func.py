PRED_DAYS = 7

def get_model_forecast(info):
    ds = ast.literal_eval(info['train_ds']) 
    y = ast.literal_eval(info['train_y']) 
    avg_prc = ast.literal_eval(info['train_avg_prc']) 
    test_y = ast.literal_eval(info['test_y'])
    test_avg_prc = ast.literal_eval(info['test_avg_prc'])
    dic = {
        'ds' : ds,
        'y' : y,
        'avg_prc' : avg_prc
    }
    data = pd.DataFrame(dic)
    holidays = pd.read_json(info['holidays'])
    
    ## feature engineering
#     if data['avg_prc'].max() > 0:
#         data['avg_prc'] = data['avg_prc'] / data['avg_prc'].max() * 100
#     else:
#         data['avg_prc'] = data['avg_prc'] / (data['avg_prc'].max() + 1) * 100
    data['cap'] = 100.0
    data['floor'] = 0.0
    
    ## run prophet
    model = Prophet(
        growth='logistic',
        holidays = holidays
    )
    model.add_country_holidays(country_name='KR')
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    if data['avg_prc'].isna().sum() == 0:
        model.add_regressor('avg_prc')
    model.fit(data)
    
    ## get estimation
    future = model.make_future_dataframe(periods=PRED_DAYS)
    if data['avg_prc'].isna().sum() == 0:
        future['avg_prc'] = pd.concat([pd.Series(avg_prc), pd.Series(test_avg_prc)], ignore_index=True)
    future['cap'] = 100
    future['floor'] = 0.0
    
    forecast = model.predict(future)
    
    return model, forecast

def prophet_plot(m, fcst, y):
    fig = plt.figure(facecolor='w', figsize=(12, 5))
    ax = fig.add_subplot(111)
    fcst_t = fcst['ds'].dt.to_pydatetime()
    ds_t = m.history['ds'].dt.to_pydatetime()
    
    ax.plot(m.history['ds'].dt.to_pydatetime(), np.square(m.history['y']), 'k.', label='observed data points')
    ax.plot(fcst_t, np.square(fcst['yhat']), ls='-', c='#0072B2', label='Forecast')
    #ax.plot(fcst_t, np.square(p.forecast['cap']), ls='--', c='k', label='Maximum capacity')
    ax.plot(fcst_t, np.square(fcst['floor']), ls='--', c='k', label='Minimum capacity')
    ax.fill_between(fcst_t, np.square(fcst['yhat_lower']), np.square(fcst['yhat_upper']),
                            color='#0072B2', alpha=0.2, label='Uncertainty interval')
    ax.set_ylabel('sales')
    
    trend = fcst['trend']
    ax.plot(fcst_t, trend, c='r')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('scaled_price')
    plt.plot(m.history['ds'].dt.to_pydatetime(), m.history['avg_prc'], color='deeppink', label='price')
    plt.legend()
    plt.show()
    
    test_ds = fcst['ds'].astype(str)[-7:]
    test_y = np.square(y[-7:])
    test_yhat = np.square(fcst['yhat'][-7:])
    
    tmp = pd.DataFrame({'ds' : test_ds, 'y' : test_y, 'yhat' : test_yhat})
    print(tmp.tail(7).T)