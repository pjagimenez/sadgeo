from dataclasses import asdict, replace
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image
import pytest

from sidgeo.application.controller_fabrica import ControllerFactory
from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.foto import LIMITE_FOTO
from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.domain.tratamento_foto import AjusteFoto, renderizar_foto


@pytest.fixture
def imagem(tmp_path):
    arquivo = tmp_path / 'panoramica.png'
    Image.new('RGB', (1600, 1200), (10, 80, 100)).save(arquivo)
    return arquivo


def test_fotos_copia_deduplicacao_e_limite(controller, imagem, tmp_path):
    primeira = controller.adicionar_foto(str(imagem), 'panoramica')
    segunda = controller.adicionar_foto(str(imagem), 'chapa')
    assert primeira.arquivo == segunda.arquivo
    assert Path(controller.caminho_foto(primeira)).read_bytes() == imagem.read_bytes()
    assert imagem.exists()
    grande = tmp_path / 'grande.jpg'
    grande.write_bytes(b'x' * (LIMITE_FOTO + 1))
    with pytest.raises(ValidacaoErro, match='5 MB'):
        controller.adicionar_foto(str(grande), 'panoramica')
    falsa = tmp_path / 'falsa.jpg'
    falsa.write_bytes(b'nao e uma imagem')
    with pytest.raises(ValidacaoErro, match='imagem'):
        controller.adicionar_foto(str(falsa), 'chapa')


@pytest.mark.parametrize('formato', ['csv', 'json', 'zip'])
def test_foto_metadata_e_unidade_roundtrip(controller, imagem, tmp_path, logger, formato):
    foto = controller.adicionar_foto(str(imagem), 'panoramica')
    reg = RegistroFabrica.criar(dict(cod_estacao='422V', informante='nome.sobrenome',
                                  unidade_informante='SES-GO/GGC', fotos=[foto]))
    controller.salvar_registro(reg)
    arquivo = tmp_path / f'exportado.{formato}'
    controller.exportar(str(arquivo), formato)
    destino = ControllerFactory.criar(logger, data_dir=tmp_path / 'outro_perfil' / 'SIDGEO')
    assert destino.importar(str(arquivo), formato) == 1
    assert asdict(destino.buscar_registro('422V')) == asdict(reg)
    if formato == 'zip':
        assert Path(destino.caminho_foto(foto)).read_bytes() == imagem.read_bytes()
        with ZipFile(arquivo) as pacote:
            assert {'sidgeo.h5', 'registros.csv', 'registros.json', f'imagens/{foto.arquivo}'} <= set(pacote.namelist())
    else:
        with pytest.raises(ValidacaoErro, match='ZIP'):
            destino.caminho_foto(foto)


def test_ajustes_preservam_proporcao_original_e_reedicao(controller, imagem, tmp_path, logger):
    foto = controller.adicionar_foto(str(imagem), 'panoramica')
    original = imagem.read_bytes()
    ajuste = AjusteFoto(codigo='422V')
    renderizada = renderizar_foto(original, ajuste)
    assert renderizada.size == (640, 480)
    assert renderizada.getpixel((370, 280)) != (10, 80, 100)
    tratada = controller.tratar_foto(foto, ajuste)
    assert tratada.arquivo_original == foto.arquivo
    assert controller.original_foto(tratada) == original
    retratada = controller.tratar_foto(tratada, replace(ajuste, horizontal=100, vertical=100))
    with Image.open(controller.caminho_foto(retratada)) as img:
        assert all(valor < 150 for valor in img.getpixel((400, 287)))
    assert imagem.read_bytes() == original
    controller.salvar_registro(RegistroFabrica.criar(dict(cod_estacao='422V', fotos=[retratada])))
    pacote = tmp_path / 'completo.zip'
    controller.exportar(str(pacote), 'zip')
    destino = ControllerFactory.criar(logger, data_dir=tmp_path / 'destino')
    destino.importar(str(pacote), 'zip')
    carregada = destino.buscar_registro('422V').fotos[0]
    assert destino.original_foto(carregada) == original
    assert destino.tratar_foto(carregada, ajuste).arquivo == tratada.arquivo


def test_ajuste_vertical_e_etiqueta_fora_da_foto():
    buffer = BytesIO()
    Image.new('RGB', (1200, 1600)).save(buffer, 'PNG')
    dados = buffer.getvalue()
    assert renderizar_foto(dados, AjusteFoto(codigo='422V', horizontal=20, vertical=20)).size == (360, 480)
    with pytest.raises(ValidacaoErro, match='caber'):
        renderizar_foto(dados, AjusteFoto(codigo='422V', horizontal=500))


def test_zip_adulterado_nao_importa_registros(controller, imagem, tmp_path):
    foto = controller.adicionar_foto(str(imagem), 'chapa')
    reg = RegistroFabrica.criar(dict(cod_estacao='422V', fotos=[foto]))
    registro = asdict(reg)
    pacote = tmp_path / 'adulterado.zip'
    with ZipFile(pacote, 'w') as arquivo:
        arquivo.writestr('registros.json', json.dumps([registro], default=str))
        arquivo.writestr(f'imagens/{foto.arquivo}', b'conteudo adulterado')
        arquivo.writestr('../fora.txt', b'nao extrair')
    with pytest.raises(ValidacaoErro, match='Integridade'):
        controller.importar(str(pacote), 'zip')
    assert controller.listar_registros() == []
    assert not (tmp_path.parent / 'fora.txt').exists()
