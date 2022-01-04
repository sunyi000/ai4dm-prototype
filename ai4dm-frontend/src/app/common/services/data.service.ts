import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Injectable, EventEmitter} from '@angular/core';
import { ConstantsService} from './constants.service';
import { MatTableDataSource } from '@angular/material/table';
import { Observable } from 'rxjs';
import {catchError} from 'rxjs/operators';



@Injectable({
    providedIn: 'root'
})
export class DataService {
    
    endpoint:string;


    airports: any[] =[];
    colaircraft : any[] =[];
    colPredictAircraft : any[] =[];

    heads: any[];
    colheads : any[];
    colPredictHeads : any[];

    aircraftHeads : any[];
    aircraftPredictHeads : any[];

    cols: any [];
    colcols : any [];
    colpcols : any [];
   
    coordinates:L.Marker[]= [];

    dataSource = new MatTableDataSource();

    colDs= new MatTableDataSource();;
    colPredictDs= new MatTableDataSource();;
    aircraftDs;
    aircraftPredictDs;
    
    
    constructor(private httpClient: HttpClient,_constant:ConstantsService) {
        this.endpoint = _constant.apiEndpoint;
        
    }

    get_facts(subj:string,pred:string,t:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/facts/' + encodeURIComponent(subj) + "/" + pred + "/" + t)
    }

    get_prediction(subj:string,pred:string,t:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/prediction/' + encodeURIComponent(subj) + "/" + pred +"/" + t)
    }

    get_all_airports(page:number){
        return this.httpClient.get(this.endpoint + '/ai4dm/api/airports/'+page)
    }

    get_airport_predicate_by_airport(type:string){
        return this.httpClient.get(this.endpoint + "/ai4dm/api/questions/airport/" + type)
    }

    get_all_aircrafts(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/aircraft/' )
    }

    get_aircraft_by_id(aircraft_id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/aircraft/' + aircraft_id)
    }

    get_aircraft_predicate(type:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/questions/aircraft/' + type)
    }

    get_runway_by_id(id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/runway/' + id)
    }

    get_region_by_id(id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/region/' + id)
    }

    get_country_by_id(id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/country/' + id)
    }

    get_institution_by_id(id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/institution/' + id)
    }
    get_all_airlines(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/airlines/' )
    }

    get_airline_by_id(airline_id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/airlines/' + airline_id)
    }

    get_airline_predicate(type:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/questions/airlines/' + type)
    }

    get_all_flights(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/flights/' )
    }

    get_flight_by_id(flight_id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/flights/' + flight_id)
    }

    get_flight_predicate(type:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/questions/flights/' + type)
    }

    get_all_events(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/events/' )
    }

    get_event_by_id(event_id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/events/' + event_id)
    }

    get_event_predicates(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/questions/events/')
    }


    get_all_orgs(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/orgs/' )
    }

    get_org_by_id(org_id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/orgs/' + org_id)
    }

    get_org_predicate(type:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/questions/orgs/' + type)
    }


    get_all_persons(){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/persons/' )
    }

    get_person_by_id(person_id:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/persons/' + person_id)
    }

    get_person_predicate(type:string){
        return this.httpClient.get(this.endpoint + 'ai4dm/api/questions/persons/' + type)
    }

    postFile(fileToUpload: File,ds : string,cat:string): Observable<any>{
        const formData: FormData = new FormData();
        formData.append('fileKey', fileToUpload, fileToUpload.name);
        formData.append('datasource',ds)
        formData.append('category',cat)
        return this.httpClient
          .post<File>(this.endpoint + "ai4dm/api/upload/", formData, { 
              
            })
            .pipe(
                catchError(this.handleError)
            );
    }



    get_param_from_url(url){
        var idx:number;
        idx = url.lastIndexOf("/")+1;
    
        return url.substring(idx,url.length);
    }

    set_heads(result){
     
        var h = Object.keys(result[0]);       
        this.heads = h.filter(
            o => ['Airport','Country','Description'].includes(o)
        )
    }

    set_colheads(result){
        if (result == null || result.length == 0)
        {
            this.colheads= [];
        }else{
            this.colheads = Object.keys(result[0]);       
        }
        
    }

    set_aircraftheads(result){
        if (result == null || result.length == 0)
        {
            this.aircraftHeads= [];
        }else{
            this.aircraftHeads = Object.keys(result[0]);       
        }
        
    }

    get_colheads(){
        
        return this.colheads;
    }

    get_colPredictHeads(){
        
        return this.colPredictHeads;
    }

    get_aircraftHeads(){
        
        return this.aircraftHeads;
    }

    set_colPredictHeads(result){
        if (result == null || result.length ==0)
        {
            this.colPredictHeads= [];
        }else{
            this.colPredictHeads = Object.keys(result[0]);       
        }

    }

    set_aircraftPredictHeads(result){
        if (result == null || result.length ==0)
        {
            this.aircraftPredictHeads= [];
        }else{
            this.aircraftPredictHeads = Object.keys(result[0]);       
        }

    }

    set_airports(result){
        this.airports= result;
    }

    set_colAircraft(result){
        this.colaircraft= result;
    }

    set_colPredictAircraft(result){
        this.colPredictAircraft= result;
    }

    set_coordinates(m){
        this.coordinates = m
    }

    get_colDs(){
        this.colDs = new MatTableDataSource();
        return this.colDs;
    }

    get_colPredictDs(){
        this.colPredictDs = new MatTableDataSource();
        return this.colPredictDs;
    }

    get_aircraftDs(){
        this.aircraftDs = new MatTableDataSource();
        return this.aircraftDs;
    }

    get_aircraftPredictDs(){
        this.aircraftPredictDs = new MatTableDataSource();
        return this.aircraftPredictDs;
    }

    handleError(error: any): Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
     }

}