package br.gov.ibge.geodesia.sadgeo.dashboard.component;

import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.PainelResumoDTO;

public class ResumoCardsComponent extends VerticalLayout {

	/**
	 * 
	 */
	private static final long serialVersionUID = -6238566993534162461L;

	public ResumoCardsComponent(PainelResumoDTO dto) {

		setPadding(false);
		setSpacing(false);
		setWidthFull();

		HorizontalLayout linhaPrincipal = new HorizontalLayout();
		linhaPrincipal.setWidthFull();

		HorizontalLayout linhaDetalhe = new HorizontalLayout();
		linhaDetalhe.setWidthFull();

		linhaPrincipal.add(

				new StatusCard(StatusPainel.TOTAL, dto.total()),

				new StatusCard(StatusPainel.NAO_CRITICADO, dto.naoCriticado()),

				new StatusCard(StatusPainel.CRITICADO_GGC, dto.criticadoCampo()),

				new StatusCard(StatusPainel.CRITICADO_PROJ, dto.criticadoProjeto()),

				new StatusCard(StatusPainel.ATUALIZADO_BDG, dto.atualizadoBdg())

		);

		linhaDetalhe.add(

				new StatusCard(StatusPainel.RETIDO_GGC, dto.retidoCampo()),

				new StatusCard(StatusPainel.LIBERADO_GGC, dto.liberadoCampo()),

				new StatusCard(StatusPainel.RETIDO_PROJ, dto.retidoProjeto()),

				new StatusCard(StatusPainel.LIBERADO_PROJ, dto.liberadoProjeto()),

				new StatusCard(StatusPainel.RESERVADO_GABINETE, dto.reservadoGabinete())

		);

		add(linhaPrincipal, linhaDetalhe);
		
	}

}
