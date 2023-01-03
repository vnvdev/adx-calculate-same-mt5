import pandas as pd
#Note data have open, high, low, close column

df = pd.read_csv('exampledata.csv')

#Calculate EMA for ADX
def ExponentialMA(i, period, prev_value, values):
    if i == 0:
        return prev_value
    else:
        ema = (values[i] - prev_value) * 2 / (period + 1) + prev_value
        return ema

def calculate_adx(high, low, close, adx_period):
    # Initialize the PDI and NDI arrays with the same length as the input arrays
    pdi = [0] * len(high)
    ndi = [0] * len(high)
    
    # Initialize the ADX array with the same length as the input arrays
    adx = [0] * len(high)
    
    # Initialize the temporary buffer with the same length as the input arrays
    tmp_buffer = [0] * len(high)
    
    # Iterate through the data points
    for i in range(1, len(high)):
        # Get the high and low prices for the current and previous data points
        high_price = high[i]
        prev_high = high[i-1]
        low_price = low[i]
        prev_low = low[i-1]
        prev_close = close[i-1]
        
        # Calculate the positive and negative values for the current data point
        tmp_pos = high_price - prev_high
        tmp_neg = prev_low - low_price
        if tmp_pos < 0:
            tmp_pos = 0
        if tmp_neg < 0:
            tmp_neg = 0
        if tmp_pos > tmp_neg:
            tmp_neg = 0
        else:
            if tmp_pos < tmp_neg:
                tmp_pos = 0
            else:
                tmp_pos = 0
                tmp_neg = 0
        
        # Calculate the True Range (TR) for the current data point
        tr = max(high_price - low_price, abs(high_price - prev_close), abs(low_price - prev_close))
        
        # Calculate the Positive Directional Indicator (PDI) and Negative Directional Indicator (NDI) for the current data point
        pdi[i] = 100 * tmp_pos / tr if tr != 0 else 0
        ndi[i] = 100 * tmp_neg / tr if tr != 0 else 0
        
        # Calculate the smoothed PDI and NDI values using an Exponential Moving Average (EMA)
        pdi[i] = ExponentialMA(i, adx_period, pdi[i-1], pdi)
        ndi[i] = ExponentialMA(i, adx_period, ndi[i-1], ndi)
        # Calculate the temporary value for the current data point
        tmp = pdi[i] + ndi[i]
        tmp_buffer[i] = 100 * abs((pdi[i] - ndi[i]) / tmp) if tmp != 0 else 0
    
    # Calculate the smoothed ADX values using an Exponential Moving Average (EMA)
    for i in range(1, len(high)):
        adx[i] = ExponentialMA(i, adx_period, adx[i-1], tmp_buffer)
    
    # Return the ADX array
    return adx
# Extract the 'high', 'low', and 'close' columns from the DataFrame
high = df['high'].to_numpy()
low = df['low'].to_numpy()
close = df['close'].to_numpy()

# Calculate the ADX values
adx = calculate_adx(high, low, close, 14)

# Add the ADX values to the DataFrame
df['ADX'] = adx
