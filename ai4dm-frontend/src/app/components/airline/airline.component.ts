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
  selector: 'app-airline',
  templateUrl: './airline.component.html',
  styleUrls: ['./airline.component.css']
})
export class AirlineComponent implements OnInit, AfterViewInit {
  @ViewChildren(MatPaginator) paginator=new QueryList<MatPaginator>();
  @ViewChildren(MatSort) sort= new QueryList<MatSort>();


  @ViewChildren(MatPaginator) set matPaginator(mpp: QueryList<MatPaginator>) {
    this.dataService.colDs.paginator = mpp.toArray()[0];
    this.dataService.colPredictDs.paginator= mpp.toArray()[1];
    this.setDataSourceAttributesPrediction();
}

  airline_id : string;
  airline : any;
  callsign;
  foundedDate;
  netIncome;
  fleetSize;
  icao;
  country;
  description;
 

  colDatasource;
  colPredictionDatasource;

  questionsal = [];
  questionsalobj = [];

  allAirlines;

  selectedAirline;

  pagename;

  selectedQuestion;
  selectedQuestionobj;


  constructor(private route: ActivatedRoute,private dataService: DataService) { 
    this.colDatasource = this.dataService.get_colDs();
    this.colPredictionDatasource = this.dataService.get_colPredictDs();


  }


  ngOnInit(): void {

    this.dataService.set_colheads(null);
    this.dataService.set_colPredictHeads(null);

    this.airline_id = this.route.snapshot.paramMap.get('airline_id')

    if (this.airline_id)
    {

      this.displayAirlineInfo(this.airline_id);

    }
    this.dataService.get_all_airlines().subscribe((result : any[])=>{
      this.allAirlines = result;
    });
    
     
    this.dataService.get_airline_predicate("subj").subscribe((result : any[])=>{
      this.questionsal = result;
    });

    this.dataService.get_airline_predicate("obj").subscribe((result : any[])=>{
      this.questionsalobj = result;
    });

  }

  displayAirlineInfo(id){
      this.dataService.get_airline_by_id(id).subscribe((result : any[])=>{
      this.selectedAirline = id;
      this.airline = result;

      this.callsign = (typeof this.airline[0]["callsign"] =='undefined')? "" : this.airline[0]["callsign"].value;
      this.foundedDate = (typeof this.airline[0]["foundedDate"] =='undefined')? "" : this.airline[0]["foundedDate"].value;
      this.netIncome = (typeof this.airline[0]["netIncome"] =='undefined')? "" : this.airline[0]["netIncome"].value;
      this.fleetSize = (typeof this.airline[0]["fleetSize"] =='undefined')? "" : this.airline[0]["fleetSize"].value;
      this.icao = (typeof this.airline[0]["icaoCode"] =='undefined')? "" : this.airline[0]["icaoCode"].value;
      this.country = (typeof this.airline[0]["country"] =='undefined')? "" : this.airline[0]["country"].value;
      this.description = (typeof this.airline[0]["description"] =='undefined')? "" : this.airline[0]["description"].value;
      this.country = (typeof this.airline[0]["country"] =='undefined')? "" : this.airline[0]["country"].value;
    });
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

setAirline(a){
  this.airline_id = a.value
  this.displayAirlineInfo(a.value)
}

predictResult(q,t){

  var question = q.value;
  

  this.dataService.get_facts(this.airline_id,question,t).subscribe((result : any[])=>{
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

  this.dataService.get_prediction(this.airline_id,question,t).subscribe((result : any[])=>{
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
