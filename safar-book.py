import os
import sys

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import psutil


def main(land_url, result):
    PROCNAME = "phantomjs.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
    PROCNAME = "geckodriver.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

    driver = webdriver.PhantomJS()
    driver.get("https://learning.oreilly.com/home/")

    elem = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/form/div[1]/input')
    elem.send_keys(login)
    elem = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/form/div[2]/input')
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    try:
        elem = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/form/div[4]/button')
        elem.click()
    except:
        pass
    elem.send_keys(Keys.RETURN)
    time.sleep(15)
    driver.save_screenshot('screen.png')

    driver2 = webdriver.Firefox()
    driver2.get("https://learning.oreilly.com/home/")
    elem = driver2.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/form/div[1]/input')
    elem.send_keys(str(login))
    elem = driver2.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/form/div[2]/input')
    elem.send_keys(str(pwd))
    elem.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.get(url=land_url)
    driver2.get(url=land_url)
    time.sleep(5)
    from PyPDF2 import PdfFileMerger

    pdfs = []
    xpath = '//*[@id="font-controls"]'
    for i in range(10):
        try:
            elem = driver.find_element_by_xpath(xpath=xpath)
            time.sleep(1)
            elem.send_keys('f')
            elem.send_keys('f')
            elem.send_keys('f')
            elem.send_keys('f')
            elem.send_keys('f')
            break
        except:
            pass


    last_last_page = None
    for count in range(1000):
        def download(driver, target_path):
            """Download the currently displayed page to target_path."""

            def execute(script, args):
                driver.execute('executePhantomScript',
                               {'script': script, 'args': args})

            # hack while the python interface lags
            driver.command_executor._commands['executePhantomScript'] = \
                ('POST', '/session/$sessionId/phantom/execute')

            # set page format
            # inside the execution script, webpage is "this"
            page_format = \
                'this.paperSize = {format: "A4", orientation: "portrait" };'
            execute(page_format, [])
            render = '''this.render("{}")'''.format(target_path)
            execute(render, [])

        pdfs.append("save_me{}.pdf".format(count))
        download(driver, "save_me{}.pdf".format(count))
        current_url = driver2.current_url

        def click_next():
            try:
                css = 'div.t-sbo-next:nth-child(3) > a:nth-child(1) > div:nth-child(3)'
                elem = driver2.find_element_by_css_selector(css_selector=css)
            except:
                try:
                    css = 'div.t-sbo-next:nth-child(2) > a:nth-child(1) > div:nth-child(3)'
                    elem = driver2.find_element_by_css_selector(css_selector=css)
                except:
                    driver2.refresh()
                    time.sleep(5)
                    css = 'div.t-sbo-next:nth-child(2) > a:nth-child(1) > div:nth-child(3)'
                    elem = driver2.find_element_by_css_selector(css_selector=css)
            try:
                elem.click()
            except:
                elem.send_keys(Keys.RIGHT)

        counter = 0
        while driver2.current_url == current_url:
            try:
                click_next()
            except:
                break
            time.sleep(0.01)
            counter += 1
            if counter >= 600:
                driver2.refresh()
                time.sleep(5)
                counter -= 600
        driver.get(driver2.current_url)
        if last_last_page == driver2.current_url:
            break
        if len(pdfs) > 2:
            last_last_page = current_url

    merger = PdfFileMerger()
    print(pdfs)
    for pdf in pdfs:
        merger.append(open(pdf, 'rb'))
    with open(result, 'wb') as fout:
        merger.write(fout)
    merger.close()
    driver.close()
    driver2.close()
    for pdf in pdfs:
        os.remove(pdf)


if __name__ == '__main__':
    link = sys.argv[1]
    result = sys.argv[2]
    login = sys.argv[3]
    pwd = sys.argv[4]
    main(link, result)
