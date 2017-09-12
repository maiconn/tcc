import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

@Component({
  selector: 'page-fotoDetail',
  templateUrl: 'fotoDetail.html'
})
export class FotoDetailPage {
  public imagem;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.imagem = navParams.get("foto");
  }

  public nova(){
    
  }

}
