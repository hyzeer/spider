import xlrd
import socket
import threading

class Check(threading.Thread):
    def __init__(self, eoc):
        threading.Thread.__init__(self)
        self.ip = eoc[0]
        self.addr = eoc[1]
        self.mac = eoc[2]
        self.port = eoc[3]

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(200)
            result = s.connect_ex((self.ip, 80))
            if result != 0:
                print("{0}: {1} {2} {3} {4}".format(result, self.ip, self.addr, self.mac, self.port))


if __name__ == '__main__':
    with xlrd.open_workbook(u'\\\\10.73.230.6\\excel\\EOC局端表.xlsx') as data:
        table = data.sheet_by_index(0)
        eoc = list(zip(table.col_values(1,3),table.col_values(2,3),
                       table.col_values(4,3),table.col_values(5,3)))

    for i in eoc:
        Check(eoc=i).start()