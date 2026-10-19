package br.gov.ibge.geodesia.sadgeo.common.component;

import java.util.UUID;

import com.vaadin.flow.component.AttachEvent;
import com.vaadin.flow.component.dependency.CssImport;
import com.vaadin.flow.component.dependency.JavaScript;
import com.vaadin.flow.component.html.Div;

@JavaScript("./js/echarts.min.js")
@JavaScript("./js/echarts-helper.js")
@CssImport("./css/echarts-sadgeo.css")
public class EchartsComponent extends Div {

	private static final long serialVersionUID = 1L;

	private final String chartId;

	private String optionJson;

	private final Div chartDiv;

	public EchartsComponent(String optionJson) {

		this.chartId = "chart-" + UUID.randomUUID();
		this.optionJson = optionJson;

		setWidthFull();
		addClassName("echarts-component");

		chartDiv = new Div();
		chartDiv.setId(chartId);
		chartDiv.addClassName("echarts-container");
		chartDiv.setWidthFull();

		add(chartDiv);

	}

	@Override
	protected void onAttach(AttachEvent attachEvent) {
		inicializarGrafico();
	}

	private void inicializarGrafico() {
		System.out.println(optionJson);

		getElement().executeJs("""
				window.SadgeoCharts.init(
				    $0,
				    $1
				);
				""", chartId, optionJson);

	}

	public void setOption(String optionJson) {

		this.optionJson = optionJson;

		getElement().executeJs("""
				console.log("TIPO", typeof $1);
				console.log($1);
				window.SadgeoCharts.update(
				    $0,
				    $1
				);
				""", chartId, optionJson);
	}
}
