import { Component } from '@angular/core';
import { NavController, ToastController } from 'ionic-angular';
import { Http } from '@angular/http';
import { LoadingController } from 'ionic-angular';
import { AppSettings } from '../../app/app.settings';
import { Storage } from '@ionic/storage';
import { DatePipe } from '@angular/common'
import { LocalizacaoDetailPage } from '../../pages/localizacaoDetail/localizacaoDetail';

@Component({
  selector: 'page-localizacao',
  templateUrl: 'localizacao.html'
})
export class LocalizacaoPage {
  private localizacoes: Array<Object>;

  constructor(public navCtrl: NavController,
              private http : Http, 
              public loadingCtrl: LoadingController, 
              private storage: Storage, 
              private datePipe: DatePipe,
              private appSettings : AppSettings, 
              private toastCtrl: ToastController) 
  {
    storage.get("localizacoes").then((result) => {
      this.localizacoes = result ? <Array<Object>> result : [];
    }, (error) => {
      console.log("ERROR DB: ", error);
    });
  }

  public nova(){
    this.storage.get("configuracoes")
      .then((result) => 
      {
        var endpoint = this.appSettings.getEndpointByResult(result);
        
        let loader = this.loadingCtrl.create({
          content: "Carregando..."
        });
        loader.present();
        this.http.get(endpoint + 'get_gps').subscribe(data => {
          var coords = data.json();
          console.log(coords);
          if(coords.error){
            AppSettings.TOAST(this.toastCtrl, 'ERROR', coords.error, 3000);
          } else {
            var localizacao = {
              data: this.datePipe.transform(new Date(), 'dd/MM/yyyy HH:mm:ss'),
              coords: coords
            };
    
            this.localizacoes.push(localizacao);
            this.storage.set("localizacoes", this.localizacoes);
            this.navCtrl.push(LocalizacaoDetailPage, {localizacao: localizacao});
          }
          loader.dismiss();
        },
        error => {
          console.log(error);
          loader.dismiss();
          AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
        });
      }, (error) => 
      {
        console.log("ERROR DB: " + error);
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      });
  }

  public itemSelected(localizacao){
    this.navCtrl.push(LocalizacaoDetailPage, {localizacao: localizacao});
  }
}
