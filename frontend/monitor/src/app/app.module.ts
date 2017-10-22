import { NgModule, ErrorHandler } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { IonicApp, IonicModule, IonicErrorHandler } from 'ionic-angular';
import { MyApp } from './app.component';
import { HttpModule } from '@angular/http';
import { DatePipe } from '@angular/common'
import { Clipboard } from '@ionic-native/clipboard';

import { AgmCoreModule } from '@agm/core';

import { LocalizacaoPage } from '../pages/localizacao/localizacao';
import { LocalizacaoDetailPage } from '../pages/localizacaoDetail/localizacaoDetail';
import { SensoresPage } from '../pages/sensores/sensores';
import { CameraMonitorarPage } from '../pages/cameraMonitorar/cameraMonitorar';
import { CameraPage } from '../pages/camera/camera';
import { FotoDetailPage } from '../pages/fotoDetail/fotoDetail';
import { ConfiguracoesPage } from '../pages/configuracoes/configuracoes';
import { StatusPage } from '../pages/status/status';
import { SSHPage } from '../pages/ssh/shh';
import { TabsPage } from '../pages/tabs/tabs';

import { AppSettings } from '../app/app.settings';
import { HttpService } from '../app/http-service';

import { RemoitService } from '../app/remoteit-service';

import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { IonicStorageModule } from '@ionic/storage';

import { GaugesModule } from 'ng-canvas-gauges/lib';

@NgModule({
  declarations: [
    MyApp,
    LocalizacaoPage,
    LocalizacaoDetailPage,
    SensoresPage,
    CameraMonitorarPage,
    CameraPage,
    FotoDetailPage,
    ConfiguracoesPage,
    StatusPage,
    SSHPage,
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
    GaugesModule
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    LocalizacaoPage,
    LocalizacaoDetailPage,
    SensoresPage,
    CameraMonitorarPage,
    CameraPage,
    FotoDetailPage,
    ConfiguracoesPage,
    StatusPage,
    SSHPage,
    TabsPage
  ],
  providers: [
    StatusBar,
    DatePipe,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    RemoitService,
    AppSettings,
    HttpService,
    Clipboard
  ]
})
export class AppModule {}
