from utils.handle_yaml import WriteUserCommand
import time
from threading import Timer
from appium_refactor.util.dos_cmd import DosCmd
import threading
import multiprocessing
'''
监控mitmproxy是否崩溃
这里是100秒检测一次
'''
def Mitmproxy_Monitor(wuc,temp):
    print(temp)
    if temp == wuc.get_value('num'):
        print('mitmproxy崩溃了！')

        t = threading.Thread(target=reboot_mitmproxy)
        t.start()
        # p = multiprocessing.Process(target=reboot_mitmproxy)
        # p.start()
        # 这里要执行方法，杀掉mitmdump，重启新的mitmdump
    else:
        temp = wuc.get_value('num')
    t = Timer(interval=10, function=Mitmproxy_Monitor, args=(wuc, temp))
    t.start()



def reboot_mitmproxy():
    dos = DosCmd()
    result_list = dos.excute_cmd_result('netstat -aon|findstr "8889"')
    if len(result_list) > 0:
        pid = result_list[-1][-9:].strip()
        dos.excute_cmd('taskkill /pid %s  -t  -f' % pid)
        time.sleep(10)
    dos.excute_cmd('mitmweb -s D:/PycharmProjects/GetSpider/test_decode_dedao.py -p 8889')


if __name__ == '__main__':
    wuc = WriteUserCommand()
    temp = 0
    t = Timer(interval=10, function=Mitmproxy_Monitor, args=(wuc,temp))
    t.start()





# class Mitmproxy_Monitor():
#     def __init__(self):
#         self.wuc = WriteUserCommand()
#
#     def time_monitor(self, sec):
#         pass
