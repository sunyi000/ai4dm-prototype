import { Component, OnInit,ViewChildren,QueryList, AfterViewInit } from '@angular/core';
import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-flight',
  templateUrl: './flight.component.html',
  styleUrls: ['./flight.component.css']
})
export class FlightComponent implements OnInit,AfterViewInit {
  @ViewChildren(MatPaginator) paginator=new QueryList<MatPaginator>();
  @ViewChildren(MatSort) sort= new QueryList<MatSort>();


  @ViewChildren(MatPaginator) set matPaginator(mpp: QueryList<MatPaginator>) {
    this.dataService.colDs.paginator = mpp.toArray()[0];
    this.dataService.colPredictDs.paginator= mpp.toArray()[1];
    this.setDataSourceAttributesPrediction();
}

flight_id;
flight;

flightno;
flightType;
stops;

colDatasource;
colPredictionDatasource;

questions = [];
questionsobj = [];

allFlights = [];
pagename;

selectedQuestion;
selectedQuestionobj;

selectedFlight;

  constructor(private route: ActivatedRoute,private dataService: DataService) { 
    this.colDatasource = this.dataService.get_colDs();
    this.colPredictionDatasource = this.dataService.get_colPredictDs();
  }

  ngOnInit(): void {
    this.flight_id = this.route.snapshot.paramMap.get('flight_id')
    this.dataService.set_colheads(null);
    this.dataService.set_colPredictHeads(null);

    if(this.flight_id)
    {
      this.displayFlightInfo(this.flight_id);
      
    }
    
    this.getAllFlights()
    


    this.dataService.get_flight_predicate("subj").subscribe((result : any[])=>{
      this.questions = result;
    });

    this.dataService.get_flight_predicate("obj").subscribe((result : any[])=>{
      this.questionsobj = result;
    });
  }

  displayFlightInfo(id){
    this.dataService.get_flight_by_id(id).subscribe((result : any[])=>{
      this.flight = result;
      this.selectedFlight = id;

      this.flightno = (typeof this.flight[0]["flight_no"] =='undefined')? "" : this.flight[0]["flight_no"].value;
      this.flightType = (typeof this.flight[0]["flight_type"] =='undefined')? "" : this.flight[0]["flight_type"].value;
      this.stops = (typeof this.flight[0]["stops"] =='undefined')? "" : this.flight[0]["stops"].value;

    });
  }
  getAllFlights(){
    this.dataService.get_all_flights().subscribe((result : any[])=>{
      this.allFlights = result;
    });
  }

  sortingDataAccessor(item, property) {
    if (property.includes('.')) {
      return property.split('.')
        .reduce((object, key) => object[key], item);
    }
    return item[property];
  }

  setDataSourceAttributesPrediction() {
    if ( this.paginator.toArray()[0]) {
      this.applyFilter('');
    }

    if ( this.paginator.toArray()[1]) {
      this.applyFilterPrediction('');
    }
  }

  ngAfterViewInit():void{
    this.dataService.colPredictDs.sortingDataAccessor =(obj, property) =>{
      return obj[property].value;
    } ;

    this.dataService.colDs.filterPredicate =  (data, filter: string) => {
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

    this.dataService.colPredictDs.filterPredicate =  (data, filter: string) => {
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


setFlight(a){
  this.flight_id = a.value
  this.displayFlightInfo(a.value)
}

predictResult(q,t){

  var question = q.value;
  

  this.dataService.get_facts(this.flight_id,question,t).subscribe((result : any[])=>{
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

  this.dataService.get_prediction(this.flight_id,question,t).subscribe((result : any[])=>{
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
