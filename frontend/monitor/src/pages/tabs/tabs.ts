import { Component } from '@angular/core';

import { LocalizacaoPage } from '../localizacao/localizacao';
import { SensoresPage } from '../sensores/sensores';
import { FotosPage } from '../fotos/fotos';
import { ConfiguracoesPage } from '../configuracoes/configuracoes';
import { StatusPage } from '../status/status';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = ConfiguracoesPage;
  tab2Root = FotosPage;
  tab3Root = LocalizacaoPage;
  tab4Root = SensoresPage;
  tab5Root = StatusPage;

  constructor() {

  }
}
