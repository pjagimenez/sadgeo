package br.gov.ibge.geodesia.sadgeo.template.menu;

import java.util.ArrayList;
import java.util.List;

import br.gov.ibge.geodesia.sadgeo.dashboard.DashboardView;
import br.gov.ibge.geodesia.sadgeo.view.pagina.AdministracaoView;
import br.gov.ibge.geodesia.sadgeo.view.pagina.AnaliseAltimetriaView;
import br.gov.ibge.geodesia.sadgeo.view.pagina.HomologacaoMarcoView;
import br.gov.ibge.geodesia.sadgeo.view.pagina.LevantamentoAltimetriaView;
import br.gov.ibge.geodesia.sadgeo.view.pagina.RelatoriosView;

public class MenuBuilder {

	private static MenuItem obterMenuLevantamento() {
		MenuItem levantamento = new MenuItem("Levantamento de Campo");

		levantamento.add(new MenuItem("Altimetria", LevantamentoAltimetriaView.class));
		/*
		 * levantamento.add( new MenuItem( "Planimetria", PlanimetriaView.class ));
		 * 
		 * levantamento.add( new MenuItem( "Gravimetria", GravimetriaView.class ));
		 * 
		 * levantamento.add( new MenuItem( "VRF", VrfView.class ));
		 * 
		 * levantamento.add( new MenuItem( "OGR", OgrView.class ));
		 */

		return levantamento;

	}

	private static MenuItem obterMenuAnalise() {

		MenuItem analise = new MenuItem("Análise");

		analise.add(new MenuItem("Altimetria", AnaliseAltimetriaView.class));

		return analise;
	}

	private static MenuItem obterMenuRelatorio() {
		return  new MenuItem("Relatórios", RelatoriosView.class);
	}

	private static MenuItem obterMenuAdministracao() {
		return new MenuItem("Administração", AdministracaoView.class);
	}

	private static MenuItem obterMenuHomologacaoMarco() {
		return new MenuItem("Homologação Marcos", HomologacaoMarcoView.class);
		
	}
	
	public static List<MenuItem>  build() {

		List<MenuItem> menus = new ArrayList<>();

		menus.add(new MenuItem("Dashboard", DashboardView.class));

		menus.add(obterMenuLevantamento());

		menus.add(obterMenuAnalise());
		
		menus.add(obterMenuHomologacaoMarco());
		
		menus.add(obterMenuRelatorio());

		menus.add(obterMenuAdministracao());
		return menus;
	}
}
