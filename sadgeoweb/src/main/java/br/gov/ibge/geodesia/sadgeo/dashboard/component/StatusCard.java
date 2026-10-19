package br.gov.ibge.geodesia.sadgeo.dashboard.component;

import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.shared.Tooltip;

public class StatusCard extends HorizontalLayout {

	private static final long serialVersionUID = 1L;

	public StatusCard(StatusPainel status, Long valor) {
		this(status, String.valueOf(valor));
	}

	public StatusCard(StatusPainel status, String valor) {

		setWidth("220px");

		getStyle().set("background", status.getCor()).set("color", "white").set("border-radius", "12px").set("padding",
				"15px");

		Span nome = new Span(status.getTitulo());

		Span numero = new Span(valor);

		nome.getStyle().set("font-weight", "bold").set("color", "white");

		numero.getStyle().set("background", "white").set("color", status.getCor()).set("padding", "2px 12px")
				.set("border-radius", "999px").set("font-weight", "bold");

		setAlignItems(Alignment.CENTER);

		setSpacing(true);

		getStyle().set("background", status.getCor()).set("padding", "4px 10px").set("border-radius", "8px")
				.set("min-width", "180px").set("justify-content", "space-between")
				.set("box-shadow", "0 1px 3px rgba(0,0,0,.2)").set("cursor", "help")
				.set("transition", "transform .15s ease");

		

		add(nome, numero);

		Tooltip.forComponent(this).setText(status.getHint());
	}
}