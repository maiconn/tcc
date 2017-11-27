import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Storage } from '@ionic/storage';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

//import { RemoitService } from './remoteit-service'

@Injectable()
export class AppSettings {
    public static DEFAULT_TIMEOUT: number = 30000;
    public static API_ENDPOINT_INIT = 'http://veiculo.sytes.net:5000/';

    public static REMOT3_USER = "";
    public static REMOT3_PASS = "";

    public static DEFAULT_CONFIGURATIONS = { 
        tipoConexao: 0, 
        endpoint: AppSettings.API_ENDPOINT_INIT,
        email: '',
        celular: '',
        notificarEmail: false,
        notificarSMS: false,
        simulador: 0,
        remoit: {
            user: AppSettings.REMOT3_USER,
            senha: AppSettings.REMOT3_PASS,
            token: '',
            apikey: '',
            deviceaddress: '',
            remoteIp: ''
        }
      };

    public static DEFAULT_REMOIT = {
        user: AppSettings.REMOT3_USER,
        senha: AppSettings.REMOT3_PASS,
        token: '',
        apikey: '',
        deviceaddress: '',
        remoteIp: ''
    }
    
    constructor(private storage: Storage){
        
    }

    public static TOAST(toastCtrl, type, message, duration){
        var _css = '';
        if(type == 'ERROR'){
            _css = 'toast-error';
        } 
        let toast = toastCtrl.create({
            message: message,
            duration: duration,
            position: 'top',
            cssClass: _css
        });
        toast.present();
    }

    public getEndpoint(){
        return new Observable<string>(observer => {
            this.storage.get("configuracoes").then((result) => 
            {
                var _configuracoes = result ? result : {};

                if(!_configuracoes.endpoint){
                    _configuracoes.endpoint = AppSettings.API_ENDPOINT_INIT;
                    observer.next(_configuracoes.endpoint);
                    observer.complete();
                } else if (_configuracoes.tipoConexao == 0) {
                    observer.next(_configuracoes.endpoint);
                    observer.complete();
                } else if (_configuracoes.tipoConexao == 1) {
                    observer.next(_configuracoes.remoit.remoteIp);
                    observer.complete();
                }
            },
            error => {
                observer.error(error);
            })
        })
            .map((response) => response)
            .toPromise();
    }
}
