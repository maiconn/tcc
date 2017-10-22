import { Component } from '@angular/core';

import { Tab, Events } from 'ionic-angular';

import { LocalizacaoPage } from '../localizacao/localizacao';
import { SensoresPage } from '../sensores/sensores';
import { CameraPage } from '../camera/camera';
import { ConfiguracoesPage } from '../configuracoes/configuracoes';
import { StatusPage } from '../status/status';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = ConfiguracoesPage;
  tab2Root = CameraPage;
  tab3Root = LocalizacaoPage;
  tab4Root = SensoresPage;
  tab5Root = StatusPage;

  constructor(private events: Events) { }

  tabChange(tab: Tab){
    this.events.publish('tab:changed', tab.index);
  }
}
