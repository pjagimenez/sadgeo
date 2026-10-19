package br.gov.ibge.geodesia.sadgeo.dashboard.component;

import java.util.List;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.ResumoAnaliticoDTO;

public class ResumoAnaliticoGrid extends VerticalLayout {

	/**
	 * 
	 */
	private static final long serialVersionUID = -2151850385407497346L;

	public ResumoAnaliticoGrid(List<ResumoAnaliticoDTO> dados) {

		Grid<ResumoAnaliticoDTO> grid = new Grid<>(ResumoAnaliticoDTO.class, false);

		grid.addColumn(ResumoAnaliticoDTO::ano).setHeader("Ano").setSortable(true);

		grid.addColumn(ResumoAnaliticoDTO::campanha).setHeader("Campanha").setSortable(true);

		grid.addColumn(ResumoAnaliticoDTO::projeto).setHeader("Projeto").setSortable(true);

		grid.addColumn(ResumoAnaliticoDTO::uf).setHeader("UF").setSortable(true);

		grid.addColumn(ResumoAnaliticoDTO::situacao).setHeader("Situação").setSortable(true);

		grid.addColumn(ResumoAnaliticoDTO::contagem).setHeader("Quantidade").setSortable(true);

		grid.addColumn(ResumoAnaliticoDTO::mediaDiasLevantamentoAteEntrada).setHeader("Lev. → Entrada");

		grid.addColumn(ResumoAnaliticoDTO::mediaDiasEntradaAteCritica).setHeader("Entrada → Crítica");

		grid.addColumn(ResumoAnaliticoDTO::mediaDiasEntradadiasAtePublicacao).setHeader("Entrada → Publicação");

		grid.addColumn(ResumoAnaliticoDTO::mediaDiasLevantamentoAteCalculoCoordenadas).setHeader("Lev. → Cálculo");

		grid.setItems(dados);

		//grid.setSizeFull();

	}

}
