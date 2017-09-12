import { Component } from '@angular/core';

import { LocalizacaoPage } from '../localizacao/localizacao';
import { SensoresPage } from '../sensores/sensores';
import { FotosPage } from '../fotos/fotos';
import { ConfiguracoesPage } from '../configuracoes/configuracoes';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = FotosPage;
  tab2Root = LocalizacaoPage;
  tab3Root = SensoresPage;
  tab4Root = ConfiguracoesPage;

  constructor() {

  }
}
