import { Component } from '@angular/core';
import { NavController, ToastController } from 'ionic-angular';
import { Storage } from '@ionic/storage';

import { AppSettings } from '../../app/app.settings';

@Component({
  selector: 'page-configuracoes',
  templateUrl: 'configuracoes.html'
})
export class ConfiguracoesPage {
  public configuracoes = { 
    endpoint: '' 
  };

  constructor(public navCtrl: NavController,
              private storage: Storage, 
              private toastCtrl: ToastController) 
  {
    storage.get("configuracoes").then((result) => {
      this.configuracoes = result ? result : {};
      console.log(this.configuracoes);
      if(!this.configuracoes.endpoint){
        this.configuracoes.endpoint = AppSettings.API_ENDPOINT_INIT;
      }
      console.log(this.configuracoes);
    }, (error) => {
      console.log("ERROR DB: ", error);
    });
  }

  public salvar(){
    this.storage.set("configuracoes", this.configuracoes);
    AppSettings.TOAST(this.toastCtrl, null, 'Configurações salvas!', 2000);
  }
}
