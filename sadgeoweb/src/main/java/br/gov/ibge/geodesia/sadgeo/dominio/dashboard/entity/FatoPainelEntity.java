package br.gov.ibge.geodesia.sadgeo.dominio.dashboard.entity;

import java.time.LocalDate;

import br.gov.ibge.geodesia.sadgeo.dashboard.dto.FatoPainelDTO;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "V_FATO_SADGEO_PAINEL", schema = "BDG_VALIDA")
public class FatoPainelEntity {

	@Id
	@Column(name = "SEQ")
	private String seq;

	@Column(name = "ANO_LEVANTAMENTO")
	private Integer anoLevantamento;

	@Column(name = "MES_LEVANTAMENTO")
	private Integer mesLevantamento;

	@Column(name = "DATA_LEVANTAMENTO")
	private LocalDate dataLevantamento;

	@Column(name = "DIM_CAMPANHA")
	private String campanha;

	@Column(name = "DIM_PROJETO")
	private String projeto;

	@Column(name = "DIM_UF")
	private String uf;

	@Column(name = "DIM_MUNICIPIO")
	private String municipio;

	@Column(name = "DIM_TIPOLOCAL")
	private String tipoLocal;

	@Column(name = "DIM_UORG_ORIGEM")
	private String uorgOrigem;

	@Column(name = "DIM_SITUACAO")
	private String situacao;

	@Column(name = "CONTAGEM")
	private Integer contagem;

	@Column(name = "DIAS_ATE_ENTRADA")
	private Integer diasAteEntrada;

	@Column(name = "DIAS_ATE_CRITICA")
	private Integer diasAteCritica;

	@Column(name = "DIAS_ATE_PUBLICACAO")
	private Integer diasAtePublicacao;

	@Column(name = "DIAS_ATE_CALCULO_COORD")
	private Integer diasAteCalculoCoord;

	public String getSeq() {
		return seq;
	}

	public void setSeq(String seq) {
		this.seq = seq;
	}

	public Integer getAnoLevantamento() {
		return anoLevantamento;
	}

	public void setAnoLevantamento(Integer anoLevantamento) {
		this.anoLevantamento = anoLevantamento;
	}

	public Integer getMesLevantamento() {
		return mesLevantamento;
	}

	public void setMesLevantamento(Integer mesLevantamento) {
		this.mesLevantamento = mesLevantamento;
	}

	public LocalDate getDataLevantamento() {
		return dataLevantamento;
	}

	public void setDataLevantamento(LocalDate dataLevantamento) {
		this.dataLevantamento = dataLevantamento;
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

	public String getMunicipio() {
		return municipio;
	}

	public void setMunicipio(String municipio) {
		this.municipio = municipio;
	}

	public String getTipoLocal() {
		return tipoLocal;
	}

	public void setTipoLocal(String tipoLocal) {
		this.tipoLocal = tipoLocal;
	}

	public String getUorgOrigem() {
		return uorgOrigem;
	}

	public void setUorgOrigem(String uorgOrigem) {
		this.uorgOrigem = uorgOrigem;
	}

	public String getSituacao() {
		return situacao;
	}

	public void setSituacao(String situacao) {
		this.situacao = situacao;
	}

	public Integer getContagem() {
		return contagem;
	}

	public void setContagem(Integer contagem) {
		this.contagem = contagem;
	}

	public Integer getDiasAteEntrada() {
		return diasAteEntrada;
	}

	public void setDiasAteEntrada(Integer diasAteEntrada) {
		this.diasAteEntrada = diasAteEntrada;
	}

	public Integer getDiasAteCritica() {
		return diasAteCritica;
	}

	public void setDiasAteCritica(Integer diasAteCritica) {
		this.diasAteCritica = diasAteCritica;
	}

	public Integer getDiasAtePublicacao() {
		return diasAtePublicacao;
	}

	public void setDiasAtePublicacao(Integer diasAtePublicacao) {
		this.diasAtePublicacao = diasAtePublicacao;
	}

	public Integer getDiasAteCalculoCoord() {
		return diasAteCalculoCoord;
	}

	public void setDiasAteCalculoCoord(Integer diasAteCalculoCoord) {
		this.diasAteCalculoCoord = diasAteCalculoCoord;
	}

	public FatoPainelDTO toDTO() {

		return new FatoPainelDTO(

				seq,

				anoLevantamento,

				mesLevantamento,

				dataLevantamento,

				campanha,

				projeto,

				uf,

				municipio,

				tipoLocal,

				uorgOrigem,

				situacao,

				contagem,

				diasAteEntrada,

				diasAteCritica,

				diasAtePublicacao,

				diasAteCalculoCoord

		);
	}
}
