from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from threading import Timer
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom

app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

#create notifier
nManager = notifications.ToastNotificationManager
notifier = nManager.create_toast_notifier(app)

#define your notification as string
tString = """
  <toast>
    <visual>
      <binding template='ToastGeneric'>
        <text>COVID Vaccine Available</text>
        <text>You're now eligible to get the COVID-19 vaccine. Go to the program to choose your options.</text>
      </binding>
    </visual>       
  </toast>
"""

#convert notification to an XmlDocument
xDoc = dom.XmlDocument()
xDoc.load_xml(tString)

# timer to call function on an interval
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# start selenium
driver = webdriver.Chrome("C:/Users/Nwott/Documents/Development/GIVECOVIDVACCINERN/files/chromedriver.exe")
driver.get("https://covid-19.ontario.ca/book-vaccine/")


def buffer():
    print("...")



def book_appointment(is_creator):
    #display notification
    notifier.show(notifications.ToastNotification(xDoc))
    if is_creator == False:
        card_type = input("1 - Green Ontario photo health card (expired cards accepted)\n2 - Red and white Ontario health card\n3 - No Ontario health card\n\nEnter health card type:")
        if card_type == "1":
            appointment_type = input("1 - The provincial online booking system\n2 - A participating pharmacy\n\nEnter appointment type: ")
        elif card_type == "2":
            appointment_type = input("1 - The Ontario call centre\n2 - A participating pharmacy\n\nEnter appointment type: ")
        elif card_type == "3":
            print("Call 1‑833‑943‑3900 between 8am and 8pm to book an appointment.")


# check if eligible
def check(postal, year, is_creator):
    postal_code_input = driver.find_element_by_id("postal_code_input")
    postal_code_input.send_keys(postal)
    birth_year = driver.find_element_by_id("birthyear_input")
    birth_year.send_keys(year)
    start_button = driver.find_element_by_id("view_priority_groups_btn")
    start_button.click()
    ineligible = driver.find_element_by_id("ineligible")

    if ineligible.is_displayed():
        print("Ineligible, reloading in 5 seconds")
        rt = RepeatedTimer(1, buffer) 
        try:
            sleep(5) 
        finally:
            driver.refresh()
            rt.stop() 
            check(postal, year, is_creator)
    else: 
        book_appointment(is_creator)


def input_numbers():
    postal_code = input("Input postal code: ")
    year_born = input("Input year born: ")
    check(postal_code, year_born, False)

input_numbers()
