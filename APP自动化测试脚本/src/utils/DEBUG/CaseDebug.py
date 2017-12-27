# coding=utf-8
from src.common.AppInit import *
from src.testcase.GN_F1331.WidgetOperation import *
from src.testcase.GN_F1331.page.ReadAPPElement import *
from src.utils.CollectLog import *
from src.utils.Debug import *

device_list = AppInit().app_init()
deviceName = device_list.keys()[0]
device_info = device_list[deviceName]
device_info["port"] = 4725
device_info["bp_port"] = 4726
device_info["wda_port"] = 4727

app_os = device_info["platformName"]
app = device_info["app"]
port = device_info["port"]
bp_port = device_info["bp_port"]
wda_port = device_info["wda_port"]
device_name = device_info["udid"]
serial_port = int(conf["phone_name"][device_name]["serial_port"])
serial_com = conf["phone_name"][device_name]["serial_com"]
device_mac = conf["phone_name"][device_name]["devices_mac"]
serial_command_queue = Queue.Queue()
serial_result_queue = Queue.Queue()
receive_serial = ReceiveSerial(serial_com, serial_port)
serial_sever = receive_serial.serial_sever
serial_main_data_queue = receive_serial.serial_main_data_queue

print('appium -a 127.0.0.1 -p %s -bp %s -U %s --no-reset --local-timezone' % (port, bp_port, deviceName))

driver = webdriver.Remote('http://localhost:%s/wd/hub' % port, device_info['desired_caps'])


def launch_receive_serial():
    receive_serial.receive_log()


def receive_serial_command():
    serial_command_queue.put_nowait((False, "", ""))
    receive_serial.start_stop_filtrate_data(serial_command_queue)


page = PageElement(app_os).get_page_element()
device_info["page"] = page

ac = AppiumCommand(app_os)
logger = check_log(device_info)
debug = check_debug(device_info)

device_info["logger"] = logger
device_info["debug"] = debug
widget_check_unit = WidgetCheckUnit(driver, device_info)
widget_click = widget_check_unit.widget_click
wait_widget = widget_check_unit.wait_widget
serial_receive_t = threading.Thread(target=launch_receive_serial)
serial_command_t = threading.Thread(target=receive_serial_command)
serial_receive_t.start()
serial_command_t.start()


class WidgetTest(WidgetOperation):
    def __init__(self):
        self.ac = ac
        self.app = app
        self.page = page
        self.driver = driver
        self.logger = logger
        self.debug = debug
        self.widget_click = widget_click
        self.wait_widget = wait_widget
        self.device_mac = device_mac
        self.serial_command_queue = serial_command_queue
        self.serial_result_queue = serial_result_queue


class b(WidgetTest):
    def case(self):
        self.choose_home_device(conf["MAC"][self.app][self.device_mac])

        self.set_power("main_button_off")

        self.input_serial_command("power", "set_cycle_timer", "launch_cylce_timer")

        self.widget_click(self.page["control_device_page"]["up_timer"],
                          self.page["up_timer_page"]["title"])

        self.widget_click(self.page["up_timer_page"]["cycle_timer"],
                          self.page["up_timer_page"]["cycle_timer_button"])

        now = time.strftime("%H:%M")

        delay_time_1, delay_time_2 = ["delay", "00:01"], ["delay", "00:01"]
        tmp = self.create_cycle_timer("up_timer_page", now, delay_time_1, delay_time_2, u"永久循环")
        start_time_1, set_time_1, start_time_2, set_time_2 = tmp[0]

        while True:
            if time.time() > set_time_2 + 10:
                break
            print(time.time())
            time.sleep(1)

        #
        btn_state_list = self.check_serial_button_state()

        btn_state = btn_state_list[0]
        if start_time_1 - 15 <= btn_state[0] <= start_time_1 + 15 and [1, 0, 0] == btn_state[1:]:
            self.logger.info(u"[APP_INFO]device state: %s" % btn_state)
        else:
            raise TimeoutException("device state error, current: %s" % btn_state)

        btn_state = btn_state_list[1]
        if set_time_1 - 15 <= btn_state[0] <= set_time_1 + 15 and [0, 0, 0] == btn_state[1:]:
            self.logger.info(u"[APP_INFO]device state: %s" % btn_state)
        else:
            raise TimeoutException("device state error, current: %s" % btn_state)

        btn_state = btn_state_list[2]
        if set_time_2 - 15 <= btn_state[0] <= set_time_2 + 15 and [1, 0, 0] == btn_state[1:]:
            self.logger.info(u"[APP_INFO]device state: %s" % btn_state)
        else:
            raise TimeoutException("device state error, current: %s" % btn_state)

        #
        set_cycle_timer_list = self.check_serial_set_cycle_timer()

        set_cycle_timer = set_cycle_timer_list[0]
        set_cycle_timer_name = set_cycle_timer[-2]
        if start_time_1 - 15 <= set_cycle_timer[0] <= start_time_1 + 15:
            self.logger.info(u"[APP_INFO]device state: %s" % set_cycle_timer)
        else:
            raise TimeoutException("device state error, current: %s" % set_cycle_timer)

        #
        launch_cycle_timer_list = self.check_serial_launch_cycle_timer()

        launch_cycle_timer = launch_cycle_timer_list[0]
        launch_cycle_timer_name = launch_cycle_timer[-2]
        if (set_time_1 - 15 <= launch_cycle_timer[0] <= set_time_1 + 15
                and launch_cycle_timer_name == set_cycle_timer_name):
            self.logger.info(u"[APP_INFO]device state: %s" % launch_cycle_timer)
        else:
            raise TimeoutException("device state error, current: %s" % launch_cycle_timer)

        launch_cycle_timer = launch_cycle_timer_list[1]
        launch_cycle_timer_name = launch_cycle_timer[-2]
        if (set_time_2 - 15 <= launch_cycle_timer[0] <= set_time_2 + 15
                and launch_cycle_timer_name == set_cycle_timer_name):
            self.logger.info(u"[APP_INFO]device state: %s" % launch_cycle_timer)
        else:
            raise TimeoutException("device state error, current: %s" % launch_cycle_timer)


b().case()


class fix(WidgetTest):
    pass


WidgetTest = fix
