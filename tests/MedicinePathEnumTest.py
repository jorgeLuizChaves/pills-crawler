import unittest

from pills_crawler.helper.medicine_builder import MedicinePathEnum


class MedicinePathEnumTest(unittest.TestCase):

    def setUp(self) -> None:
        self.expected_fields = [{'field': 'name', 'value': 'td[1]/text()'},
                           {'field': 'company', 'value': 'td[2]/text()'},
                           {'field': 'publish_date', 'value': 'td[4]/text()'},
                           {'field': 'anvisa_id', 'value': 'td[5]/a/@onclick'},
                           {'field': 'expedient_number', 'value': 'td[3]/text()'}]

    def test_fields(self):
        cont = 0
        for field in MedicinePathEnum:
            expected_field = self.expected_fields[cont]
            self.assertEqual(expected_field.get('field'), str(field))
            cont += 1


if __name__ == '__main__':
    unittest.main()
