import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
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
    private storage: Storage, 
    private toastCtrl: ToastController) 
  {
    this.recuperar()
  }

  public openURL(url: string){
    console.log("FUNCIONOU "+url);
    window.open(url, '_system', 'location=yes'); 
    return false;
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
      this.loader.dismiss();
      console.log("ERROR: " + error);
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }
}
