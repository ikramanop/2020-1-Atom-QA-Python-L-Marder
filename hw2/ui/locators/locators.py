from selenium.webdriver.common.by import By


class BaseLocators:
    LOGO_LOCATOR = (By.XPATH, '//a[@class="head-module-logoLink-3H7E6Y head-module-myTargetLogo-nNkxeR"]')
    CAMPAIGNS_LOCATOR = (By.XPATH, '//li[@class="center-module-buttonWrap-D2syOt"]/a[@href="/campaigns/list"]')
    AUDS_LOCATOR = (By.XPATH, '//li[@class="center-module-buttonWrap-D2syOt"]/a[@href="/segments"]')


class LoginPageLocators(BaseLocators):
    LOGIN_BUTTON = (By.XPATH, '//div[@class="responseHead-module-button-1BMAy4"]')
    LOGIN_FIELD = (By.XPATH, '//input[@name="email"]')
    PASSWD_FIELD = (By.XPATH, '//input[@name="password"]')
    ENTER_BUTTON = (By.XPATH, '//div[@class="authForm-module-button-2G6lZu"]')


class MainPageLocators(BaseLocators):
    EMPTY_CAMPAIGNS = (By.XPATH, '//span[@class="empty-table-data-message__text"]')
    CREATE_CAMPAIGN = (By.XPATH, '//span[@class="empty-table-data-message__text"]/a')
    TOGGLE_BOX = (By.XPATH, '//span[@class="toggle__box-wrap js-button-toggle-checkbox-wrap _checked"]')
    RELOAD_BUTTON = (By.XPATH, '//button[@class="button button_reload button_general"]')
    S_CHEGO_NACHAT = (By.XPATH, '//div[@class="instruction__title js-instruction-title"]')
    CREATE_SEGMENT = (By.XPATH, '//a[@href="/segments/segments_list/new"]')
    LIST_OF_SEGMENTS = (By.XPATH, '//div[@class="page_segments__title js-title"]')
    SEGMENT_NAME = (By.XPATH, '//span[@data-field="name"]')
    DELETE_SEGMENT = (By.XPATH, '//button[@class="button button_confirm-remove button_general"]')
    BANNER_LOCATOR = (By.XPATH, '//a[@href="/banners"]')
    BANNER_CHECKBOX = (By.XPATH, '//input[@class="flexi-table-nt__header__checkbox js-flexi-table_header_checkbox"]')
    BANNER_ACTIONS = (
        By.XPATH, '//span[@class="drop-down-list__button drop-down-list__button_tbl-actions js-drop-down-button"]')
    BANNER_DELETE = (By.XPATH, '//div[@data-test="ARCHIVE"]')

    @staticmethod
    def cross_segment(name):
        return By.XPATH, f'//a[contains(text(), "{name}")]/ancestor::tr//span[@class="icon-cross"]'


class ErrorLoginPageLocators(BaseLocators):
    ERROR_LOCATOR = (By.XPATH, '//div[@class="formMsg_title"]')


class CreateCampaignPageLocators(BaseLocators):
    TRAFFIC_LOCATOR = (By.XPATH, '//div[@class="column-list-item _traffic"]')
    ENTER_LINK = (By.XPATH, '//input[@class="input__inp js-form-element" and @maxlength="1000"]')
    BUDGET_LOCATOR = (By.XPATH, '//div[@class="progress__item-text" and @title="Бюджет: бюджет не ограничен"]')
    BUDGET_PER_DAY_FIELD = (By.XPATH, '//div[@class="input__wrap"]/input[@data-test="budget-per_day"]')
    BUDGET_OVERALL_FIELD = (By.XPATH, '//div[@class="input__wrap"]/input[@data-test="budget-total"]')
    FORMAT_REKLAMY_LOCATOR = (By.XPATH, '//div[@class="progress__item-text" and @title="Формат рекламы"]')
    BANNER_LOCATOR = (By.XPATH, '//div[@id="192"]')
    HISTOGRAM_LOCATOR = (By.XPATH, '//div[@class="price-slider-setting__btn icon-hysto js-price-slider-icon"]')
    CREATE_ADVERT_LOCATOR = (By.XPATH, '//div[@class="progress__item-text" and @title="Создание объявлений"]')
    CLOSE_MEDIA = (By.XPATH, '//div[@data-test="button-hide-medialib"]')
    UPLOAD_IMAGE_BUTTON = (By.XPATH, '//input[@class="input__inp input__inp_file js-form-element"]')
    SAVE_IMAGE_BUTTON = (By.XPATH, '//input[@class="image-cropper__save js-save"]')
    ADD_ADVERT_BUTTON = (By.XPATH, '//span[@class="js-banner-form-btn"]//div')
    CREATE_BUTTON = (By.XPATH, '//div[@class="footer__buttons-wrap"]/div')


class CreateSegmentPageLocators(BaseLocators):
    ADD_SEGMENT = (
        By.XPATH, '//div[@class="create-segment-form__block create-segment-form__block_add js-add-segments-button"]')
    CHECK_BOX = (By.XPATH, '//input[@class="adding-segments-source__checkbox js-main-source-checkbox"]')
    SUBMIT_BUTTON = (By.XPATH, '//div[@class="adding-segments-modal__btn-wrap js-add-button"]')
    NAME_FIELD = (By.XPATH, '//input[@class="input__inp js-form-element" and @maxlength="60"]')
    CREATE_SEGMENT = (By.XPATH, '//button[@class="button button_submit"]')
