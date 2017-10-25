import { Component, ViewChild } from '@angular/core';
import { NavController, LoadingController, ToastController, Navbar, Events  } from 'ionic-angular';
import { DatePipe } from '@angular/common'

import { AppSettings } from '../../app/app.settings';

@Component({
  selector: 'page-cameraMonitorar',
  templateUrl: 'cameraMonitorar.html'
})
export class CameraMonitorarPage {
  src: string = "";
  dataHora: string = "";

  public executando: boolean = false;

  public loader;

  @ViewChild(Navbar) navBar: Navbar;

  constructor(public navCtrl: NavController, 
              public loadingCtrl: LoadingController, 
              private datePipe: DatePipe,
              private appSettings : AppSettings, 
              private toastCtrl: ToastController,
              private events: Events
    ) 
  {  
    this.events.subscribe('tab:changed', (index) => {
      if(this.executando){
        this.pausar();
      }
    });
    this.executar();
  }

  ionViewDidLoad() {
    this.navBar.backButtonClick = (e:UIEvent)=>{
      this.pausar();
     }
  }

  public pausar(){
    this.src = null;
    this.dataHora = null;
    this.executando = false;
    this.navCtrl.pop();
  }

  public executar(){
    this.loader = this.loadingCtrl.create({
      content: "Carregando..."
    }); 
    this.loader.present();
    this.executando = true;
    this.monitorarCamera();
  }

  public monitorarCamera(){
    this.appSettings.getEndpoint().then(endpoint => {
      this.dataHora = this.datePipe.transform(new Date(), 'dd/MM/yyyy HH:mm:ss'),
      this.src = endpoint + "get_video";
      this.loader.dismiss();
    }).catch(error => {
      this.loader.dismiss();
      console.log("ERROR: ", error);
      this.pausar();
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }

}
