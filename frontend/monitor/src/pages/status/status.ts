import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController, AlertController } from 'ionic-angular';
import { AppSettings } from '../../app/app.settings';
import { HttpService } from "../../app/http-service"


@Component({
  selector: 'page-statusDetail',
  templateUrl: 'status.html'
})
export class StatusPage {

  private loader;

  private nullStatusDtc = {
    dtc_pendentes: [],
    dtc_registrados: [],
    status: null
  };

  public statusDtc = this.nullStatusDtc

  constructor(public navCtrl: NavController,
              private httpService : HttpService,
              public loadingCtrl: LoadingController,
              private appSettings : AppSettings,
              private toastCtrl: ToastController,
              public alertCtrl: AlertController) 
  {
    this.recuperar()
  }

  public openURL(url: string){
    window.open(url, '_system', 'location=yes'); 
    return false;
  }

  public limparDTC(){
    const alert = this.alertCtrl.create({
      title: 'Apagar DTC',
      message: 'Deseja realmente apagar os códigos de erro do seu veículo?',
      buttons: [
        {
          text: 'Sim',
          handler: () => this.limparDtc()
        },
        {
          text: 'Não',
          role: 'nao',
          handler: () => { }
        }
      ]
    });
    alert.present();
  }

  private limparDtc(){
    this.loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    this.loader.present();

    this.appSettings.getEndpoint().then(endpoint => {
      this.httpService.get(endpoint + 'clear_dtc').then(result => {
        var clear = result.json();
        if(clear.error){
          AppSettings.TOAST(this.toastCtrl, 'ERROR', clear.error, 3000);
        } else {
          AppSettings.TOAST(this.toastCtrl, null, "Códigos de erro DTC apagados!", 3000);
          this.loader.dismiss();
          this.recuperar();
        }
      }).catch(error =>{
        console.log(error);
        this.loader.dismiss();
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      });
    }).catch(error => {
      this.loader.dismiss();
      console.log("ERROR: " + error);
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }

  public recuperar(){
    this.loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    this.loader.present();

    this.appSettings.getEndpoint().then(endpoint => {
      this.httpService.get(endpoint + 'get_dtc').then(result => {
        var statusDtc = result.json();
        if(statusDtc.error){
          AppSettings.TOAST(this.toastCtrl, 'ERROR', statusDtc.error, 3000);
          this.statusDtc = this.nullStatusDtc;
        } else {
          this.statusDtc = statusDtc;
        }
        this.loader.dismiss();
      }).catch(error =>{
        this.statusDtc = this.nullStatusDtc;
        console.log(error);
        this.loader.dismiss();
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      });
    }).catch(error => {
      this.statusDtc = this.nullStatusDtc;
      this.loader.dismiss();
      console.log("ERROR: " + error);
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }
}
