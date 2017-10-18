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
        return this.http
            .get(`${url}`, {headers: new Headers(headersDict)})
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