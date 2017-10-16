# coding=utf-8
from src.testcase.common.WidgetOperation_JD import *


class JDAppElectricityMeter11(WidgetOperationJD):
    @case_run_jd(False)
    def run(self):
        self.case_module = u"APP功能测试"  # 用例所属模块
        self.case_title = u'实时功率检查_500W'  # 用例名称
        self.zentao_id = 1133  # 禅道ID

    # 用例动作
    def case(self):
        self.choose_home_device(conf["MAC"][0])

        self.set_power("power_on")

        power = []

        i = 10
        end_time = time.time() + 60
        while i > 0:
            if time.time() < end_time:
                try:
                    tmp = self.ac.get_attribute(self.wait_widget(self.page["control_device_page"]["power"]), "name")
                    if isinstance(tmp, unicode):
                        power.append(tmp)
                        if len(power) >= 60:
                            break
                except TimeoutException:
                    pass
            else:
                end_time = time.time() + 60
                i -= 1

        power = map(lambda x: float(x.replace(" W", "")), power)

        aver_power = sum(power) / len(power)

        if aver_power / 500 > 0.01:
            raise TimeoutException()

        self.case_over(True)
