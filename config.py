# 需要用到的常数和全局变量

import pandas as pd

# 常量定义
REARTH = 6371000  # 地球半径(米)
PREWIN = 5.0  # 前置时间窗口(秒)
PSTWIN = 30.0  # 后置时间窗口(秒)
DTP = 5.0  # 预处理时间偏移
SDW = 0.9  # 信号衰减窗口比例
DDW = 0.99  # 数据衰减窗口比例


class SmConfig:
    def __init__(self):
        # 地震发生时间
        self.year: int = 0
        self.month: int = 0
        self.day: int = 0
        self.hour: int = 0
        self.minute: int = 0
        self.hyptime: float = 0.0

        # 震源位置
        self.hyplat: float = 0.0  # 纬度
        self.hyplon: float = 0.0  # 经度
        self.hypdep: float = 0.0  # 深度(m)

        # 其他参数
        self.data_dir: str = ""
        self.stdismin: float = 0.0  # 最小震中距(m)
        self.stdismax: float = 0.0  # 最大震中距(m)
        self.out_dir: str = ""

        # 台站信息
        self.stanum: int = 0
        self.unit2m: float = 0.0

        self.stations = pd.DataFrame(
            {
                "station_code": [],  # stcode
                "latitude": [],  # lat
                "longitude": [],  # lon
                "start_time": [],  # start
                "p_arrival": [],  # ponset
                "duration": [],  # length
                "sampling_rate": [],  # sample
                "distance": [],  # dis
            }
        )
