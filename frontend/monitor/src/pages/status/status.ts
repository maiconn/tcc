import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController } from 'ionic-angular';
import { Http } from '@angular/http';
import { Storage } from '@ionic/storage';
import { AppSettings } from '../../app/app.settings';

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
    private http : Http, 
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
    this.storage.get("configuracoes").then((result) => 
    {
        var _endpoint = this.appSettings.getEndpointByResult(result);      
        this.http.get(_endpoint + 'get_dtc').subscribe(
          data => {
            var statusDtc = data.json();
            if(statusDtc.error){
              AppSettings.TOAST(this.toastCtrl, 'ERROR', statusDtc.error, 3000);
              this.statusDtc = this.nullStatusDtc;
            } else {
              this.statusDtc = statusDtc;
            }
            this.loader.dismiss();
          },
          error => {
            this.statusDtc = this.nullStatusDtc;
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
