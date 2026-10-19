package br.gov.ibge.geodesia.sadgeo.dashboard.component;

public enum StatusPainel {

	TOTAL("Total", "#000000", "Todos os registros incluídos no SADGeo."),

	NAO_CRITICADO("Não Criticado", "#ff0000", "Total de registros não criticados."),

	CRITICADO_GGC("Criticado GGC/GLC", "#800080", "Total de registros criticados/salvos pela GGC/GLC na 1ª crítica \n(somatório de retidos e liberados)."),

	RETIDO_GGC("Retido GGC/GLC", "#800080", "Total de registros criticados e salvos mas ainda não liberados para a 2ª crítica."),

	LIBERADO_GGC("Liberado GGC/GLC", "#FFC107", "Total de registros já liberados para a 2ª crítica."),

	CRITICADO_PROJ("Criticado PROJ", "#FFC107", "Total de registros que aguardam ou já passaram pela 2ª crítica \n(somatório de retidos e liberados)."),

	RETIDO_PROJ("Retido PROJ", "#FF9800", "Total de registros que ainda não foram liberados pela 2ª crítica para carga no BDG."),

	LIBERADO_PROJ("Liberado PROJ", "#008000", "Os registros já podem ser submetidos à carga no BDG"),

	ATUALIZADO_BDG("Atualizado BDG", "#0000ff", "Registros que já foram atualizados no BDG."),

	RESERVADO_GABINETE("Reservado GAB", "#6c757d", "Registros reservados pelo Gabinete/PROJETO");

	/*
	 *Status  Cor
	 *Total⚫ Preto
	 *Não Criticado🔴 Vermelho
	 *Retido GGC🟣 Roxo
	 *Liberado GGC🟡 Amarelo
	 *Criticado GGC🟡 Amarelo
	 *Retido PROJ🟠 Laranja
	 *Liberado PROJ🟢 Verde
	 *Criticado PROJ🟢 Verde
	 *Atualizado BDG🔵 Azul
	 *Reservado Gabinete⚪ Cinza
	 */
	private final String titulo;
	private final String cor;
	private final String hint;

	StatusPainel(String titulo, String cor, String hint) {

		this.titulo = titulo;
		this.cor = cor;
		this.hint = hint;
	}

	public String getTitulo() {
		return titulo;
	}

	public String getCor() {
		return cor;
	}

	public String getHint() {
		return hint;
	}
}