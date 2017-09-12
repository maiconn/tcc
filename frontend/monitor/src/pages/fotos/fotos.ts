import { Component } from '@angular/core';
import { NavController, LoadingController, ToastController } from 'ionic-angular';
import { Http } from '@angular/http';
import { Storage } from '@ionic/storage';
import { DatePipe } from '@angular/common'

import { AppSettings } from '../../app/app.settings';
import { FotoDetailPage } from '../../pages/fotoDetail/fotoDetail';

@Component({
  selector: 'page-fotos',
  templateUrl: 'fotos.html'
})
export class FotosPage {
  private fotos: Array<Object>;

  constructor(public navCtrl: NavController, 
              private http : Http, 
              public loadingCtrl: LoadingController, 
              private storage: Storage, 
              private datePipe: DatePipe,
              private appSettings : AppSettings, 
              private toastCtrl: ToastController
            ) 
  { 
    storage.get("fotos").then((result) => {
        this.fotos = result ? <Array<Object>> result : [];
    }, (error) => {
        console.log("ERROR DB: ", error);
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }


  public nova(){
    this.storage.get("configuracoes").then((result) => 
      {
        var endpoint = this.appSettings.getEndpointByResult(result);
        
        let loader = this.loadingCtrl.create({
          content: "Carregando..."
        });
        loader.present();
        this.http.get(endpoint + 'get_foto').subscribe(data => {
          console.log(data);
          var imagem = {
              data: this.datePipe.transform(new Date(), 'dd/MM/yyyy HH:mm:ss'),
              foto: data.text()
          };
    
          this.fotos.push(imagem);
          this.storage.set("fotos", this.fotos);
          this.navCtrl.push(FotoDetailPage, {foto: imagem});
    
          loader.dismiss();
        },
        error => {
          console.log(error);
          loader.dismiss();
          AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
        });
      }, (error) => 
      {
          console.log("ERROR DB: ", error);
          AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      }
    );
  }

  public itemSelected(foto){
    this.navCtrl.push(FotoDetailPage, {foto: foto});
  }

}
