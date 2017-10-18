import { Component } from '@angular/core';
import { NavController, ToastController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { LoadingController } from 'ionic-angular';

import { AppSettings } from '../../app/app.settings';
import { RemoitService } from '../../app/remoteit-service';
import { HttpService } from "../../app/http-service"

@Component({
  selector: 'page-configuracoes',
  templateUrl: 'configuracoes.html'
})
export class ConfiguracoesPage {
  public configuracoes = AppSettings.DEFAULT_CONFIGURATIONS;

  constructor(public navCtrl: NavController,
              private storage: Storage, 
              private toastCtrl: ToastController,
              public loadingCtrl: LoadingController,
              private remoitService : RemoitService,
              private appSettings : AppSettings,
              private httpService : HttpService) 
  {
    let loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    loader.present();

    storage.get("configuracoes").then((result) => {
      loader.dismiss();
      this.configuracoes = result ? result : {};
      
      if(!this.configuracoes.endpoint){
        this.configuracoes = AppSettings.DEFAULT_CONFIGURATIONS;
      }
    }, (error) => {
      loader.dismiss();
      console.log("ERROR DB: ", error);
    });
    
  }

  public salvar(){
    let loader = this.loadingCtrl.create({
      content: "Salvado..."
    });
    loader.present();

    this.appSettings.getEndpoint().then(endpoint => {
      this.httpService.post(endpoint + "save_configs", this.configuracoes).then(result => {
        if(result.json().status == "OK"){
          this.storage.set("configuracoes", this.configuracoes);
          AppSettings.TOAST(this.toastCtrl, null, 'Configurações salvas!', 2000);
        }
        loader.dismiss();
      }).catch(error =>{
        this.storage.set("configuracoes", this.configuracoes);
        AppSettings.TOAST(this.toastCtrl, "ERROR", "Não foi possível salvar no servidor, Serviço fora do ar!", 3000);
        loader.dismiss();
      });
    }).catch(error => {
      AppSettings.TOAST(this.toastCtrl, "ERROR", error, 3000);
      loader.dismiss();
    });
  }

  public carregarConfiguracoesEndpoint(){
    let loader = this.loadingCtrl.create({
      content: "Buscando configurações..."
    });
    loader.present();

    this.httpService.get(this.configuracoes.endpoint + 'get_configs').then(result => {
      var configuracoes = result.json();
      if(configuracoes.endpoint){
        var endpoint = this.configuracoes.endpoint;
        this.configuracoes = configuracoes;
        this.configuracoes.endpoint = endpoint;
        this.configuracoes.remoit = AppSettings.DEFAULT_REMOIT;
        this.configuracoes.tipoConexao = 0;
        this.storage.set("configuracoes", this.configuracoes);
        AppSettings.TOAST(this.toastCtrl, null, 'Configurações carregadas!', 2000);
      }  else if (configuracoes.error) {
        AppSettings.TOAST(this.toastCtrl, 'ERROR', configuracoes.error, 2000);
      }
      loader.dismiss();
    }).catch(error =>{
      console.log(error);
      loader.dismiss();
      AppSettings.TOAST(this.toastCtrl, 'ERROR', "Serviço fora do ar!", 2000);
    });
  }

  public carregarConfiguracoesRemoit(){
    let loader = this.loadingCtrl.create({
      content: "Buscando configurações..."
    });
    loader.present();

    this.remoitService.getConfigs(this.configuracoes.remoit.user, this.configuracoes.remoit.senha).then(response => {
      this.configuracoes.remoit = response;
      this.storage.set("configuracoes", this.configuracoes);
      AppSettings.TOAST(this.toastCtrl, null, 'Configurações carregadas!', 2000);
      loader.dismiss();
    }).catch(error => {
      AppSettings.TOAST(this.toastCtrl, 'ERROR', `Ops... ${error}`, 2000);
      console.log(error);
      loader.dismiss();
    });
  }
}