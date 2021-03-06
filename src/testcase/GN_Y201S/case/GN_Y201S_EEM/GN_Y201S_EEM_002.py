# coding=utf-8
from src.testcase.GN_Y201S.WidgetOperation import *


class GNY201SEem2(WidgetOperation):
    @case_run(False)
    def run(self):
        self.case_module = u"FUT_EEM_电量计量(#61)"  # 用例所属模块
        self.case_title = u'FUT_EEM_用电图表显示周期设置'  # 用例名称
        self.zentao_id = "558"  # 禅道ID

    # 用例动作
    def case(self):
        device = conf["MAC"]["AL"][0]
        self.set_power(device, "power_off")

        self.choose_home_device(device)

        self.close_mode_timer()

        self.close_general_timer()

        self.ac.swipe(0.5, 0.9, 0.5, 0.1, self.driver)

        self.widget_click(self.page["control_device_page"]["elec"],
                          self.page["elec_page"]["title"])

        elec_elements = self.wait_widget(self.page["elec_page"]["elec_time"])
        elec_elements = self.ac.get_attribute(elec_elements, "name")
        self.debug.info("[ELEC_INFO]%s" % elec_elements)
        if not re.findall(u"日总电量", elec_elements):
            raise TimeoutException("day elec time is wrong, current: %s" % [elec_elements])

        self.widget_click(self.page["elec_page"]["week"],
                          self.page["elec_page"]["title"])

        elec_elements = self.wait_widget(self.page["elec_page"]["elec_time"])
        elec_elements = self.ac.get_attribute(elec_elements, "name")
        self.debug.info("[ELEC_INFO]%s" % elec_elements)
        if not re.findall(u"周总电量", elec_elements):
            raise TimeoutException("week elec time is wrong, current: %s" % [elec_elements])

        self.widget_click(self.page["elec_page"]["month"],
                          self.page["elec_page"]["title"])

        elec_elements = self.wait_widget(self.page["elec_page"]["elec_time"])
        elec_elements = self.ac.get_attribute(elec_elements, "name")
        self.debug.info("[ELEC_INFO]%s" % elec_elements)
        if not re.findall(u"月总电量", elec_elements):
            raise TimeoutException("month elec time is wrong, current: %s" % [elec_elements])

        self.widget_click(self.page["elec_page"]["year"],
                          self.page["elec_page"]["title"])

        elec_elements = self.wait_widget(self.page["elec_page"]["elec_time"])
        elec_elements = self.ac.get_attribute(elec_elements, "name")
        self.debug.info("[ELEC_INFO]%s" % elec_elements)
        if not re.findall(u"年总电量", elec_elements):
            raise TimeoutException("year elec time is wrong, current: %s" % [elec_elements])

        self.widget_click(self.page["elec_page"]["to_return"],
                          self.page["control_device_page"]["title"])

        self.widget_click(self.page["control_device_page"]["elec"],
                          self.page["elec_page"]["title"])

        elec_elements = self.wait_widget(self.page["elec_page"]["elec_time"])
        elec_elements = self.ac.get_attribute(elec_elements, "name")
        self.debug.info("[ELEC_INFO]%s" % elec_elements)
        if not re.findall(u"日总电量", elec_elements):
            raise TimeoutException("day elec time2 is wrong, current: %s" % [elec_elements])
