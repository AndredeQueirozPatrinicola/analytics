from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Docente(models.Model):
    docente_id = models.CharField(max_length=255)
    api_docente = models.JSONField()                                            # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                          # https://dados.fflch.usp.br/api/programas
    api_docentes = models.JSONField(null=True)                                  # https://dados.fflch.usp.br/api/docentes

    def __str__(self):
        return self.docente_id
 
 
class Departamento(models.Model):
    sigla = models.CharField(max_length=10)
    api_docentes = models.JSONField()                                             # https://dados.fflch.usp.br/api/docente
    api_programas = models.JSONField()                                           # https://dados.fflch.usp.br/api/programas
    api_programas_docente = models.JSONField()
    api_pesquisa = models.JSONField()  
    api_pesquisa_parametros = models.JSONField()                                # https://dados.fflch.usp.br/api/pesquisa + 'filtro=departamento&ano_ini=&ano_fim=&serie_historica_tipo='
    api_programas_docente_limpo = models.JSONField(null=True)
    api_defesas = models.JSONField(null=True)

    def __str__(self):
        return self.sigla


class Mapa(models.Model):
    nome = models.CharField(max_length=255)
    base_de_dados = models.JSONField(null=True)
    dados_do_mapa = models.JSONField(null=True)

    def __str__(self) -> str:
        return self.nome