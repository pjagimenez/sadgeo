package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.ResumoAnaliticoDTO;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "V_SADGEO_PAINEL_RESUMO_ANALITICO", schema = "BDG_VALIDA")
public class PainelResumoAnaliticoEntity {

	@Id
	@Column(name = "Id")
	private Long id;

	@Column(name = "ANO")
	private Integer ano;

	@Column(name = "CAMPANHA")
	private String campanha;

	@Column(name = "PROJETO")
	private String projeto;

	@Column(name = "UF")
	private String uf;

	@Column(name = "SITUACAO")
	private String situacao;

	@Column(name = "QUANTIDADE", columnDefinition = "NUMBER")
	private Long criticadoCampo;

	@Column(name = "MEDIA_DIAS_ENTRADA", columnDefinition = "NUMBER")
	private Long mediaDiasEntrada;

	@Column(name = "MEDIA_DIAS_CRITICA", columnDefinition = "NUMBER")
	private Long mediaDiasCritica;

	@Column(name = "MEDIA_DIAS_PUBLICACAO", columnDefinition = "NUMBER")
	private Long mediaDiasPublicacao;

	@Column(name = "MEDIA_DIAS_CALCULO", columnDefinition = "NUMBER")
	private Long mediaDiasCalculoCoordenada;

	public Long getCriticadoCampo() {
		return criticadoCampo;
	}

	public void setCriticadoCampo(Long criticadoCampo) {
		this.criticadoCampo = criticadoCampo;
	}

	public Long getMediaDiasEntrada() {
		return mediaDiasEntrada;
	}

	public void setMediaDiasEntrada(Long mediaDiasEntrada) {
		this.mediaDiasEntrada = mediaDiasEntrada;
	}

	public Long getMediaDiasCritica() {
		return mediaDiasCritica;
	}

	public void setMediaDiasCritica(Long mediaDiasCritica) {
		this.mediaDiasCritica = mediaDiasCritica;
	}

	public Long getMediaDiasPublicacao() {
		return mediaDiasPublicacao;
	}

	public void setMediaDiasPublicacao(Long mediaDiasPublicacao) {
		this.mediaDiasPublicacao = mediaDiasPublicacao;
	}

	public Long getMediaDiasCalculoCoordenada() {
		return mediaDiasCalculoCoordenada;
	}

	public void setMediaDiasCalculoCoordenada(Long mediaDiasCalculoCoordenada) {
		this.mediaDiasCalculoCoordenada = mediaDiasCalculoCoordenada;
	}

	public ResumoAnaliticoDTO toDTO() {

		return new ResumoAnaliticoDTO(

				ano,

				campanha,

				projeto,

				uf,

				situacao,

				criticadoCampo,

				mediaDiasEntrada == null ? null : mediaDiasEntrada.doubleValue(),

				mediaDiasCritica == null ? null : mediaDiasCritica.doubleValue(),

				mediaDiasPublicacao == null ? null : mediaDiasPublicacao.doubleValue(),

				mediaDiasCalculoCoordenada == null ? null : mediaDiasCalculoCoordenada.doubleValue()

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

	public String getSituacao() {
		return situacao;
	}

	public void setSituacao(String situacao) {
		this.situacao = situacao;
	}
}
