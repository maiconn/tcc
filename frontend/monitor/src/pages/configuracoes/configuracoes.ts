import { Component } from '@angular/core';
import { NavController, ToastController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { Http } from '@angular/http';
import { LoadingController } from 'ionic-angular';

import { AppSettings } from '../../app/app.settings';

@Component({
  selector: 'page-configuracoes',
  templateUrl: 'configuracoes.html'
})
export class ConfiguracoesPage {
  public configuracoes = { 
    endpoint: '',
    email: '',
    celular: '',
    notificarEmail: false,
    notificarSMS: false
  };

  constructor(public navCtrl: NavController,
              private storage: Storage, 
              private toastCtrl: ToastController,
              private http : Http, 
              public loadingCtrl: LoadingController) 
  {
    let loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    loader.present();

    storage.get("configuracoes").then((result) => {
      this.configuracoes = result ? result : {};
      
      if(!this.configuracoes.endpoint){
        this.configuracoes = AppSettings.DEFAULT_CONFIGURATIONS;
      }

      this.http.get(this.configuracoes.endpoint+"get_configs").subscribe(data => {
        loader.dismiss();
        if(data.json().endpoint){
          this.configuracoes = data.json();
        } else {
          storage.get("configuracoes").then((result) => {
            this.configuracoes = result ? result : {};
            
            if(!this.configuracoes.endpoint){
              this.configuracoes = AppSettings.DEFAULT_CONFIGURATIONS;
            }
      
          }, (error) => {
            console.log("ERROR DB: ", error);
          });
        }
      },
      error => {
        loader.dismiss();
        storage.get("configuracoes").then((result) => {
          this.configuracoes = result ? result : {};
          
          if(!this.configuracoes.endpoint){
            this.configuracoes = AppSettings.DEFAULT_CONFIGURATIONS;
          }
    
        }, (error) => {
          console.log("ERROR DB: ", error);
        });
      });
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

    this.http.post(this.configuracoes.endpoint + "save_configs", this.configuracoes)
    .subscribe(data => {
      if(data.json().status == "OK"){
        this.storage.set("configuracoes", this.configuracoes);
        AppSettings.TOAST(this.toastCtrl, null, 'Configurações salvas!', 2000);
      }
      loader.dismiss();
    },
    error => {
      this.storage.set("configuracoes", this.configuracoes);
      AppSettings.TOAST(this.toastCtrl, "Não foi possível salvar no servidor, Endpoint fora do ar!", error, 2500);
      loader.dismiss();
    });
  }

  public testarEndpoint(){
    let loader = this.loadingCtrl.create({
      content: "Testando Endpoint..."
    });
    loader.present();

    this.http.get(this.configuracoes.endpoint).subscribe(data => {
      if(data.json().status == "OK"){
        AppSettings.TOAST(this.toastCtrl, null, 'Endpoint no ar!', 2000);
      }
      loader.dismiss();
    },
    error => {
      console.log(error);
      loader.dismiss();
      AppSettings.TOAST(this.toastCtrl, 'ERROR', "Endpoint inválido!", 2000);
    });   
  }
}