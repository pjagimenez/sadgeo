# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/bdg_formulario_busca.py
@created: 09-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from __future__ import annotations

import tkinter as tk

from sidgeo.domain.registro import Registro
from sidgeo.view.coordenadas_frame import CoordenadasFrame
from sidgeo.view.mensagem_visual import MensagemVisual
from sidgeo.view.registro_visao_mapeador import RegistroMapeadorVisao
from sidgeo.view.tema import AbaRolavel, ajustar_janela, estilizar_quadro
from sidgeo.domain.coordenadas import coordenadas_decimais, diferenca_horizontal_m


class JanelaCoordenadasBDG(tk.Toplevel):
    """Formulário Tela para comparar coordenadas locais com coordenadas vindas do BDG."""

    def __init__(
        self,
        master: tk.Tk | tk.Toplevel,
        mensagens: MensagemVisual,
        view_mapper: RegistroMapeadorVisao,
        registro_local: Registro,
        registro_bdg: Registro | None,
    ) -> None:
        super().__init__(master)

        self.mensagens = mensagens
        self.view_mapper = view_mapper
        self.registro_local = registro_local
        self.registro_bdg = registro_bdg
        self.resultado: tuple[bool, Registro] | None = None

        self.title(f"Comparação de coordenadas — Estação {registro_local.cod_estacao}")
        ajustar_janela(self, 1100, 500)
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self._construir_interface()
        self.grab_set()

    def _construir_interface(self) -> None:
        # Reserva o espaço das ações antes da área rolável.
        frame_bottom = tk.Frame(self)
        frame_bottom.pack(side="bottom", fill="x", padx=10, pady=6)
        conteudo = AbaRolavel(self)
        conteudo.pack(fill="both", expand=True, padx=8, pady=8)
        top_frame = conteudo.conteudo
        top_frame.columnconfigure(0, weight=3)
        top_frame.columnconfigure(1, weight=2)

        self.frm_coord_local = CoordenadasFrame(
            top_frame,
            self.mensagens,
            titulo="Coordenadas (Local)",
            com_def_coord=False,
        )
        self.frm_coord_local.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=2,
        )

        self.frm_coord_bdg = CoordenadasFrame(
            top_frame,
            self.mensagens,
            titulo="Coordenadas BDG",
            com_def_coord=False,
        )
        self.frm_coord_bdg.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=2,
        )

        self.lbl_data_local = tk.Label(top_frame, text=self._rotulo_data(self.registro_local), anchor="w")
        self.lbl_data_local.grid(row=1, column=0, sticky="ew", padx=8)
        self.lbl_data_bdg = tk.Label(top_frame, text=self._rotulo_data(self.registro_bdg), anchor="w")
        self.lbl_data_bdg.grid(row=1, column=1, sticky="ew", padx=8)
        self.lbl_diferenca = tk.Label(top_frame, text="Diferença indisponível: coordenadas incompletas.",
                                     anchor="w", font=("TkDefaultFont", 10, "bold"), wraplength=950)
        self.lbl_diferenca.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=12)
        tk.Label(top_frame, text="A escolha altera o formulário. Use Salvar registro para confirmar.",
                 anchor="w").grid(row=3, column=0, columnspan=2, sticky="ew", padx=8)

        self.btn_local = tk.Button(
            frame_bottom,
            text="Manter Local",
            command=self.manter_local,
        )
        self.btn_local.pack(side="left", padx=5)

        self.btn_bdg = tk.Button(
            frame_bottom,
            text="Usar BDG",
            command=self.usar_bdg,
        )
        self.btn_bdg.pack(side="left", padx=5)

        self.btn_cancelar = tk.Button(
            frame_bottom,
            text="Cancelar",
            command=self.fechar,
        )
        self.btn_cancelar.pack(side="left", padx=5)

        self._popular_coordenadas_local()
        self._popular_coordenadas_bdg()
        if self.registro_bdg is not None:
            try:
                metros = diferenca_horizontal_m(self.registro_local, self.registro_bdg)
                valor = f"{metros:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                self.lbl_diferenca.config(text=f"Diferença horizontal aproximada: {valor} m")
            except ValueError:
                pass

        self.frm_coord_local.disable_all()
        self.frm_coord_bdg.disable_all()
        estilizar_quadro(self.frm_coord_local)
        estilizar_quadro(self.frm_coord_bdg)
        conteudo.ativar_rolagem()

    @staticmethod
    def _rotulo_data(registro: Registro | None) -> str:
        if registro is not None and registro.data_coordenada is not None:
            return f"Data da coordenada: {registro.data_coordenada:%d/%m/%Y}"
        return "Data da coordenada: não informada"

    def _popular_coordenadas_local(self) -> None:
        self._popular_frame_coordenadas(
            self.frm_coord_local,
            self.registro_local,
        )

    def _popular_coordenadas_bdg(self) -> None:
        if self.registro_bdg is None:
            self.mensagens.warn(
                "Nenhuma coordenada encontrada no BDG.",
                modal=True,
            )
            self.btn_bdg.config(state="disabled")
            return

        self._popular_frame_coordenadas(
            self.frm_coord_bdg,
            self.registro_bdg,
        )
        try:
            coordenadas_decimais(self.registro_bdg)
        except ValueError:
            self.btn_bdg.config(state="disabled")

    def _popular_frame_coordenadas(
        self,
        frame: CoordenadasFrame,
        registro: Registro,
    ) -> None:
        view = self.view_mapper.registro_para_dict_view(registro)

        frame.combo_lat_sinal.set(view["lat_sinal"])
        frame.txt_lat_grau.delete(0, "end")
        frame.txt_lat_grau.insert(0, view["lat_grau"])
        frame.txt_lat_min.delete(0, "end")
        frame.txt_lat_min.insert(0, view["lat_min"])
        frame.txt_lat_seg.delete(0, "end")
        frame.txt_lat_seg.insert(0, view["lat_seg"])

        frame.combo_lon_sinal.set(view["lon_sinal"])
        frame.txt_lon_grau.delete(0, "end")
        frame.txt_lon_grau.insert(0, view["lon_grau"])
        frame.txt_lon_min.delete(0, "end")
        frame.txt_lon_min.insert(0, view["lon_min"])
        frame.txt_lon_seg.delete(0, "end")
        frame.txt_lon_seg.insert(0, view["lon_seg"])

        frame.combo_tipo_fonte.set(view["tipo_fonte_coord"])
        frame.var_atualizar_coord.set(view["is_atualizar_coord"])
        frame.var_ocup_gps.set(view["is_ocup_gps"])
        frame.var_ocup_mira.set(view["is_ocup_mira"])
        frame.var_ocup_gravimetro.set(view["is_ocup_gravimetro"])

    def usar_bdg(self) -> None:
        if self.registro_bdg is None:
            return
        try:
            coordenadas_decimais(self.registro_bdg)
        except ValueError as erro:
            self.mensagens.warn(str(erro), modal=True)
            return
        self.resultado = (True, self.registro_bdg)
        self.destroy()

    def manter_local(self) -> None:
        self.resultado = (False, self.registro_local)
        self.destroy()

    def fechar(self) -> None:
        self.resultado = None
        self.destroy()

    def obter_resultado(self) -> tuple[bool, Registro] | None:
        self.wait_window()
        return self.resultado
