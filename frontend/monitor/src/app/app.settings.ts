import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Storage } from '@ionic/storage';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { RemoitService } from './remoteit-service'

@Injectable()
export class AppSettings {
    public static DEFAULT_TIMEOUT: number = 30000;
    public static API_ENDPOINT_INIT = 'http://192.168.0.23/';

    public static DEFAULT_CONFIGURATIONS = { 
        tipoConexao: 0, 
        endpoint: AppSettings.API_ENDPOINT_INIT,
        email: '',
        celular: '',
        notificarEmail: false,
        notificarSMS: false,
        simulador: 0,
        remoit: {
            user: '',
            senha: '',
            token: '',
            apikey: '',
            deviceaddress: '',
            remoteIp: ''
        }
      };

    public static DEFAULT_REMOIT = {
        user: '',
        senha: '',
        token: '',
        apikey: '',
        deviceaddress: '',
        remoteIp: ''
    }

    constructor(private storage: Storage,
                private remoitService : RemoitService){
        
    }

    private getEndpointByResult(result){
        var _configuracoes = result ? result : {};
        if(!_configuracoes.endpoint){
            _configuracoes.endpoint = AppSettings.API_ENDPOINT_INIT;
        } else {
            _configuracoes = _configuracoes;
        }
        return _configuracoes.endpoint;
    }

    public static TOAST(toastCtrl, type, message, duration){
        var _msg = '';
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