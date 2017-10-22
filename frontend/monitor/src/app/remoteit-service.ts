import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/observable/throw';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { HttpService } from "./http-service"

@Injectable()
export class RemoitService {

    private actionUrl: string;
    private headerDict = {
        'content-type': 'application/json',
        'apikey': 'WeavedDemoKey\$2015'
    };   

    constructor(private httpService: HttpService) {
        this.actionUrl = "https://api.weaved.com/v22/api";
    }

    public autenticar(user: string, senha: string) {
        return new Observable<any>(observer => { 
            this.httpService.get(`${this.actionUrl}/user/login/${user}/${senha}`, this.headerDict)
                .then(result => {
                    observer.next(result);
                    observer.complete();
                }).catch(error =>{
                    if(error.status == 403){
                        if(error._body){
                            observer.error(JSON.parse(error._body).reason)
                        }
                    }
                    observer.error(error);
                });
        })
        .map((response) => response.json())
        .toPromise();
    }

    public listAll(headers) {
        return new Observable<any>(observer => { 
            this.httpService.get(`${this.actionUrl}/device/list/all`, headers)
                .then(result => {
                    observer.next(result);
                    observer.complete();
                }).catch(error =>{
                    observer.error(error);
                    observer.complete();
                });
        })
        .map((response) => response.json())
        .toPromise();
    }

    public connect(deviceaddress: string, headers){
        var postData = {
            'deviceaddress': deviceaddress,
            'wait': true
        };

        return new Observable<any>(observer => { 
            this.httpService.post(`${this.actionUrl}/device/connect`, postData, headers)
                .then(result => {
                    observer.next(result);
                    observer.complete();
                }).catch(error =>{
                    observer.error(error);
                    observer.complete();
                });
        })
        .map((response) => response.json())
        .toPromise();
            
    }

    public getConfigs(user: string, senha: string){
        return new Observable<any>(observer => {
            this.autenticar(user, senha)
                .then(data => {
                    console.log(data);
                    if (data.status == 'true'){
                        const headerDict = {
                            'content-type': 'application/json',
                            'apikey': data.apikey,
                            'token': data.token
                            };                        
                        this.listAll(headerDict).then(retorno_listAll =>{
                            console.log(retorno_listAll);
                            if (retorno_listAll.status == 'true'){ 
                                var servico = retorno_listAll.devices.filter(x => x.servicetitle == "HTTP")[0];
                                this.connect(servico.deviceaddress, headerDict).then(
                                    retorno_connect =>{
                                        console.log(retorno_connect);
                                        observer.next({
                                            user: user,
                                            senha: senha,
                                            apikey: data.apikey,
                                            token : data.token,
                                            deviceaddress: servico.deviceaddress,
                                            remoteIp: retorno_connect.connection.proxy + '/'
                                        });
                                        observer.complete();
                                    }).catch(error => {
                                        observer.error(error);
                                    });
                            } else {
                                observer.error(data.reason);
                            }
                        }).catch(error => {
                            observer.error(error);
                        });

                    } else {
                        observer.error(data.reason);
                    }
                }).catch(error => {
                    observer.error(error);
                });
            })
            .map((response) => response)
            .toPromise();
        
    }

    public getSSH(apikey: string, token: string){
        return new Observable<any>(observer => {
                const headerDict = {
                    'content-type': 'application/json',
                    'apikey': apikey,
                    'token': token
                    };                        
                this.listAll(headerDict).then(retorno_listAll =>{
                    console.log(retorno_listAll);
                    if (retorno_listAll.status == 'true'){ 
                        var servico = retorno_listAll.devices.filter(x => x.servicetitle == "SSH")[0];
                        this.connect(servico.deviceaddress, headerDict).then(
                            retorno_connect =>{
                                console.log(retorno_connect);
                                observer.next({
                                    deviceaddress: servico.deviceaddress,
                                    remoteIp: retorno_connect.connection.proxy
                                });
                                observer.complete();
                            }).catch(error => {
                                observer.error(error);
                            });
                    } else {
                        observer.error(retorno_listAll.reason);
                    }
                }).catch(error => {
                    observer.error(error);
                });
            })    
            .map((response) => response)
            .toPromise();
    }
}