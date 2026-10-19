package br.gov.ibge.geodesia.sadgeo.olap;

import tech.tablesaw.aggregate.AggregateFunctions;
import tech.tablesaw.aggregate.NumericAggregateFunction;

public enum Medida {

	CONTAGEM("contagem", AggregateFunctions.sum),

	DIAS_ENTRADA("diasAteEntrada", AggregateFunctions.mean),

	DIAS_CRITICA("diasAteCritica", AggregateFunctions.mean),

	DIAS_PUBLICACAO("diasAtePublicacao", AggregateFunctions.mean);

	private final String coluna;
	private final NumericAggregateFunction formula;

	Medida(String coluna, NumericAggregateFunction formula) {
		this.coluna = coluna;
		this.formula = formula;
	}

	public String coluna() {
		return coluna;
	}

	public NumericAggregateFunction getFormula() {
		return formula;
	}
}