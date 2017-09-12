import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController } from 'ionic-angular';
import { Http } from '@angular/http';
import { Storage } from '@ionic/storage';
import { AppSettings } from '../../app/app.settings';

@Component({
  selector: 'page-sensores',
  templateUrl: 'sensores.html'
})
export class SensoresPage {

  public list = [];
  private loader;

  constructor(public navCtrl: NavController, 
              private http : Http, 
              public loadingCtrl: LoadingController,
              private appSettings : AppSettings,
              private storage: Storage, 
              private toastCtrl: ToastController) 
  {
    this.loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    this.loader.present();
    this.monitorarSensores();
  }

  public reconectar(){
    this.loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    this.loader.present();
    this.monitorarSensores();
  }

  public monitorarSensores(){
    this.storage.get("configuracoes").then((result) => 
    {
        var _endpoint = this.appSettings.getEndpointByResult(result);      
        this.http.get(_endpoint + 'get_obdii').subscribe(
          data => {
            var list = data.json();
            if(list.error){
              AppSettings.TOAST(this.toastCtrl, 'ERROR', list.error, 3000);
              this.list = [];
            } else {
              this.list = list;
              this.monitorarSensores();
            }
            console.log(list);
            this.loader.dismiss();
          },
          error => {
            this.list = [];
            console.log(error);
            this.loader.dismiss();
            AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
          }
        );
      }, (error) => 
      {
          console.log("ERROR DB: " + error);
          AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      }
    );
  }



}
