# coding=utf-8
from ReadAPPElement import *


class b(a):
    def case(self):
        try:
            self.wait_widget(self.page["control_device_page"]["power_off"])
        except TimeoutException:
            self.widget_click(self.page["control_device_page"]["power_button"],
                              self.page["control_device_page"]["power_off"])
        
        self.widget_click(self.page["control_device_page"]["normal_timer"],
                          self.page["normal_timer_page"]["title"])
        
        start_time_1, set_time_1 = self.create_normal_timer(2, "power_on")
        start_time_2, set_time_2 = self.create_normal_timer(4, "power_off")
        
        self.widget_click(self.page["normal_timer_page"]["to_return"],
                          self.page["control_device_page"]["title"])
        
        self.wait_widget(self.page["control_device_page"]["power_off"])
        
        self.check_timer(2, u"设备已开启", set_time_1)
        self.check_timer(4, u"设备已关闭", set_time_2)
    
    def create_normal_timer(self, delay_time, power):
        self.widget_click(self.page["normal_timer_page"]["add_timer"],
                          self.page["add_normal_timer_page"]["title"])
        
        start_time, set_time = self.set_timer_roll(self.page["add_normal_timer_page"]["timer_h"],
                                                   self.page["add_normal_timer_page"]["timer_m"],
                                                   self.page["add_normal_timer_page"]["set_timer"],
                                                   delay_time)
        
        self.widget_click(self.page["add_normal_timer_page"][power],
                          self.page["add_normal_timer_page"]["title"])
        
        attribute = self.ac.get_attribute(self.wait_widget(self.page["add_normal_timer_page"]["repeat"]), "name")
        if u"每天" not in attribute:
            self.widget_click(self.page["add_normal_timer_page"]["repeat"],
                              self.page["timer_repeat_page"]["title"])
            
            self.widget_click(self.page["timer_repeat_page"]["repeat_button"],
                              self.page["timer_repeat_page"]["everyday"])
            
            self.widget_click(self.page["timer_repeat_page"]["everyday"],
                              self.page["timer_repeat_page"]["title"])
            
            self.widget_click(self.page["timer_repeat_page"]["to_return"],
                              self.page["add_normal_timer_page"]["title"])
            
            attribute = self.ac.get_attribute(self.wait_widget(self.page["add_normal_timer_page"]["repeat"]), "name")
            if u"每天" not in attribute:
                raise TimeoutException("Cycle set error")
        
        self.widget_click(self.page["add_normal_timer_page"]["saved"],
                          self.page["normal_timer_page"]["title"])
        return start_time, set_time
    
    def check_timer(self, time_delay, power_state, times):
        self.now = time.time()
        element = self.wait_widget(self.page["control_device_page"]["power_state"])
        while True:
            attribute = self.ac.get_attribute(element, "name")
            if time.strftime("%H:%M") == times:
                time.sleep(10)
                if attribute == power_state:
                    break
                else:
                    raise TimeoutException("Device state Error")
            else:
                if time.time() < self.now + time_delay * 60 + 30:
                    time.sleep(1)
                else:
                    raise TimeoutException("Device state Error, time out")


b().case()


class c(b):
    def case(self):
        delay_time_1 = "00:01"
        start_time_1, set_time_1 = self.set_timer_roll(self.page["piocc_mode_timer_page"]["end_h"],
                                                       self.page["piocc_mode_timer_page"]["end_m"],
                                                       self.page["piocc_mode_timer_page"]["end_time_text"],
                                                       delay_time_1)


c().case()
