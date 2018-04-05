
def find_pumps(candle_data, percent_volume, percent_price=0):
    result = []
    volumes = [float(item[5]) for item in candle_data]
    total_volume = sum(volumes)
    if total_volume == 0:
        return result

    for i in range(0, len(candle_data)):
        if volumes[i] / total_volume * 100 < percent_volume:
            continue

        open_price = float(candle_data[i][1])
        close_price = float(candle_data[i][4])
        if (close_price - open_price) / open_price * 100 < percent_price:
            continue

        pump_time = candle_data[i][0]
        result.append(pump_time)

    return result
