import unittest
from app import run
class Pesquisa(unittest.TestCase):
    def test_indexacao(self):
        data=dict(autor="Autor",obra="Obra",edicao="1",ano=2020,pagina_inicial=1,referencia="Jo 15",parafrase="Texto",avaliacao="Avaliação",palavras_chave=["fé","fé","graça"],questoes=["Como aplicar?"])
        result=run(data)
        self.assertEqual(result["palavras_chave"],["fé","graça"])
        self.assertIn("## Questões de pesquisa",result["markdown"])
        data["questoes"]="inválido"
        with self.assertRaises(ValueError): run(data)
