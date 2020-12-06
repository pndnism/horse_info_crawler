from dataclasses import dataclass

from selenium import webdriver


class SeleniumClient:
    @classmethod
    def create_web_driver(cls):
        return SeleniumClientContextManager(cls())

    def get_web_driver(self):
        return self._driver

    def close(self):
        self._driver.quit()

    def __init__(self):
        self._create_new_driver()

    def _create_new_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        # NOTE: ウィンドウサイズが大きいとクラッシュしやすくなるようなので小さく設定する
        # https://qiita.com/oieioi/items/0e9468c1d2ad2da1a94c
        options.add_argument("--window-size=800,800")
        options.add_argument("--disable-dev-shm-usage")

        self._driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=options.to_capabilities()
        )


@dataclass(frozen=True)
class SeleniumClientContextManager:
    selenium_client: SeleniumClient

    def __enter__(self):
        return self.selenium_client.get_web_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.selenium_client.close()
