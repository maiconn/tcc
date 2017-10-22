import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController } from 'ionic-angular';
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
          this.lerSensores = false;
          this.list = [];
          AppSettings.TOAST(this.toastCtrl, 'ERROR', list.error, 3000);
        } else if(this.lerSensores){
          this.list = list;
          this.monitorarSensores();
        }
        this.loader.dismiss();
      }).catch(error =>{
        console.log(error);
        this.lerSensores = false;
        this.list = [];
        this.loader.dismiss();
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      });
    }).catch(error => {
      console.log(error);
      this.lerSensores = false;
      this.list = [];
      this.loader.dismiss();
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }
}
