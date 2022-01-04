import { AfterViewInit, Component, OnInit,ViewChild, ViewChildren,QueryList, Query } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { FormControl } from '@angular/forms';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';

@Component({
  selector: 'app-airport',
  templateUrl: './airport.component.html',
  styleUrls: ['./airport.component.css']
})
export class AirportComponent implements OnInit, AfterViewInit {
  @ViewChildren(MatPaginator) paginator=new QueryList<MatPaginator>();
  @ViewChildren(MatSort) sort= new QueryList<MatSort>();


  @ViewChildren(MatPaginator) set matPaginator(mpp: QueryList<MatPaginator>) {
    this.dataService.colDs.paginator = mpp.toArray()[0];
    this.dataService.colPredictDs.paginator= mpp.toArray()[1];
    this.setDataSourceAttributesPrediction();
}

  airport_id : string;
  airport : any;
  iata;
  gps;
  mu;
  lat;
  long;
  region;
  name;
  elev;
  country;
  type;
  runway;

  colDatasource;
  colPredictionDatasource;

  questions = [];
  questionsobj = [];

  allAirports;

  selectedAirport;

  pagename;

  selectedQuestion;
  selectedQuestionobj;

  airportFilterOptions: Observable<string[]>;
  airportControl =new FormControl();

  constructor(private route: ActivatedRoute,private dataService: DataService,private helperService:HelperService) { 
    this.colDatasource = this.dataService.get_colDs();
    this.colPredictionDatasource = this.dataService.get_colPredictDs();


  }


  ngOnInit(): void {

    this.dataService.set_colheads(null);
    this.dataService.set_colPredictHeads(null);

    this.airport_id = this.route.snapshot.paramMap.get('airport_id')

    if (this.airport_id)
    {

      this.displayAiportInfo(this.airport_id);

    }
    
    this.allAirports=this.dataService.airports;
     
    this.dataService.get_airport_predicate_by_airport("subj").subscribe((result : any[])=>{
      this.questions = result;
    });

    this.dataService.get_airport_predicate_by_airport("obj").subscribe((result : any[])=>{
      this.questionsobj = result;
    });

  }

  displayAiportInfo(id){
    this.selectedAirport = id;
    for (var i=0; i<this.dataService.airports.length; i++){
      if(this.dataService.airports[i]["Airport"].value==id){
        this.airport = this.dataService.airports[i];
      }

    }
    this.iata = this.airport["IATA"].value;
    this.gps = this.airport["GPS_Code"].value;
    this.lat = this.airport["Latitude"].value;
    this.long = this.airport["Longitude"].value;
    this.region = this.airport["Region_Served"].value;
    this.name = this.airport["Description"].value;
    this.elev = this.airport["Elevation"].value;
    this.country = this.airport["Country"].value;
    this.mu = this.airport["Municipality"].value;
    this.type = this.airport["Type"].value;
    this.runway  = this.airport["Runway"].value;
  }
  setDataSourceAttributesPrediction() {
    if ( this.paginator.toArray()[0]) {
      this.applyFilter('');
    }

    if ( this.paginator.toArray()[1]) {
      this.applyFilterPrediction('');
    }
  }


  ngAfterViewInit() {
    this.colDatasource.filterPredicate =  (data, filter: string) => {
      const transformedFilter = filter.trim().toLowerCase();
    
      const listAsFlatString = (obj): string => {
        let returnVal = '';
    
        Object.values(obj).forEach((val) => {
          if (typeof val !== 'object') {
            returnVal = returnVal + ' ' + val;
          } else if (val !== null) {
            returnVal = returnVal + ' ' + listAsFlatString(val);
          }
        });
    
        return returnVal.trim().toLowerCase();
      };
    
      return listAsFlatString(data).includes(transformedFilter);
    };

    this.colPredictionDatasource.filterPredicate =  (data, filter: string) => {
      const transformedFilter = filter.trim().toLowerCase();
    
      const listAsFlatString = (obj): string => {
        let returnVal = '';
    
        Object.values(obj).forEach((val) => {
          if (typeof val !== 'object') {
            returnVal = returnVal + ' ' + val;
          } else if (val !== null) {
            returnVal = returnVal + ' ' + listAsFlatString(val);
          }
        });
    
        return returnVal.trim().toLowerCase();
      };
    
      return listAsFlatString(data).includes(transformedFilter);
    };

    this.colDatasource.sort = this.sort.toArray()[0];
    this.colDatasource.sortingDataAccessor = (item, property) => {
      return item[property].value;

    };

    this.colPredictionDatasource.sort = this.sort.toArray()[1];
    this.colPredictionDatasource.sortingDataAccessor = (item, property) => {
      return item[property].value;

    };

  }

get colheads():any[]{
    return this.dataService.get_colheads();
}

set colheads(value:any[]){
    this.dataService.colheads = value;
}

get colpheads():any[]{
  return this.dataService.colPredictHeads;
}

set colpheads(value:any[]){
  this.dataService.colPredictHeads = value;
}


applyFilter(value:string){
  this.dataService.colDs.filter = value;
}

applyFilterPrediction(value:string){
  this.dataService.colPredictDs.filter = value;
}

setAirport(a){
  this.airport_id = a.value
  this.displayAiportInfo(a.value)
}

predictAircraftByAirport(q,t){

  var question = q.value;
  

  this.dataService.get_facts(this.airport_id,question,t).subscribe((result : any[])=>{
      this.dataService.colaircraft = result;
      this.dataService.set_colheads(this.dataService.colaircraft)
      this.dataService.set_colAircraft(this.dataService.colaircraft);

      this.dataService.colDs.data = this.dataService.colaircraft;
      if(result !=null && result.length>0)
      {
        this.dataService.colcols=Object.keys(result[0])
        let pname:string = result[0]["obj"].value
        this.pagename = pname.split("-")[0]
      }

      this.colDatasource.paginator = this.paginator.toArray()[0];

  });

  this.dataService.get_prediction(this.airport_id,question,t).subscribe((result : any[])=>{
      // this.dataService.colPredictAircraft = result;
      this.dataService.colPredictAircraft =result.filter(x=> !this.dataService.colaircraft.some(exclude =>exclude['obj'].value ===x['obj'].value));
      this.dataService.set_colPredictHeads(this.dataService.colPredictAircraft)
      this.dataService.set_colPredictAircraft(this.dataService.colPredictAircraft);
  
      this.dataService.colPredictDs.data = this.dataService.colPredictAircraft;
      if(result !=null && result.length>0)
      {
          this.dataService.colpcols=Object.keys(result[0])
          var pname = result[0]["obj"].value
          this.pagename = pname.split("-")[0]
      }
      
    
    this.colPredictionDatasource.paginator = this.paginator.toArray()[1];
  });

  

}


}
