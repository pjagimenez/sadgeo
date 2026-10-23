# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/main_window.py
@created: 25-02-2025 pjag
@updated: 16-10-2025 pjag
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional


from sidgeo.view.info_basicas_frame import InfoBasicasFrame
from sidgeo.view.coordenadas_frame import CoordenadasFrame
from sidgeo.view.observacoes_frame import ObservacoesFrame
from sidgeo.view.registro_frame import RegistroFrame
from sidgeo.view.dataset_frame import DatasetFrame
from sidgeo.view.sadgeo_formulario_busca import JanelaBuscaSadgeo
from sidgeo.view.bdg_formulario_busca import JanelaCoordenadasBDG 
from sidgeo.view.registro_visao_mapeador import RegistroMapeadorVisao

from sidgeo.view.dialogo_visual import DialogoVisual

from sidgeo.util.settings import APP_ALTURA, APP_LARGURA, APP_SIGLA, APP_VERSAO
from sidgeo.application.aplicacao_controller import AplicacaoController
from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog
from sidgeo.infra.erros_integracao import IntegracaoErro

from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_metadados import COLUNAS_NOMES
from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.domain.erros import ValidacaoErro

from sidgeo.view.mensagem_visual import MensagemVisual

class AplicativoVisual(tk.Tk):
    """Janela principal do SIDGEO (Controller da UI)."""

    def __init__(
        self,
        controle_app: AplicacaoController,
        notificacao_app: NotificadorEventoLog,
    ) -> None:
        super().__init__()
        
        self.controle_app = controle_app
        self.msg = MensagemVisual(notificacao_app)
        self.mapper_view = RegistroMapeadorVisao()           
        self.dialogo = DialogoVisual()
        self.dialogo.attach(self)
        
        self.titulo=f"Coletor {APP_SIGLA} - {APP_VERSAO}",
        
        self.title(self.titulo)
        self.geometry(f"{APP_LARGURA}x{APP_ALTURA}")

        lbl_titulo = tk.Label(self, text=self.titulo, font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=2)

        self._criar_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.msg.info("APP:__init__ -> Pronto")


    # ───────────────────────────── UI building ─────────────────────────────
    def _criar_widgets(self) -> None:
        self.msg.info("APP:_criar_widgets -> Montagem da tela iniciada.")

        top_frame = tk.Frame(self)
        top_frame.pack(fill="both", expand=True, padx=5, pady=2)
        top_frame.columnconfigure(0, weight=3)
        top_frame.columnconfigure(1, weight=2)

        self.info_basicas = InfoBasicasFrame(top_frame, self.msg)
        self.info_basicas.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)

        self.coordenadas = CoordenadasFrame(top_frame, self.msg)
        self.coordenadas.grid(row=0, column=1, sticky="nsew", padx=5, pady=2)

        # ----- FRAME do MEIO ------------------------
        mid_frame = tk.Frame(self)
        mid_frame.pack(fill="both", expand=True, padx=5, pady=2)
        #mid_frame.columnconfigure(0, weight=7)
        #mid_frame.columnconfigure(1, weight=3)

        self.observacoes = ObservacoesFrame(mid_frame, self.msg)
        self.observacoes.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)

        self.reg_frame = RegistroFrame(
            mid_frame, self.msg,
            salvar=self.acao_salvar,
            excluir=self.acao_excluir,
            limpar=self.acao_limpar,
            buscar=self.acao_buscar,
            comparar=self.acao_comparar_coord_bdg,
        )
        self.reg_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=2)

        mid_frame.columnconfigure(0, weight=3)
        mid_frame.columnconfigure(1, weight=2)

        # ----- FRAME do RODAPE ------------------------

        self.ds_frame = DatasetFrame(
            self, self.msg,
            importar=self.janela_importar,
            exportar=self.janela_exportar,
            zerar=self.zerar_base,
            ver=self.exibir_dados,
            consSadgeo=self.janela_importar_sadgeo,
        )
        self.ds_frame.pack(side="bottom", fill="x", pady=2)

        self.atualiza_listbox()
        self.msg.info("APP:_criar_widgets -> Montagem da tela finalizada.")
        

    # ───────────────────────────── helpers ─────────────────────────────
    def _coletar_dados_do_form(self) -> Registro:
        self.msg.info("APP:_coletar_dados_do_form -> Coletando dados")
        dados: Dict[str, Any] = {}
        dados.update(self.info_basicas.get_data())
        dados.update(self.coordenadas.get_data())
        dados.update(self.observacoes.get_data())
        reg = RegistroFabrica.criar(dados)
        self.msg.info("APP:_coletar_dados_do_form -> OK")
        return reg

    def _cod_selecionado(self) -> Optional[str]:
        sel = self.reg_frame.lb.curselection()
        if not sel:
            self.msg.warn("Nenhum registro selecionado.")
            return None
        linha = self.reg_frame.lb.get(sel[0])
        return (linha.split("|", 1)[0].strip() if linha else "") or None

    def validar_dados_pre_salvar(self) -> None:
        conexao = self.info_basicas.entry_conexao.get().strip()
        tipo_conexao = self.info_basicas.combo_tipo_conexao.get().strip()
    
        if bool(conexao) != bool(tipo_conexao):
    
            if not conexao:
                self.info_basicas.entry_conexao.focus_set()
            else:
                self.info_basicas.combo_tipo_conexao.focus_set()
    
            raise ValidacaoErro(
                "Conexão e Tipo de Conexão devem ser informados em conjunto."
            )


    # ───────────────────────────── ações CRUD ─────────────────────────────
    def acao_salvar(self) -> None:
        try:
            self.msg.info("App:acao_salvar -> preparando salvamento")
            
            self.validar_dados_pre_salvar()
            reg = self._coletar_dados_do_form()
            
            self.controle_app.salvar_registro(reg)  
            
            self.atualiza_listbox()
            self.acao_limpar()
            
            self.msg.info("App:acao_salvar -> Registro salvo com sucesso.")

        except ValidacaoErro as e:
            self.msg.warn(str(e), modal=True)
        except Exception as e:
            self.msg.error(f"Falha ao salvar: {e}", modal=True)


    def acao_excluir(self) -> None:
        self.msg.info("App:acao_excluir -> iniciar")
        reg = self._coletar_dados_do_form()
        cod = (reg.cod_estacao or "").strip()
        if not cod:
            self.msg.warn("Nenhuma estação válida selecionada para exclusão.")
            return
        if not self.msg.confirm(f"Deseja excluir o registro da Estação {cod}?", cor="red"):
            self.msg.info("Exclusão cancelada.")
            return
        if self.controle_app.excluir_registro(cod):
            self.msg.info(f"Estação {cod} excluída.")
            self.atualiza_listbox()
            self.acao_limpar()
        else:
            self.msg.warn(f"Nenhum registro encontrado para o código {cod}.")


    def acao_buscar(self) -> None:
        self.msg.info("App:acao_buscar -> executar")
        cod = self._cod_selecionado()
        if not cod:
            return
        reg = self.controle_app.buscar_registro(cod)
        if not reg:
            self.msg.warn("Registro não encontrado.")
            return
        self._preencher_formulario(reg)
        self.msg.info(f"Registro '{cod}' carregado.")
    
    
    def acao_comparar_coord_bdg(self) -> None:
        self.msg.info("App:acao_buscar -> executar")
    
        cod = self.info_basicas.entry_estacao.get().strip()
    
        if not cod:
            self.msg.warn("Necessário preencher Código Estação.", True )
            return
    
        resultado = self.janela_importar_coordenadas_bdg(cod)
    
        if resultado is None:
            self.msg.info("Operação cancelada.")
            return
    
        atualiz, reg = resultado
    
        if atualiz:    
            self._preencher_coordenadas(reg)
            self.acao_salvar()
            self.msg.info( "Coordenadas atualizadas com dados do BDG.")
    
        else:    
            self.msg.info("Mantidas as coordenadas locais.")
    
        
        
    def acao_limpar(self) -> None:
        self._limpar_formulario()

    # ───────────────────────────── dataset / UI utils ────────────────────
    def exibir_dados(self) -> None:
        self.msg.info("App:exibir_dados -> abrir viewer")
        top = tk.Toplevel(self)
        top.title("Registros SIDGEO")
        top.geometry("1000x600")

        wrapper = tk.Frame(top)
        wrapper.pack(fill="both", expand=True)

        tree = ttk.Treeview(wrapper, show="headings")
        tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(wrapper, orient="horizontal", command=tree.xview)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        wrapper.rowconfigure(0, weight=1)
        wrapper.columnconfigure(0, weight=1)

        tree["columns"] = COLUNAS_NOMES
        for col in COLUNAS_NOMES:
            tree.heading(col, text=col)
            tree.column(col, width=max(80, len(col) * 10), stretch=False)

        for reg in self.controle_app.listar_registro():
            row = self.mapper_view.registro_para_dict_view(reg)
            tree.insert("", "end", values=[row.get(c, "") for c in COLUNAS_NOMES])

    def on_close(self) -> None:
        self.msg.info("App -> encerrando.")
        if self.msg.confirm("Deseja sair salvando os dados?"):
            self.controle_app.finalizarPersistencia()  # salve dataset/estado
        self.destroy()

    def _limpar_formulario(self) -> None:
        self.msg.info("Formulário limpo.")
        self.info_basicas.limpar()
        self.coordenadas.limpar()
        self.observacoes.limpar()
    
    
    def _preencher_coordenadas(self, reg: Registro) -> None:
        
        view = self.mapper_view.registro_para_dict_view(reg)
        coord = self.coordenadas
    
        # Latitude
        coord.combo_lat_sinal.set(view["lat_sinal"])
    
        coord.txt_lat_grau.delete(0, "end")
        coord.txt_lat_grau.insert(0, view["lat_grau"])
    
        coord.txt_lat_min.delete(0, "end")
        coord.txt_lat_min.insert(0, view["lat_min"])
    
        coord.txt_lat_seg.delete(0, "end")
        coord.txt_lat_seg.insert(0, view["lat_seg"])
    
        # Longitude
        coord.combo_lon_sinal.set(view["lon_sinal"])
    
        coord.txt_lon_grau.delete(0, "end")
        coord.txt_lon_grau.insert(0, view["lon_grau"])
    
        coord.txt_lon_min.delete(0, "end")
        coord.txt_lon_min.insert(0, view["lon_min"])
    
        coord.txt_lon_seg.delete(0, "end")
        coord.txt_lon_seg.insert(0, view["lon_seg"])
    
        # Fonte
        coord.combo_tipo_fonte.set(view["tipo_fonte_coord"])
    
        # Flags
        coord.var_atualizar_coord.set(view["is_atualizar_coord"])
        coord.var_ocup_gps.set(view["is_ocup_gps"])
        coord.var_ocup_mira.set(view["is_ocup_mira"])
        coord.var_ocup_gravimetro.set(view["is_ocup_gravimetro"])
        """
        Atualiza apenas os campos de coordenadas do formulário.
        Não altera informações básicas nem observações.
    """

    def _preencher_formulario(self, reg: Registro) -> None:
        self.msg.info("Atualizando formulário…")
        view = self.mapper_view.registro_para_dict_view(reg)
        self._limpar_formulario()

        ib = self.info_basicas
        coord = self.coordenadas
        obs = self.observacoes

        # ---- Info Básicas ----
        ib.entry_estacao.delete(0, "end")
        ib.entry_estacao.insert(0, view["cod_estacao"])
        ib.combo_monumentacao.set(view["monumentacao"])
        ib.combo_tipo_local.set(view["tipo_local"])
        ib.entry_inscr_chapa.delete(0, "end")
        ib.entry_inscr_chapa.insert(0, view["inscr_chapa"])
        ib.combo_situacao.set(view["situacao"])
        ib.entry_conexao.delete(0, "end")
        ib.entry_conexao.insert(0, view["conexao"])
        ib.combo_tipo_conexao.set(view["tipo_conexao"])
        ib.entry_rn_anterior.delete(0, "end");
        ib.entry_rn_anterior.insert(0, view["rn_anterior"])
        ib.combo_campanha.set(view["campanha"])
        ib.combo_uf.set(view["uf"])

        if view["data_levantamento"]: ib.entry_data_levantamento.set_date(view["data_levantamento"])
        if view["data_critica"]:      ib.entry_data_critica.set_date(view["data_critica"])

        for widget, key in [
            (ib.entry_projeto, "projeto"),
            (ib.entry_nue, "nue"),
            (ib.entry_linha, "linha"),
            (ib.entry_caderneta, "caderneta"),
            (ib.entry_informante, "informante"),
            (ib.entry_siape, "siape"),
            (ib.entry_municipio, "municipio"),
        ]:
            widget.delete(0, "end"); widget.insert(0, view[key])

        ib.seq_var.set(view["seq"])
        ib.status_vrf_var.set(view["status_vrf"])

        # ---- Coordenadas ----
        coord.combo_lat_sinal.set(view["lat_sinal"])
        coord.txt_lat_grau.delete(0, "end"); coord.txt_lat_grau.insert(0, view["lat_grau"])
        coord.txt_lat_min.delete(0, "end");  coord.txt_lat_min.insert(0, view["lat_min"])
        coord.txt_lat_seg.delete(0, "end");  coord.txt_lat_seg.insert(0, view["lat_seg"])

        coord.combo_lon_sinal.set(view["lon_sinal"])
        coord.txt_lon_grau.delete(0, "end"); coord.txt_lon_grau.insert(0, view["lon_grau"])
        coord.txt_lon_min.delete(0, "end");  coord.txt_lon_min.insert(0, view["lon_min"])
        coord.txt_lon_seg.delete(0, "end");  coord.txt_lon_seg.insert(0, view["lon_seg"])

        coord.combo_tipo_fonte.set(view["tipo_fonte_coord"])

        coord.var_atualizar_coord.set(view["is_atualizar_coord"])
        coord.var_ocup_gps.set(view["is_ocup_gps"])
        coord.var_ocup_mira.set(view["is_ocup_mira"])
        coord.var_ocup_gravimetro.set(view["is_ocup_gravimetro"])

        # ---- Observações ----
        for txt_widget, key in [
            (obs.txt_descricao, "descricao"),
            (obs.txt_localizacao, "localizacao"),
            (obs.txt_itinerario, "itinerario"),
            (obs.txt_observacao, "observacao"),
        ]:
            txt_widget.delete("1.0", "end")
            txt_widget.insert("1.0", view[key])

    def zerar_base(self) -> None:
        self.msg.info("Zerando base local…")
        if self.msg.confirm("ATENÇÃO!\nIsso apagará TODOS os registros.\nDeseja continuar?", cor="red"):
            self.controle_app.zerar_base()
            self.atualiza_listbox()
            self.msg.info("Base zerada.", modal=True)

    def janela_importar(self) -> None:
        
        escolha = self.dialogo.escolher_arquivo_importacao()
        
        if escolha is None:
            return
        
        path, fmt = escolha
        
        try:
            n = self.controle_app.importar(path, fmt)
            self.msg.info(f"Importação concluída de {path} ({n} registros).")
            self.atualiza_listbox()
        except Exception as e:
            self.msg.error(f"Falha na importação: {e}", modal=True)

    def janela_exportar(self) -> None:
        
        escolha = self.dialogo.escolher_arquivo_exportacao()
        
        if escolha is None:
            return
        
        path, fmt = escolha
        
        try:
            self.controle_app.exportar(path, fmt)
            self.msg.info(f"Exportado em {path}")
        except Exception as e:
            self.msg.error(f"Falha ao exportar: {e}", modal=True)

        
    def atualiza_listbox(self) -> None:
        
        self.msg.info("Atualizando lista de estações…")
        self.reg_frame.lb.delete(0, tk.END)
    
        for reg in self.controle_app.listar_registro():
            v = self.mapper_view.registro_para_dict_view(reg)
    
            cod = v.get("cod_estacao", "")[:10]
    
            # Extrai parte antes do hífen e remove espaços
            campanha = v.get("campanha", "").split("-")[0].strip()
    
            # Formata a data para DD/MM/YYYY
            data_raw = v.get("data_levantamento", "")
            data = ""
            if data_raw:
                try:
                    if isinstance(data_raw, str) and len(data_raw) >= 10:
                        data = f"{data_raw[8:10]}/{data_raw[5:7]}/{data_raw[0:4]}"
                    elif hasattr(data_raw, "strftime"):
                        data = data_raw.strftime("%d/%m/%Y")
                except Exception:
                    data = ""
    
            # Trata o campo seq: se for None ou 'null', mostra vazio
            seq = v.get("seq")
            seq_str = "" if seq in (None, "null") else str(seq)
            seq_str = seq_str.ljust(5)
    
            # Monta a string com largura fixa
            texto = f"{cod:<8} | {campanha:<5} | {data:<10} | {seq_str:<7}"
            self.reg_frame.lb.insert(tk.END, texto)
    
    
    def janela_importar_coordenadas_bdg( self, cod_estacao: str,):    
        try:
            reg_bdg = self.controle_app.buscar_bdg(
                cod_estacao
            )
    
        except IntegracaoErro as erro:
            self.msg.error(
                str(erro),
                modal=True,
            )
            return None
    
        reg_local = self.controle_app.buscar_registro(
            cod_estacao
        )
    
        dialogo = JanelaCoordenadasBDG(
            self,
            mensagens=self.msg,
            view_mapper=self.mapper,
            registro_local=reg_local,
            registro_bdg=reg_bdg,
        )
    
        return dialogo.obter_resultado()
 
    def janela_importar_sadgeo(self) -> None:
        
        dialogo = JanelaBuscaSadgeo(
            self,
            mensagens=self.msg,
            controller=self.controle_app,
        )
              
        reg_sadgeo = dialogo.obter_resultado()
        if reg_sadgeo is None:
            self.msg.warn("Nenhum registro selecionado.",  True)
            return
        try:
            self.controle_app.salvar_registro(reg_sadgeo)
        except Exception as e:
            self.msg.error(f"Falha na importação: {e}")
            return
        self.msg.info("Importação via SADGEO concluída.")
        self.atualiza_listbox()
    
    
    def show_confirm_modal(self, pergunta: str, cor: str = "black") -> bool:
        modal = tk.Toplevel(self)
        modal.title("Confirmação")
        modal.transient(self)
        modal.grab_set()
        modal.geometry("+%d+%d" % (self.winfo_rootx()+60, self.winfo_rooty()+60))
    
        tk.Label(modal, text=pergunta, fg=cor, wraplength=300).pack(padx=20, pady=2)
    
        resultado = {"resposta": False}
    
        def confirmar():
            resultado["resposta"] = True
            modal.destroy()
    
        def cancelar():
            resultado["resposta"] = False
            modal.destroy()
    
        btns = tk.Frame(modal)
        btns.pack(pady=2)
        tk.Button(btns, text="Sim", command=confirmar).pack(side="left", padx=2)
        tk.Button(btns, text="Não", command=cancelar).pack(side="left", padx=2)
    
        self.wait_window(modal)
        return resultado["resposta"]
    
    
    def show_modal(self, mensagem: str, cor: str = "black") -> None:
        modal = tk.Toplevel(self)
        modal.title("Mensagem")
        modal.transient(self)
        modal.grab_set()
        modal.geometry("+%d+%d" % (self.winfo_rootx()+60, self.winfo_rooty()+60))
    
        tk.Label(modal, text=mensagem, fg=cor, wraplength=300).pack(padx=20, pady=2)
        tk.Button(modal, text="OK", command=modal.destroy).pack(pady=2)
    
        self.wait_window(modal)