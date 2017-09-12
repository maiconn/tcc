import { NgModule } from '@angular/core';

@NgModule({})
export class AppSettings {
    public static API_ENDPOINT_INIT = 'http://192.168.0.9:5000/';
    public API_ENDPOINT = '';

    constructor(){
        
    }

    public getEndpointByResult(result){
        var _configuracoes = result ? result : {};
        if(!_configuracoes.endpoint){
            _configuracoes.endpoint = AppSettings.API_ENDPOINT_INIT;
        } else {
            _configuracoes = _configuracoes;
        }
        console.log(_configuracoes);
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