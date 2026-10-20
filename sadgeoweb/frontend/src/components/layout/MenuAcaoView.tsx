import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { menus } from "../../navigation";

export default function MenuAcaoView() {
  const { pathname } = useLocation();
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  return (
    <aside className="portal-menu">
      <nav aria-label="Navegação principal" className="menu-navigation">
        <NavLink to="/index">Painel de Controle</NavLink>
        {menus.map((group, index) => {
          const open = expanded[group.label] ?? group.items.some(item => item.path === pathname);
          const id = `menu-group-${index}`;
          return (
            <section className="menu-group" key={group.label}>
              <button type="button" className="menu-group-toggle" aria-expanded={open}
                aria-controls={id} onClick={() => setExpanded(previous => ({ ...previous, [group.label]: !open }))}>
                <span className="menu-chevron" aria-hidden="true">{open ? "▾" : "▸"}</span>
                <span>{group.label}</span>
              </button>
              <div id={id} hidden={!open}>
                {group.items.map(item => (
                  <NavLink key={item.path} to={item.path}>
                    {item.label}{item.campanha && <span className="campaign-code"> ({item.campanha})</span>}
                  </NavLink>
                ))}
              </div>
            </section>
          );
        })}
      </nav>
    </aside>
  );
}
