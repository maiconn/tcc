import { NgModule } from '@angular/core';

@NgModule({})
export class AppSettings {
    public static API_ENDPOINT_INIT = 'http://192.168.0.12:5000/';

    public static DEFAULT_CONFIGURATIONS = { 
        endpoint: AppSettings.API_ENDPOINT_INIT,
        email: '',
        celular: '',
        notificarEmail: false,
        notificarSMS: false,
        simulador: 0
      };

    constructor(){
        
    }

    public getEndpointByResult(result){
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
            _msg = '[ERRO] ' + message;
            _css = 'toast-error';
        } else {
            _msg = message;
        }
        let toast = toastCtrl.create({
            message: _msg,
            duration: duration,
            position: 'top',
            cssClass: _css
        });
        toast.present();
    }
}