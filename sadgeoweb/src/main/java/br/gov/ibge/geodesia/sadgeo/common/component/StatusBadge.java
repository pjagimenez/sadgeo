package br.gov.ibge.geodesia.sadgeo.common.component;

import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;

public class StatusBadge extends HorizontalLayout {

    /**
	 * 
	 */
	private static final long serialVersionUID = -7210615489599450807L;

	public StatusBadge(
            String titulo,
            String valor,
            String corFundo) {

        Span label = new Span(titulo);

        Span badge = new Span(valor);

        badge.getStyle()
                .set("background", "white")
                .set("color", corFundo)
                .set("padding", "2px 12px")
                .set("border-radius", "15px")
                .set("font-weight", "bold");

        setAlignItems(Alignment.CENTER);

        getStyle()
            .set("background", corFundo)
            .set("color", "white")
            .set("padding", "4px 8px")
            .set("border-radius", "8px")
            .set("font-weight", "bold");

        add(label, badge);
    }
}