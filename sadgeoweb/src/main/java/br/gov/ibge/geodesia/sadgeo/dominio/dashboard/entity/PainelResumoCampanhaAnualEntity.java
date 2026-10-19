package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity;

import java.time.LocalDate;

import org.hibernate.annotations.Immutable;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.EvolucaoAnualCampanhaProjetoUfDTO;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Immutable
@Table(name = "V_SADGEO_PAINEL_RESUMO_CAMPANHA_ANUAL", schema = "BDG_VALIDA")
public class PainelResumoCampanhaAnualEntity {

	@Id
	@Column(name = "ID")
	private Long id;

	@Column(name = "ANO")
	private Integer ano;

	@Column(name = "CAMPANHA")
	private String campanha;

	@Column(name = "PROJETO")
	private String projeto;

	@Column(name = "UF")
	private String uf;

	@Column(name = "TOTAL", columnDefinition = "NUMBER")
	private Long total;

	@Column(name = "NAO_CRITICADO", columnDefinition = "NUMBER")
	private Long naoCriticado;

	@Column(name = "RETIDO_CAMPO", columnDefinition = "NUMBER")
	private Long retidoCampo;

	@Column(name = "LIBERADO_CAMPO", columnDefinition = "NUMBER")
	private Long liberadoCampo;

	@Column(name = "CRITICADO_CAMPO", columnDefinition = "NUMBER")
	private Long criticadoCampo;

	@Column(name = "RETIDO_PROJETO", columnDefinition = "NUMBER")
	private Long retidoProjeto;

	@Column(name = "CRITICADO_PROJETO", columnDefinition = "NUMBER")
	private Long criticadoProjeto;

	@Column(name = "LIBERADO_PROJETO", columnDefinition = "NUMBER")
	private Long liberadoProjeto;

	@Column(name = "ATUALIZADO_BDG", columnDefinition = "NUMBER")
	private Long atualizadoBdg;

	@Column(name = "RESERVADO_GABINETE", columnDefinition = "NUMBER")
	private Long reservadoGabinete;

	@Column(name = "DATA_PRIMEIRO_LEVANTAMENTO", columnDefinition = "DATE")
	private LocalDate dtPrimeiroLevantamento;

	@Column(name = "DATA_ULTIMO_LEVANTAMENTO", columnDefinition = "DATE")
	private LocalDate dtUltimoLevantamento;

	public Long getTotal() {
		return total;
	}

	public void setTotal(Long total) {
		this.total = total;
	}

	public Long getNaoCriticado() {
		return naoCriticado;
	}

	public void setNaoCriticado(Long naoCriticado) {
		this.naoCriticado = naoCriticado;
	}

	public Long getRetidoCampo() {
		return retidoCampo;
	}

	public void setRetidoCampo(Long retidoCampo) {
		this.retidoCampo = retidoCampo;
	}

	public Long getLiberadoCampo() {
		return liberadoCampo;
	}

	public void setLiberadoCampo(Long liberadoCampo) {
		this.liberadoCampo = liberadoCampo;
	}

	public Long getCriticadoCampo() {
		return criticadoCampo;
	}

	public void setCriticadoCampo(Long criticadoCampo) {
		this.criticadoCampo = criticadoCampo;
	}

	public Long getRetidoProjeto() {
		return retidoProjeto;
	}

	public void setRetidoProjeto(Long retidoProjeto) {
		this.retidoProjeto = retidoProjeto;
	}

	public Long getCriticadoProjeto() {
		return criticadoProjeto;
	}

	public void setCriticadoProjeto(Long criticadoProjeto) {
		this.criticadoProjeto = criticadoProjeto;
	}

	public Long getLiberadoProjeto() {
		return liberadoProjeto;
	}

	public void setLiberadoProjeto(Long liberadoProjeto) {
		this.liberadoProjeto = liberadoProjeto;
	}

	public Long getAtualizadoBdg() {
		return atualizadoBdg;
	}

	public void setAtualizadoBdg(Long atualizadoBdg) {
		this.atualizadoBdg = atualizadoBdg;
	}

	public Long getReservadoGabinete() {
		return reservadoGabinete;
	}

	public void setReservadoGabinete(Long reservadoGabinete) {
		this.reservadoGabinete = reservadoGabinete;
	}



	public EvolucaoAnualCampanhaProjetoUfDTO toDTO() {

		return new EvolucaoAnualCampanhaProjetoUfDTO(

				campanha,

				uf,

				projeto,

				ano,

				total,

				naoCriticado,

				retidoCampo,

				liberadoCampo,

				criticadoCampo,

				retidoProjeto,

				liberadoProjeto,

				criticadoProjeto,

				atualizadoBdg,

				reservadoGabinete,

				dtPrimeiroLevantamento,

				dtUltimoLevantamento

		);
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Integer getAno() {
		return ano;
	}

	public void setAno(Integer ano) {
		this.ano = ano;
	}

	public String getCampanha() {
		return campanha;
	}

	public void setCampanha(String campanha) {
		this.campanha = campanha;
	}

	public String getProjeto() {
		return projeto;
	}

	public void setProjeto(String projeto) {
		this.projeto = projeto;
	}

	public String getUf() {
		return uf;
	}

	public void setUf(String uf) {
		this.uf = uf;
	}

	public LocalDate getDtPrimeiroLevantamento() {
		return dtPrimeiroLevantamento;
	}

	public void setDtPrimeiroLevantamento(LocalDate dtPrimeiroLevantamento) {
		this.dtPrimeiroLevantamento = dtPrimeiroLevantamento;
	}

	public LocalDate getDtUltimoLevantamento() {
		return dtUltimoLevantamento;
	}

	public void setDtUltimoLevantamento(LocalDate dtUltimoLevantamento) {
		this.dtUltimoLevantamento = dtUltimoLevantamento;
	}
}