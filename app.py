from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

options = webdriver.FirefoxProfile()
options.set_preference("browser.download.folderList",2)
options.set_preference('browser.download.dir', 'C:\\Users\\Tyler\\Desktop')
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

class SportTracker:
    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.bot = webdriver.Firefox(options)

    def loginStrava(self):
        bot = self.bot
        # Login to Strava
        bot.get('https://www.strava.com/login')
        time.sleep(3)
        email = bot.find_element_by_name('email')
        password = bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.email)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def changeActivityName(self):
        bot = self.bot
        # Load feed
        bot.get('https://www.strava.com/dashboard?feed_type=my_activity')
        time.sleep(3)

        # Find latest activity address
        activity_address = bot.find_element_by_css_selector('.title-text a').get_attribute('href')

        # Go to activity edit address
        bot.get(activity_address + '/edit')
        time.sleep(3)

        # Change name from run to paddle
        title = bot.find_element_by_name('activity[name]')
        new_title = title.get_attribute("value").partition(' ')[0] + ' Paddle'
        title.clear()
        title.send_keys(new_title)

        # Change sport to Kayaking
        sport = Select(bot.find_element_by_id('activity_type'))
        sport.select_by_value('Kayaking')

        # Save changes
        bot.find_element_by_xpath('//button[text()="Save"]').click()
        time.sleep(10)

    def downloadGPX(self):
        bot = self.bot
        # Download GPX file
        bot.find_element_by_class_name("icon-nav-more").click()
        time.sleep(5)
        bot.find_element_by_link_text('Export GPX').click()

    def garmin(self, gpx_address):
        bot = self.bot
        # Login to Garmin
        bot.get('https://connect.garmin.com/signin')
        time.sleep(15)
        bot.switch_to.frame('gauth-widget-frame-gauth-widget')
        email = bot.find_element_by_id('username')
        password = bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.email)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(20)

        # Upload GPX file
        bot.switch_to.default_content()
        bot.find_element_by_class_name('icon-activity-upload').click()
        time.sleep(20)
        bot.find_element_by_link_text('Import Data').click()
        time.sleep(20)

        # JS to drop file

        JS_DROP_FILE = """
        var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

        var input = document.createElement('INPUT');
        input.type = 'file';
        input.onchange = function () {
        var rect = target.getBoundingClientRect(),
            x = rect.left + (offsetX || (rect.width >> 1)),
            y = rect.top + (offsetY || (rect.height >> 1)),
            dataTransfer = { files: this.files };

        ['dragenter', 'dragover', 'drop'].forEach(function (name) {
            var evt = document.createEvent('MouseEvent');
            evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
            evt.dataTransfer = dataTransfer;
            target.dispatchEvent(evt);
        });

        setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
            """

        def drag_and_drop_file(drop_target, path):
            driver = drop_target.parent
            file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
            file_input.send_keys(path)

        drop_target = bot.find_element_by_id('import-data')
        drag_and_drop_file(drop_target, gpx_address)
        time.sleep(10)
        bot.find_element_by_id('import-data-start').click()
        time.sleep(10)
        bot.find_element_by_link_text('View Details').click()
        time.sleep(10)

        # Set activity type
        bot.find_element_by_id('event-type-dropdown').click()
        time.sleep(3)
        bot.find_element_by_link_text('Training').click()
        time.sleep(3)
        bot.find_element_by_id('activityTypeDropdownPlaceholder').click()
        time.sleep(3)
        bot.find_element_by_link_text('Paddling').click()


        

# Add email and password for Garmin and Strava   
email = ''
password = ''
# Add file location
gpx_address = ''

user1 = SportTracker(email, password)
user1.loginStrava()
user1.changeActivityName()
user1.downloadGPX()
user1.garmin(gpx_address)
