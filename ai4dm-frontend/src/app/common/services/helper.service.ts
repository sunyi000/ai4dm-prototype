import { Injectable } from '@angular/core';
import { DataService } from './data.service';


@Injectable({
    providedIn: 'root'
})
export class HelperService {

    constructor(private dataService:DataService){
        

    }

    // updateResults(result){
    //     if (result.length>0) {
    //         this.dataService.set_heads(result);
    //         //this.dataService.cols = this.dataService.heads;
    //     }
    //     this.dataService.sites=result;
    //     this.dataService.cols = Object.keys(result[0]);
    //     this.dataService.dataSource.data = this.dataService.sites;
    // }

}