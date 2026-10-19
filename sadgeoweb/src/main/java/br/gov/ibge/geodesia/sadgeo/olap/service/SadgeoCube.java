package br.gov.ibge.geodesia.sadgeo.olap.service;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.FatoPainelDTO;
import br.gov.ibge.geodesia.sadgeo.olap.Dimensao;
import br.gov.ibge.geodesia.sadgeo.olap.Medida;
import br.gov.ibge.geodesia.sadgeo.olap.PivotTable;
import tech.tablesaw.api.IntColumn;
import tech.tablesaw.api.Row;
import tech.tablesaw.api.StringColumn;
import tech.tablesaw.api.Table;

public class SadgeoCube {

	private Table fato = Table.create("sadgeo");;

	public SadgeoCube(List<FatoPainelDTO> dados) {

		carregarFato(dados);
	}

	public void carregarFato(List<FatoPainelDTO> dados) {

		IntColumn ano = IntColumn.create("ano");

		IntColumn mes = IntColumn.create("mes");

		StringColumn campanha = StringColumn.create("campanha");

		StringColumn projeto = StringColumn.create("projeto");

		StringColumn uf = StringColumn.create("uf");

		StringColumn municipio = StringColumn.create("municipio");

		StringColumn tipoLocal = StringColumn.create("tipoLocal");

		StringColumn uorgOrigem = StringColumn.create("uorgOrigem");

		StringColumn situacao = StringColumn.create("situacao");

		IntColumn contagem = IntColumn.create("contagem");
		IntColumn diasEntrada = IntColumn.create("diasAteEntrada");
		IntColumn diasCritica = IntColumn.create("diasAteCritica");
		IntColumn diasPublicacao = IntColumn.create("diasAtePublicacao");
		IntColumn diasCalculo = IntColumn.create("diasAteCalculoCoord");

		dados.forEach(d -> {

			ano.append(nvl(d.anoLevantamento()));

			mes.append(nvl(d.mesLevantamento()));

			campanha.append(texto(d.campanha()));

			projeto.append(texto(d.projeto()));

			uf.append(texto(d.uf()));

			municipio.append(texto(d.municipio()));

			tipoLocal.append(texto(d.tipoLocal()));

			uorgOrigem.append(texto(d.uorgOrigem()));

			situacao.append(texto(d.situacao()));

			contagem.append(nvl(d.contagem()));
			diasEntrada.append(nvl(d.diasAteEntrada()));

			diasCritica.append(nvl(d.diasAteCritica()));

			diasPublicacao.append(nvl(d.diasAtePublicacao()));

			diasCalculo.append(nvl(d.diasAteCalculoCoord()));
		});

		fato.addColumns(ano, mes, campanha, projeto, uf, municipio, tipoLocal, uorgOrigem, situacao, contagem);

	}

	private Integer nvl(Integer valor) {

		return valor == null ? 0 : valor;
	}

	private String texto(String valor) {

		return valor == null ? "(não informado)" : valor;
	}

	public PivotTable pivot(Dimensao eixoX, Dimensao serie, Medida medida) {

		String x = eixoX.coluna();
		String s = serie.coluna();

		Table agregada = fato.summarize(medida.coluna(), medida.getFormula()).by(x, s);

		String colunaValor = agregada.columnNames().stream().filter(nome -> !nome.equals(x))
				.filter(nome -> !nome.equals(s)).findFirst().orElseThrow();

		List<String> categorias =

				agregada.column(x).asList().stream().map(String::valueOf).distinct().sorted().toList();

		List<String> seriesNomes =

				agregada.column(s).asList().stream().map(String::valueOf).distinct().sorted().toList();

		Map<String, List<Double>> series =

				new LinkedHashMap<>();

		for (String serieNome : seriesNomes) {

			List<Double> valores = new ArrayList<>();

			for (String categoria : categorias) {

				double valor = 0;

				for (Row row : agregada) {

					if (categoria.equals(String.valueOf(row.getObject(x)))

							&&

							serieNome.equals(String.valueOf(row.getObject(s)))) {

						valor = row.getDouble(colunaValor);

						break;
					}
				}

				valores.add(valor);
			}

			series.put(serieNome, valores);
		}

		return new PivotTable(categorias, series);

	}
}