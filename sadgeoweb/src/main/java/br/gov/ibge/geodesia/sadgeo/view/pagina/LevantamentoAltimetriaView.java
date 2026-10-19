package br.gov.ibge.geodesia.sadgeo.view.pagina;

import com.vaadin.flow.component.html.H1;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.Route;

import br.gov.ibge.geodesia.sadgeo.view.MainLayout;

@Route(value = "levantamento/altimetria", layout = MainLayout.class)
public class LevantamentoAltimetriaView extends VerticalLayout {

	/**
	* 
	*/
	private static final long serialVersionUID = -7424225239904092206L;

	public LevantamentoAltimetriaView() {
		add(new H1("Altimetria"));
	}
}