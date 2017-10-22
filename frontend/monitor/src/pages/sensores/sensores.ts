import { Component } from '@angular/core';
import { NavController, ToastController, LoadingController, Events } from 'ionic-angular';
import { AppSettings } from '../../app/app.settings';
import { HttpService } from "../../app/http-service"

@Component({
  selector: 'page-sensores',
  templateUrl: 'sensores.html'
})
export class SensoresPage {
  private valores = [];
  public pids = [];

  lerSensores: boolean = false;

  private loaderRecarregar;

  constructor(public navCtrl: NavController, 
              public loadingCtrl: LoadingController,
              private appSettings : AppSettings,
              private toastCtrl: ToastController,
              private httpService : HttpService, 
              private events: Events) 
  {
    this.events.subscribe('tab:changed', (index) => {
      if(index != 3)
        this.pausar();
      else
        this.recarregar();
    });
  }

  public pausar(){
    this.zeraContadores();
    this.lerSensores = false;
  }

  public recarregar(){
    this.lerSensores = true;
    
    this.recuperarPids();
    
    if(this.lerSensores){
      this.loaderRecarregar = this.loadingCtrl.create({
        content: "Carregando..."
      });
      this.loaderRecarregar.present();
      this.monitorarPids();
    }
    
  }

  public recuperarPids(){
    let loader = this.loadingCtrl.create({
      content: "Carregando..."
    });
    loader.present();
    this.appSettings.getEndpoint().then(endpoint => {
      this.httpService.get(endpoint + 'get_obdii_pids').then(result => {
        var list = result.json();
        if(list.error){
          this.pausar();
          AppSettings.TOAST(this.toastCtrl, 'ERROR', list.error, 3000);
        } else {
          this.pids = list;
        }
        loader.dismiss();
      }).catch(error => {
        console.log(error);
        this.pausar();
        loader.dismiss();
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      });
    }).catch(error => {
      console.log(error);
      this.pausar();
      loader.dismiss();
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }

  public monitorarPids(){
    this.appSettings.getEndpoint().then(endpoint => {
      this.httpService.get(endpoint + 'get_obdii_values').then(result => {
        var list = result.json();
        if(list.error){
          this.lerSensores = false;
          this.zeraContadores();
          AppSettings.TOAST(this.toastCtrl, 'ERROR', list.error, 3000);
        } else if(this.lerSensores){
          this.valores = list;
          this.valores.forEach(sensor => {
            this.pids.filter(x => x.codigo == sensor.codigo)
              .forEach(pid => {
                pid.valor = sensor.valor;
              });
          });
          this.monitorarPids();
        }
        this.loaderRecarregar.dismiss();
      }).catch(error =>{
        console.log(error);
        this.lerSensores = false;
        this.zeraContadores();
        this.loaderRecarregar.dismiss();
        AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
      });
    }).catch(error => {
      console.log(error);
      this.lerSensores = false;
      this.zeraContadores();
      this.loaderRecarregar.dismiss();
      AppSettings.TOAST(this.toastCtrl, 'ERROR', error, 3000);
    });
  }

  public zeraContadores(){
    this.pids.forEach(pid => {
        pid.valor = 0;
    });
  }
}