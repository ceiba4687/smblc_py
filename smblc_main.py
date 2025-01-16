# 主函数
import config
from smblc_inp import read_smblc_input


def main():
    file_name = "/home/ceiba/Code/smblc_py/test.inp"
    seis_info = read_smblc_input(file_name)
    print(seis_info.stations)


if __name__ == "__main__":
    main()
