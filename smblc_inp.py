from config import SmConfig, PREWIN
import pandas as pd
from disazi import disazi


def read_smblc_input(filename):
    """
    读取smblc输入文件，跳过注释行，提取相关参数
    参数:
        filename: 输入文件名
    返回:
        SmConfig 对象，包含所有参数
    """
    config = SmConfig()

    with open(filename, "r") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    # 1. 读取地震发生时间和震源参数
    origin_time = lines[0].split()
    config.year = int(origin_time[0])
    config.month = int(origin_time[1])
    config.day = int(origin_time[2])
    config.hour = int(origin_time[3])
    config.minute = int(origin_time[4])
    config.hyptime = float(origin_time[5])

    # 2. 读取震源位置
    hypocenter = lines[1].split()
    config.hyplat = float(hypocenter[0])  # 纬度
    config.hyplon = float(hypocenter[1])  # 经度
    config.hypdep = float(hypocenter[2]) * 1000  # 深度(m)

    # 3. 读取强震动数据文件夹
    config.data_dir = lines[2].strip().strip("'./")

    # 4. 读取震中距阈值
    distance_thresh = lines[3].split()
    config.stdismin = float(distance_thresh[0]) * 1000  # 最小震中距(m)
    config.stdismax = float(distance_thresh[1]) * 1000  # 最大震中距(m)

    # 5. 读取输出参数
    config.out_dir = lines[4].strip().strip("'./")

    # 6. 读取台站信息
    station_file = f"{config.data_dir}/SMDataInfo.dat"
    with open(station_file, "r") as sf:
        station_lines = [
            line.strip()
            for line in sf
            if line.strip() and not line.strip().startswith("#")
        ]
    if len(station_lines) < 3:
        raise ValueError("台站信息不完整")
    # 验证地震时间和震源参数
    station_origin_time = station_lines[0].split()
    if (
        config.year != int(station_origin_time[0])
        or config.month != int(station_origin_time[1])
        or config.day != int(station_origin_time[2])
        or config.hour != int(station_origin_time[3])
        or config.minute != int(station_origin_time[4])
        or config.hyptime != float(station_origin_time[5])
    ):
        raise ValueError("地震时间不匹配")

    # 验证震源位置
    station_hypocenter = station_lines[1].split()
    if (
        config.hyplat != float(station_hypocenter[0])
        or config.hyplon != float(station_hypocenter[1])
        or config.hypdep != float(station_hypocenter[2]) * 1000
    ):
        raise ValueError("震源位置不匹配")
    datacanshu = station_lines[2].split()
    config.stanum = int(datacanshu[0])
    config.unit2m = float(datacanshu[1])
    # 读取台站信息并存储到config.stations中
    stations_data = []
    for line in station_lines[3:]:
        values = line.split()
        stations_data.append(
            {
                "station_code": values[0],
                "latitude": float(values[1]),
                "longitude": float(values[2]),
                "start_time": float(values[3]),
                "p_arrival": float(values[4]),
                "duration": float(values[5]),
                "sampling_rate": float(values[6]),
            }
        )
        if float(values[4]) < float(values[3]) + PREWIN:
            raise ValueError("P波到时小于PREWIN")
        if float(values[6]) <= 0:
            raise ValueError("采样率小于等于0")
    config.stations = pd.DataFrame(stations_data)
    # 将台站按震中距排序
    config.stations["distance"] = config.stations.apply(
        lambda x: disazi(config.hyplat, config.hyplon, x["latitude"], x["longitude"]),
        axis=1,
    )
    config.stations = config.stations.sort_values(by="distance", ignore_index=True)
    return config
