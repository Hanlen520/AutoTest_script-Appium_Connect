# coding=utf-8
from src.testcase.GN_F1331.WidgetOperation import *


class GNF1331NormalTimer8(WidgetOperation):
    @case_run(False)
    def run(self):
        self.case_module = u"APP功能测试"  # 用例所属模块
        self.case_title = u'上、中层普通定时'  # 用例名称
        self.zentao_id = 1216  # 禅道ID

    # 用例动作
    def case(self):
        self.choose_home_device(conf["MAC"][self.app][self.device_mac])

        self.delete_out_date_timer()

        self.set_power("main_button_off")

        self.input_serial_command("power", "set_normal_timer", "launch_normal_timer_once")

        # 上层
        # self.widget_click(self.page["control_device_page"]["up_timer"],
        #                   self.page["up_timer_page"]["title"])
        #
        # self.delete_normal_timer("up")
        #
        # now = time.strftime("%H:%M")
        #
        # delay_time_1 = 1
        # delay_time_2 = 2
        # start_time_1, set_time_1, cycle_1 = self.create_normal_timer("up_timer_page", now, delay_time_1, "power_on")
        # start_time_2, set_time_2, cycle_2 = self.create_normal_timer("up_timer_page", now, delay_time_2, "power_off")
        #
        # self.widget_click(self.page["up_timer_page"]["to_return"],
        #                   self.page["control_device_page"]["title"])

        # 中层
        self.widget_click(self.page["control_device_page"]["mid_timer"],
                          self.page["mid_timer_page"]["title"])

        self.delete_normal_timer("mid")

        now = time.strftime("%H:%M")

        delay_time_3 = 1
        delay_time_4 = 2
        start_time_3, set_time_3, cycle_3 = self.create_normal_timer("mid_timer_page", now, delay_time_3, "power_on")
        start_time_4, set_time_4, cycle_4 = self.create_normal_timer("mid_timer_page", now, delay_time_4, "power_off")

        while True:
            if time.time() > set_time_4 + 10:
                break
            print(time.time())
            time.sleep(1)

        #####
        btn_state_list = self.check_serial_button_state()  # 开关
        set_normal_timer_list = self.check_serial_set_normal_timer()  # 定时设置
        launch_normal_timer_once_list = self.check_serial_launch_normal_timer_once()  # 定时执行开
        timer_list = self.get_timer_id_from_set(set_normal_timer_list)
        result = self.get_layer_timer_from_launch(timer_list,
                                                  a=launch_normal_timer_once_list)
        self.debug.info(u"[APP_INFO]device state: \n"
                        u"btn_state_list: %s;\n"
                        u"set_normal_timer_list: %s;\n"
                        u"launch_normal_timer_once_list: %s;\n"
                        u"timer_list: %s;\n"
                        u"result: %s;"
                        % (btn_state_list, set_normal_timer_list, launch_normal_timer_once_list, timer_list, result))

        up_normal_id, mid_normal_id = timer_list  # timer id
        up_launch_normal_timer_list, mid_launch_normal_timer_list = \
            result[up_normal_id]["a"], result[mid_normal_id]["a"]
        self.debug.info(u"[APP_INFO]timer_list: %s;\n"
                        u"up_launch_normal_timer_list: %s;\n"
                        u"mid_launch_normal_timer_list: %s;"
                        % (timer_list, up_launch_normal_timer_list, mid_launch_normal_timer_list))
        # 上层
        # 设置
        set_normal_timer = set_normal_timer_list[0]
        set_normal_timer_id = set_normal_timer[1]
        result = [start_time_1 - 15 <= set_normal_timer[0] <= start_time_1 + 15]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (set_normal_timer, result))
        # 执行开→关
        launch_normal_timer = up_launch_normal_timer_list[0]
        launch_normal_timer_id = launch_normal_timer[1]
        result = [set_time_1 - 15 <= launch_normal_timer[0] <= set_time_1 + 15,
                  launch_normal_timer_id == set_normal_timer_id]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (launch_normal_timer, result))

        # 中层
        # 设置
        set_normal_timer = set_normal_timer_list[1]
        set_normal_timer_id = set_normal_timer[1]
        result = [start_time_2 - 15 <= set_normal_timer[0] <= start_time_2 + 15]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (set_normal_timer, result))
        # 执行开→关
        launch_normal_timer = mid_launch_normal_timer_list[0]
        launch_normal_timer_id = launch_normal_timer[1]
        result = [set_time_2 - 15 <= launch_normal_timer[0] <= set_time_2 + 15,
                  launch_normal_timer_id == set_normal_timer_id]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (launch_normal_timer, result))

        # 开关
        # 100, 000, 010, 000
        # 上层初始开关,先跳开
        btn_state = btn_state_list[0]
        btn_all_layer = btn_state[1]
        result = [start_time_1 - 15 <= btn_state[0] <= start_time_1 + 15,
                  btn_all_layer == "100"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))
        # 上层开→关开关
        btn_state = btn_state_list[1]
        btn_all_layer = btn_state[1]
        result = [set_time_1 - 15 <= btn_state[0] <= set_time_1 + 15,
                  btn_all_layer == "000"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))

        # 中层初始开关,先跳开
        btn_state = btn_state_list[2]
        btn_all_layer = btn_state[1]
        result = [start_time_2 - 15 <= btn_state[0] <= start_time_2 + 15,
                  btn_all_layer == "010"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))
        # 中层开→关开关
        btn_state = btn_state_list[3]
        btn_all_layer = btn_state[1]
        result = [set_time_2 - 15 <= btn_state[0] <= set_time_2 + 15,
                  btn_all_layer == "000"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))
