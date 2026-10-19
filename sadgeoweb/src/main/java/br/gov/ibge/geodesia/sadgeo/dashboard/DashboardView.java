package br.gov.ibge.geodesia.sadgeo.dashboard;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;

import br.gov.ibge.geodesia.sadgeo.dashboard.component.EvolucaoAnualChart;
import br.gov.ibge.geodesia.sadgeo.dashboard.component.FatoPainelGrid;
import br.gov.ibge.geodesia.sadgeo.dashboard.component.ResumoAnaliticoGrid;
import br.gov.ibge.geodesia.sadgeo.dashboard.component.ResumoCardsComponent;
import br.gov.ibge.geodesia.sadgeo.dashboard.service.DashboardService;
import br.gov.ibge.geodesia.sadgeo.olap.Dimensao;
import br.gov.ibge.geodesia.sadgeo.olap.Medida;
import br.gov.ibge.geodesia.sadgeo.olap.component.PivotChartComponent;
import br.gov.ibge.geodesia.sadgeo.olap.service.CubeProvider;
import br.gov.ibge.geodesia.sadgeo.view.MainLayout;

@Route(value = "", layout = MainLayout.class)
@PageTitle("Dashboard")
public class DashboardView extends VerticalLayout {

	private static final long serialVersionUID = 1L;

	private EvolucaoAnualChart graficoAnual;

	// private EvolucaoCampanhaChart graficoCampanha;
	private PivotChartComponent graficoCampanha;

	private ResumoAnaliticoGrid gridAnalitico;

	private FatoPainelGrid gridFato;

	public DashboardView(DashboardService service, CubeProvider cubeProvider) {

		setSizeFull();
		setPadding(true);
		setSpacing(true);

		add(criarCabecalho(), new ResumoCardsComponent(service.obterResumoAtual()),
				// filtroComponent,
				criarLinhaGraficos(service, cubeProvider), criarLinhaGrids(service)

		);
	}

	private Component criarCabecalho() {

		VerticalLayout layout = new VerticalLayout();

		layout.setPadding(false);
		layout.setSpacing(false);

		layout.add(new H2("Painel Resumo"));

		return layout;
	}

	private Component criarLinhaGraficos(DashboardService service, CubeProvider cubeProvider) {

		HorizontalLayout linha = new HorizontalLayout();

		linha.setWidthFull();

		graficoAnual = new EvolucaoAnualChart(service.obterEvolucaoAnual());

		// graficoCampanha = new
		// EvolucaoCampanhaChart(service.obterEvolucaoCampanhaAnual());
		graficoCampanha = new PivotChartComponent(cubeProvider.getCube(), Dimensao.ANO, Dimensao.CAMPANHA, Medida.CONTAGEM);

		graficoAnual.setWidthFull();
		graficoCampanha.setWidthFull();

		linha.add(graficoAnual, graficoCampanha);

		linha.expand(graficoAnual, graficoCampanha);

		return linha;
	}

	private Component criarLinhaGrids(DashboardService service) {

		HorizontalLayout linha = new HorizontalLayout();

		linha.setWidthFull();

		gridAnalitico = new ResumoAnaliticoGrid(service.obterResumoAnalitico());

		gridFato = new FatoPainelGrid(service.obterFatoPainel());

		gridAnalitico.setWidthFull();
		gridFato.setWidthFull();

		linha.add(gridAnalitico, gridFato);

		linha.expand(gridAnalitico, gridFato);

		return linha;
	}
}
