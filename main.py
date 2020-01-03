from constants import proxy, Request
# from file import GetStopInfoJsonFile, GetLineJsonFile
from file import YandexApiRequestFile
from functions import convert


def main():
    file = YandexApiRequestFile(Request.GET_STOP_INFO, '732').write_obtained_data()
    # file = YandexApiRequestFile(Request.GET_LINE, '732').write_obtained_data()
    print(convert(file.data_dict))


if __name__ == '__main__':
    main()
