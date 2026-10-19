package br.gov.ibge.geodesia.sadgeo.dashboard.component;

import java.util.List;
import java.util.stream.Collectors;

import br.gov.ibge.geodesia.sadgeo.common.component.AbstractChartComponent;
import br.gov.ibge.geodesia.sadgeo.dashboard.dto.EvolucaoAnualDTO;

public class EvolucaoAnualChart  extends AbstractChartComponent<EvolucaoAnualDTO> {

	private static final long serialVersionUID = 1L;

	public EvolucaoAnualChart(List<EvolucaoAnualDTO> dados) {
		super(dados);		
	}

	@Override
	protected String montarOption(List<EvolucaoAnualDTO> dados) {

		String anos = dados.stream().map(d -> "'" + d.ano() + "'").collect(Collectors.joining(","));

		String naoCriticado = dados.stream().map(d -> String.valueOf(d.naoCriticado()))
				.collect(Collectors.joining(","));

		String retidoGgc = dados.stream().map(d -> String.valueOf(d.retidoCampo())).collect(Collectors.joining(","));

		String liberadoGgc = dados.stream().map(d -> String.valueOf(d.liberadoCampo()))
				.collect(Collectors.joining(","));

		String retidoProj = dados.stream().map(d -> String.valueOf(d.retidoProjeto())).collect(Collectors.joining(","));

		String liberadoProj = dados.stream().map(d -> String.valueOf(d.liberadoProjeto()))
				.collect(Collectors.joining(","));

		String reservado = dados.stream().map(d -> String.valueOf(d.reservadoGabinete()))
				.collect(Collectors.joining(","));

		String atualizado = dados.stream().map(d -> String.valueOf(d.atualizadoBdg())).collect(Collectors.joining(","));

		String option = """
				{
				  tooltip: {
				      trigger: 'axis'
				  },


				  legend: {
				      top: 10
				  },


				  xAxis: {
				      type: 'category',
				      data: [%s]
				  },


				  yAxis: {
				      type: 'value'
				  },


				  series: [


				     {
				         name:'Não Criticado',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#ff0000'},
				         data:[%s]
				     },


				     {
				         name:'Retido GGC',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#800080'},
				         data:[%s]
				     },


				     {
				         name:'Liberado GGC',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#ffc107'},
				         data:[%s]
				     },


				     {
				         name:'Retido PROJ',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#ff9800'},
				         data:[%s]
				     },


				     {
				         name:'Liberado PROJ',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#008000'},
				         data:[%s]
				     },


				     {
				         name:'Reservado',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#6c757d'},
				         data:[%s]
				     },


				     {
				         name:'Atualizado BDG',
				         type:'bar',
				         stack:'total',
				         itemStyle:{color:'#0000ff'},
				         data:[%s]
				     }


				  ]
				}
				""".formatted(anos, naoCriticado, retidoGgc, liberadoGgc, retidoProj, liberadoProj, reservado,
				atualizado);
		return option;

	}
}
