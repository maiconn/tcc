import { Component } from '@angular/core';
import { NavController, LoadingController, ToastController } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { DatePipe } from '@angular/common'

import { AppSettings } from '../../app/app.settings';
import { FotoDetailPage } from '../../pages/fotoDetail/fotoDetail';
import { HttpService } from '../../app/http-service';

@Component({
  selector: 'page-fotos',
  templateUrl: 'fotos.html'
})
export class FotosPage {
  private fotos: Array<Object>;

  constructor(public navCtrl: NavController, 
              public loadingCtrl: LoadingController, 
              private storage: Storage, 
              private datePipe: DatePipe,
              private appSettings : AppSettings,
              private httpService : HttpService, 
              private toastCtrl: ToastController
            ) 
  { 
    storage.get("fotos").then((result) => {
        this.fotos = result ? <Array<Object>> result : [];
    }, (error) => {
        console.log("ERROR: ", error);
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }


  public nova(){
    this.appSettings.getEndpoint().then(endpoint => {
      let loader = this.loadingCtrl.create({
        content: "Carregando..."
      });
      loader.present();
      this.httpService.get(endpoint + 'get_foto').then(data => {
        var imagem = {
            data: this.datePipe.transform(new Date(), 'dd/MM/yyyy HH:mm:ss'),
            foto: data.text()
        };
  
        this.fotos.push(imagem);
        this.storage.set("fotos", this.fotos);
        this.navCtrl.push(FotoDetailPage, {foto: imagem});
  
        loader.dismiss();
      }).catch(error =>{
          console.log(error);
          loader.dismiss();
          AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000); 
      });
    }).catch(error => {
      console.log("ERROR: ", error);
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }

  public itemSelected(foto){
    this.navCtrl.push(FotoDetailPage, {foto: foto});
  }

}
