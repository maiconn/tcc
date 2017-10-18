import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { AppSettings } from '../../app/app.settings';
import { HttpService } from "../../app/http-service"

@Component({
  selector: 'page-sensores',
  templateUrl: 'sensores.html'
})
export class SensoresPage {

  public list = [];
  private loader;
  public lerSensores: boolean = false;

  constructor(public navCtrl: NavController, 
              public loadingCtrl: LoadingController,
              private appSettings : AppSettings,
              private storage: Storage, 
              private toastCtrl: ToastController,
              private httpService : HttpService) 
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

  public pausar(){
    this.list = [];
    this.lerSensores = false;
  }

  public monitorarSensores(){
    this.lerSensores = true;
    this.appSettings.getEndpoint().then(endpoint => {
      this.httpService.get(endpoint + 'get_obdii').then(result => {
        var list = result.json();
        if(list.error){
          AppSettings.TOAST(this.toastCtrl, 'ERROR', list.error, 3000);
          this.lerSensores = false;
          this.list = [];
        } else if(this.lerSensores){
          this.list = list;
          this.monitorarSensores();
        }
        this.loader.dismiss();
      }).catch(error =>{
        this.lerSensores = false;
        console.log("ERROR: " + error);
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
        this.loader.dismiss();
      });
    }).catch(error => {
      this.lerSensores = false;
      console.log("ERROR: " + error);
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      this.loader.dismiss();
    });
  }
}
