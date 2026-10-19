import { injectGlobalWebcomponentCss } from 'Frontend/generated/jar-resources/theme-util.js';

import { injectGlobalCss } from 'Frontend/generated/jar-resources/theme-util.js';

import { css, unsafeCSS, registerStyles } from '@vaadin/vaadin-themable-mixin';
import $cssFromFile_0 from 'Frontend/css/echarts-sadgeo.css?inline';
import '@vaadin/polymer-legacy-adapter/style-modules.js';
import '@vaadin/vertical-layout/theme/lumo/vaadin-vertical-layout.js';
import '@vaadin/app-layout/theme/lumo/vaadin-app-layout.js';
import '@vaadin/app-layout/theme/lumo/vaadin-drawer-toggle.js';
import '@vaadin/button/theme/lumo/vaadin-button.js';
import '@vaadin/tooltip/theme/lumo/vaadin-tooltip.js';
import 'Frontend/generated/jar-resources/disableOnClickFunctions.js';
import '@vaadin/side-nav/theme/lumo/vaadin-side-nav.js';
import '@vaadin/side-nav/theme/lumo/vaadin-side-nav-item.js';
import '@vaadin/combo-box/theme/lumo/vaadin-combo-box.js';
import 'Frontend/generated/jar-resources/flow-component-renderer.js';
import 'Frontend/generated/jar-resources/comboBoxConnector.js';
import '@vaadin/multi-select-combo-box/theme/lumo/vaadin-multi-select-combo-box.js';
import '@vaadin/horizontal-layout/theme/lumo/vaadin-horizontal-layout.js';
import '@vaadin/grid/theme/lumo/vaadin-grid.js';
import '@vaadin/grid/theme/lumo/vaadin-grid-column.js';
import '@vaadin/grid/theme/lumo/vaadin-grid-sorter.js';
import '@vaadin/checkbox/theme/lumo/vaadin-checkbox.js';
import 'Frontend/generated/jar-resources/gridConnector.ts';
import 'Frontend/generated/jar-resources/vaadin-grid-flow-selection-column.js';
import '@vaadin/grid/theme/lumo/vaadin-grid-column-group.js';
import 'Frontend/generated/jar-resources/lit-renderer.ts';
import '@vaadin/context-menu/theme/lumo/vaadin-context-menu.js';
import 'Frontend/generated/jar-resources/contextMenuConnector.js';
import 'Frontend/generated/jar-resources/contextMenuTargetConnector.js';
import 'Frontend/js/echarts.min.js';
import 'Frontend/js/echarts-helper.js';
import '@vaadin/common-frontend/ConnectionIndicator.js';
import '@vaadin/vaadin-lumo-styles/sizing.js';
import '@vaadin/vaadin-lumo-styles/spacing.js';
import '@vaadin/vaadin-lumo-styles/style.js';
import '@vaadin/vaadin-lumo-styles/vaadin-iconset.js';
import 'Frontend/generated/jar-resources/ReactRouterOutletElement.tsx';

injectGlobalCss($cssFromFile_0.toString(), 'CSSImport end', document);
injectGlobalWebcomponentCss($cssFromFile_0.toString());

const loadOnDemand = (key) => {
  const pending = [];
  if (key === '3f7397cf5cd42ebdb469d4354e7c113803972add17bd17df040c1510c867b80b') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === 'aad70be912e10a317de03c1d8db4cfb3da1367125731b492317828bde89159b1') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === 'abd6c49b7ac7f9de13e1071dbcbcbaf4c6835bf659ac4588cf22b48834e3025c') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === '33ed6947c6c0f61457604c931c5e8794a81d6771a79b1bfd9d5a4ab387dc25b2') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === '98ccd66c00e59b9338fdcbfdb0290e01e6627ec6cb71d82b89542e1aa71c9374') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === '453b07b9fd0305b63f9422a655e2d8e15ee628aff6f235a0487612722f48eec6') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === 'e3fb66ea734ce7444a212df6d53976eb0d2dcbaf045cfe6095dea539a031b509') {
    pending.push(import('./chunks/chunk-0f54f634db48e05042587cbac73cffed20622cbe7a04a88dfec825e06eecf674.js'));
  }
  if (key === '9a8c5b37eb0de7c82be9e0f295d5ae336dcf932ea509d2c7d124b2ea8d7b1f13') {
    pending.push(import('./chunks/chunk-e41dff79cb7ee40a85870de2072574108034c908d9b5a5ee57434bea635a40ea.js'));
  }
  return Promise.all(pending);
}

window.Vaadin = window.Vaadin || {};
window.Vaadin.Flow = window.Vaadin.Flow || {};
window.Vaadin.Flow.loadOnDemand = loadOnDemand;
window.Vaadin.Flow.resetFocus = () => {
 let ae=document.activeElement;
 while(ae&&ae.shadowRoot) ae = ae.shadowRoot.activeElement;
 return !ae || ae.blur() || ae.focus() || true;
}