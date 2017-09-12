import { NgModule, ErrorHandler } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { IonicApp, IonicModule, IonicErrorHandler } from 'ionic-angular';
import { MyApp } from './app.component';
import { HttpModule } from '@angular/http';
import { DatePipe } from '@angular/common'

import { AgmCoreModule } from '@agm/core';

import { LocalizacaoPage } from '../pages/localizacao/localizacao';
import { LocalizacaoDetailPage } from '../pages/localizacaoDetail/localizacaoDetail';
import { SensoresPage } from '../pages/sensores/sensores';
import { FotosPage } from '../pages/fotos/fotos';
import { FotoDetailPage } from '../pages/fotoDetail/fotoDetail';
import { ConfiguracoesPage } from '../pages/configuracoes/configuracoes';
import { TabsPage } from '../pages/tabs/tabs';
import { AppSettings } from '../app/app.settings';

import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { IonicStorageModule } from '@ionic/storage';

@NgModule({
  declarations: [
    MyApp,
    LocalizacaoPage,
    LocalizacaoDetailPage,
    SensoresPage,
    FotosPage,
    FotoDetailPage,
    ConfiguracoesPage,
    TabsPage
  ],
  imports: [
    BrowserModule, 
    HttpModule,
    IonicModule.forRoot(MyApp),
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyDdj6ktEhIiqI67yFYy6UCrz1kcQProAuc'
    }),
    IonicStorageModule.forRoot(),
    AppSettings
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    LocalizacaoPage,
    LocalizacaoDetailPage,
    SensoresPage,
    FotosPage,
    FotoDetailPage,
    ConfiguracoesPage,
    TabsPage
  ],
  providers: [
    StatusBar,
    DatePipe,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler}
  ]
})
export class AppModule {}
