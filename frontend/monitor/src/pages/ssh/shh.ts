import { Component, ViewChild } from '@angular/core';
import { NavController, NavParams, LoadingController, ToastController } from 'ionic-angular';
import { Clipboard } from '@ionic-native/clipboard';

import { RemoitService } from '../../app/remoteit-service';

import { AppSettings } from '../../app/app.settings';

@Component({
  selector: 'page-ssh',
  templateUrl: 'ssh.html'
})
export class SSHPage {
  public configuracoes;
  public senha;
  public ehParaExibir = false;
  public ssh = "";

  @ViewChild('minhaSenha') minhaSenha;
  @ViewChild('meuSSH') meuSSH;

  constructor(public navCtrl: NavController, 
              public navParams: NavParams,
              private toastCtrl: ToastController,
              public loadingCtrl: LoadingController,
              private remoitService : RemoitService,
              private clipboard: Clipboard) 
  {
    this.configuracoes = navParams.get("configuracoes");
    window.setTimeout(() => {
      console.log(this.minhaSenha);
      this.minhaSenha.setFocus();
    },600);
  }

  public exibirConfigs(){
    if(this.senha == "tcc"){
      this.carregarSSH();
    } else {
      AppSettings.TOAST(this.toastCtrl, "ERROR", "¯\\_(ツ)_/¯", 3000);
      this.navCtrl.pop();
    }
  }

  public carregarSSH(){
    let loader = this.loadingCtrl.create({
      content: "Buscando ssh..."
    });
    loader.present();
    this.ssh = "pi@"

    // ENDPOINT
    if(this.configuracoes.tipoConexao == 0){
      
      this.ssh += this.configuracoes.endpoint
                      .substring(0, this.configuracoes.endpoint.length - 1)
                      .replace("http://","")
                       + ":22";
      this.clipboard.copy(this.ssh);
      loader.dismiss();
      this.meuSSH.setFocus();
      this.ehParaExibir = true;
    } 
    
    // PROXY
    else if(this.configuracoes.tipoConexao == 1) 
    {
      this.remoitService.getSSH(this.configuracoes.remoit.apikey, this.configuracoes.remoit.token).then(ssh => {
        this.ssh += ssh.remoteIp.replace("http://","");
        this.clipboard.copy(this.ssh);
        loader.dismiss();
        this.meuSSH.setFocus();
        this.ehParaExibir = true; 
      }).catch(error => {
        this.ehParaExibir = false;
        AppSettings.TOAST(this.toastCtrl, "ERROR", error, 3000);
        loader.dismiss();
      });
    }
  }
}
