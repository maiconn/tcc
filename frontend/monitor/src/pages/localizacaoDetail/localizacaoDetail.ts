import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

@Component({
  selector: 'page-LocalizacaoDetail',
  templateUrl: 'localizacaoDetail.html'
})
export class LocalizacaoDetailPage {
  public localizacao;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.localizacao = navParams.get("localizacao");
  }
}
