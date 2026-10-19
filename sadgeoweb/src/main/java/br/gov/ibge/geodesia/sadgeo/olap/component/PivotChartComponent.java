package br.gov.ibge.geodesia.sadgeo.olap.component;

import java.util.stream.Collectors;

import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;

import br.gov.ibge.geodesia.sadgeo.common.component.EchartsComponent;
import br.gov.ibge.geodesia.sadgeo.olap.Dimensao;
import br.gov.ibge.geodesia.sadgeo.olap.Medida;
import br.gov.ibge.geodesia.sadgeo.olap.PivotTable;
import br.gov.ibge.geodesia.sadgeo.olap.service.SadgeoCube;

public class PivotChartComponent extends VerticalLayout {

	private static final long serialVersionUID = 1L;

	private final SadgeoCube cube;

	private final ComboBox<Dimensao> eixoX;

	private final ComboBox<Dimensao> serie;

	private ComboBox<Medida> medida;

	private final EchartsComponent chart;

	public PivotChartComponent(SadgeoCube cube, Dimensao dimEixoX, Dimensao dimSerie, Medida metrica) {

		this.cube = cube;

		setWidthFull();
		setPadding(false);

		eixoX = new ComboBox<>("Eixo X");
		eixoX.setItems(Dimensao.values());
		eixoX.setValue(dimEixoX);

		serie = new ComboBox<>("Série");
		serie.setItems(Dimensao.values());
		serie.setValue(dimSerie);
		
		medida = new ComboBox<>("Valor");
		medida.setItems( Medida.values());
		medida.setValue(metrica);
		
		chart = new EchartsComponent("{}");
		chart.setWidthFull();

		HorizontalLayout filtros = new HorizontalLayout(eixoX, serie, medida);

		add(filtros, chart);

		eixoX.addValueChangeListener(e -> atualizar());

		serie.addValueChangeListener(e -> atualizar());

		atualizar();
	}

	private void atualizar() {

		PivotTable tabela = cube.pivot(eixoX.getValue(), serie.getValue(), medida.getValue());
		chart.setOption(montarOption(tabela));
	}

	private String montarOption(PivotTable tabela) {

		String categorias = tabela.categorias().stream().map(v -> "'" + v + "'").collect(Collectors.joining(","));

		String seriesJson = tabela.series().entrySet().stream().map(entry -> {

			String valores = entry.getValue().stream().map(String::valueOf).collect(Collectors.joining(","));

			return """
					{
					    name:'%s',
					    type:'bar',
					    data:[%s]
					}
					""".formatted(entry.getKey(), valores);

		}).collect(Collectors.joining(","));

		return """
				{
				    tooltip:{
				        trigger:'axis'
				    },

				    legend:{
				        top:10
				    },

				    xAxis:{
				        type:'category',
				        data:[%s]
				    },

				    yAxis:{
				        type:'value'
				    },

				    series:[
				        %s
				    ]
				}
				""".formatted(categorias, seriesJson);
	}
}