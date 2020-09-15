import unittest

from pills_crawler.helper.medicine_builder import MedicineBuilder


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._row = """
        <tr bgcolor="#E0E0E0" class="">
				<td height="35px" class="">
					A SAÚDE DA MULHER
				</td>
				<td height="35px" class="">
					EMS S/A
				</td>
				<td height="35px" class="">
					0500912/14-0
				</td>
				<td height="35px" class="">
					25/06/2014
				</td>
				<td height="35px" class="">
					<a title="Clique para visualizar a Bula de Paciente" href="#" onclick="fVisualizarBula('5382372014', '2111405')">
						<img style="border-style:none" src="imagens/pdf.png" width="24" height="24">
					</a>
				</td>
				<td height="35px" class="">
					<a title="Clique para visualizar a Bula de Paciente" href="#" onclick="fVisualizarBula('5382372014', '2111416')">
						<img style="border-style:none" src="imagens/pdf.png" width="24" height="24">
					</a>
				</td>
			</tr>
        """

    def test_something(self):
        builder = MedicineBuilder(row=self._row)
        obj = builder.build()
        self.assertEqual("", obj.get('name'))


if __name__ == '__main__':
    unittest.main()
