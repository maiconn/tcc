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

    this.loader.dismiss();
  }

  public reconectar(){
    this.loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    this.loader.present();

    this.loader.dismiss();
  }
}
