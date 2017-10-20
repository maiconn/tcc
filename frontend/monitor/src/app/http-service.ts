import { Http, Headers } from '@angular/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/observable/throw';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/timeoutWith';

import { AppSettings } from "./app.settings"

@Injectable()
export class HttpService {
    
    constructor(private http: Http) {

    }

    public get(url: string, headersDict = null) {
        return new Observable<any>(observer => { 
            this.http
                .get(`${url}`, {headers: new Headers(headersDict)}).subscribe(data =>{
                    observer.next(data);
                    observer.complete();
                }, error =>{
                    console.log(error);
                    if (`${error}`.indexOf("Response with status: 0  for URL: null") >= 0){
                        observer.error("Ops.. Servidor fora do ar!");
                    } else {
                        observer.error(error);
                    }
                });
        })
        .map((response) => response)
        .timeoutWith(AppSettings.DEFAULT_TIMEOUT, Observable.throw(new Error('timeout!')))
        .toPromise();
    }

    public post(url: string, postData, headersDict = null){
        return this.http.post(`${url}`, postData, {headers: new Headers(headersDict)})
            .map((response) => response)
            .timeoutWith(AppSettings.DEFAULT_TIMEOUT, Observable.throw(new Error('timeout!')))
            .toPromise();
    }
}