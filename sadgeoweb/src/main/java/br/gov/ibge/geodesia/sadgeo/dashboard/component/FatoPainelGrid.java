package br.gov.ibge.geodesia.sadgeo.dashboard.component;

import java.util.List;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.FatoPainelDTO;

public class FatoPainelGrid extends VerticalLayout {

	private static final long serialVersionUID = 1L;

	public FatoPainelGrid(
            List<FatoPainelDTO> dados) {

        //setSizeFull();

        Grid<FatoPainelDTO> grid =
                new Grid<>(FatoPainelDTO.class, false);

        grid.addColumn(FatoPainelDTO::anoLevantamento)
                .setHeader("Ano");

        grid.addColumn(FatoPainelDTO::campanha)
                .setHeader("Campanha");

        grid.addColumn(FatoPainelDTO::projeto)
                .setHeader("Projeto");

        grid.addColumn(FatoPainelDTO::uf)
                .setHeader("UF");

        grid.addColumn(FatoPainelDTO::municipio)
                .setHeader("Município");

        grid.addColumn(FatoPainelDTO::situacao)
                .setHeader("Situação");

        grid.setItems(dados);

        grid.setSizeFull();

        add(grid);

        expand(grid);
    }

}
