import re
from datetime import datetime
from enum import Enum

TAB = "\t"
EMPTY_STR = ""
BREAK_LINE = "\n"
PUBLISH_DATE_FORMAT = "%d/%m/%Y"


class MedicinePathEnum(Enum):
    NAME = "td[1]/text()"
    ANVISA_ID = EMPTY_STR
    COMPANY = "td[2]/text()"
    PUBLISH_DATE = "td[4]/text()"
    EXPEDIENT_NUMBER = "td[3]/text()"
    LEAFLET_PATIENT_ID = "td[5]/a/@onclick"
    LEAFLET_PROFESSIONAL_ID = "td[6]/a/@onclick"

    def __str__(self):
        return self.name.lower()


class MedicineBuilder:

    def __init__(self, row):
        self._row = row
        self._medicine = {'leaflet': {}}

    def _name(self):
        field = MedicinePathEnum.NAME
        self._medicine[str(field)] = self._row.xpath(field.value).extract()[0]\
            .replace("\r", EMPTY_STR).replace(BREAK_LINE, EMPTY_STR) \
            .replace(BREAK_LINE, EMPTY_STR).replace(TAB, EMPTY_STR).capitalize()
        return self

    def _company(self):
        field = MedicinePathEnum.COMPANY
        self._medicine[str(field)] = self._row.xpath(field.value).extract()[0].replace("\r", EMPTY_STR).replace(BREAK_LINE, EMPTY_STR) \
            .replace(BREAK_LINE, EMPTY_STR).replace(TAB, EMPTY_STR).capitalize()
        return self

    def _expedient_number(self):
        field = MedicinePathEnum.EXPEDIENT_NUMBER
        self._medicine[str(field)] = self._row.xpath(field.value).extract()[0].replace("\r", EMPTY_STR)\
            .replace(BREAK_LINE, EMPTY_STR) \
            .replace(BREAK_LINE, EMPTY_STR).replace(TAB, EMPTY_STR).capitalize()
        return self

    def _publish_date(self):
        field = MedicinePathEnum.PUBLISH_DATE
        publish_date = self._row.xpath(field.value).extract()[0].replace("\r", EMPTY_STR)\
            .replace(BREAK_LINE, EMPTY_STR) \
            .replace(BREAK_LINE, EMPTY_STR).replace(TAB, EMPTY_STR).capitalize()
        self._medicine[str(field)] = str(datetime.strptime(publish_date, PUBLISH_DATE_FORMAT))
        return self

    def _anvisa_id(self):
        field = MedicinePathEnum.LEAFLET_PATIENT_ID
        leaflet_patient_ids = self._row.xpath(field.value).extract()[0]
        patient_ids = re.search("[0-9]+.*[0-9]+", leaflet_patient_ids).group().replace("'", EMPTY_STR).split(",")
        self._medicine[str(MedicinePathEnum.ANVISA_ID)] = patient_ids[0].strip()
        return self

    def _leaflet_patient_id(self):
        field = MedicinePathEnum.LEAFLET_PATIENT_ID
        leaflet_patient_ids = self._row.xpath(field.value).extract()[0]
        patient_ids = re.search("[0-9]+.*[0-9]+", leaflet_patient_ids).group().replace("'", EMPTY_STR).split(",")
        if len(patient_ids) > 1:
            self._medicine['leaflet'][str(field)] = patient_ids[1].strip()
        return self

    def _leaflet_professional_id(self):
        field = MedicinePathEnum.LEAFLET_PROFESSIONAL_ID
        leaflet_professionals_ids = self._row.xpath(field.value).extract()[0]
        professionals_ids = re.search("[0-9]+.*[0-9]+", leaflet_professionals_ids).group().replace("'", EMPTY_STR).split(",")
        if len(professionals_ids) > 1:
            self._medicine['leaflet'][str(field)] = professionals_ids[1].strip()
        return self

    def build(self):
        return self._anvisa_id()._company()._expedient_number()\
            ._leaflet_patient_id()._leaflet_professional_id()\
            ._name()._publish_date()._medicine
