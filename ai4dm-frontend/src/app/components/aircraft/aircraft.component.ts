import { AfterViewInit, Component, OnInit,ViewChildren,QueryList } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';


@Component({
  selector: 'app-aircraft',
  templateUrl: './aircraft.component.html',
  styleUrls: ['./aircraft.component.css']
})
export class AircraftComponent implements OnInit, AfterViewInit {

  @ViewChildren(MatPaginator) paginator=new QueryList<MatPaginator>();
  @ViewChildren(MatSort) sort= new QueryList<MatSort>();


  @ViewChildren(MatPaginator) set matPaginator(mpp: QueryList<MatPaginator>) {
    this.dataService.colDs.paginator = mpp.toArray()[0];
    this.dataService.colPredictDs.paginator= mpp.toArray()[1];
    this.setDataSourceAttributesPrediction();
}

  aircraft_id : string;
  aircraft : any[];
  model : any;
  manufacturer;
  engine_count;
  wingtip;
  approach_speed;
  wingspan;
  length;
  tail_height;
  mtow;
  max_ramp;
  gear_config;
  icao;
  wake_cat;
  parking_area;
  physical_class

  aircraftDatasource;
  aircraftPredictionDatasource;

  questions = [];
  questionsobj = [];

  allAircraft = [];
  pagename;

  selectedQuestion;
  selectedQuestionobj;

  selectedAircraft;

  constructor(private route: ActivatedRoute,private dataService: DataService) {
    this.aircraftDatasource = this.dataService.get_colDs();
    this.aircraftPredictionDatasource = this.dataService.get_colPredictDs();
   }

  ngOnInit(): void {
    this.aircraft_id = this.route.snapshot.paramMap.get('aircraft_id')
    this.dataService.set_colheads(null);
    this.dataService.set_colPredictHeads(null);

    if(this.aircraft_id)
    {
      this.displayAircraftInfo(this.aircraft_id);
      
    }
    
    this.getAllAircraft()
    


    this.dataService.get_aircraft_predicate("subj").subscribe((result : any[])=>{
      this.questions = result;
    });

    this.dataService.get_aircraft_predicate("obj").subscribe((result : any[])=>{
      this.questionsobj = result;
    });
  }


  displayAircraftInfo(id){
    this.dataService.get_aircraft_by_id(id).subscribe((result : any[])=>{
      this.aircraft = result;
      this.selectedAircraft = id;

      this.model = this.aircraft[0]["model"].value;
      this.manufacturer = this.aircraft[0]["manufacturer"].value;
      this.engine_count = (typeof this.aircraft[0]["engine_count"] =='undefined')? "" : this.aircraft[0]["engine_count"].value;
      this.wingtip = (typeof this.aircraft[0]["wingtip"] =='undefined')? "" : this.aircraft[0]["wingtip"].value;
      this.approach_speed = (typeof this.aircraft[0]["approach_speed"] =='undefined')? "" : this.aircraft[0]["approach_speed"].value;
      this.wingspan = (typeof this.aircraft[0]["wing_span"] =='undefined')? "" : this.aircraft[0]["wing_span"].value;
      this.length = (typeof this.aircraft[0]["length"] =='undefined')? "" : this.aircraft[0]["length"].value;
      this.max_ramp = (typeof this.aircraft[0]["max_ramp"] =='undefined')? "" : this.aircraft[0]["max_ramp"].value;
      this.tail_height = (typeof this.aircraft[0]["tail_height"] =='undefined')? "" : this.aircraft[0]["tail_height"].value;
      this.mtow = (typeof this.aircraft[0]["mtow"] =='undefined')? "" : this.aircraft[0]["mtow"].value;
      this.gear_config = (typeof this.aircraft[0]["gear_config"] =='undefined')? "" : this.aircraft[0]["gear_config"].value;
      this.icao = (typeof this.aircraft[0]["icao_code"] =='undefined')? "" : this.aircraft[0]["icao_code"].value;
      this.wake_cat = (typeof this.aircraft[0]["wake_category"] =='undefined')? "" : this.aircraft[0]["wake_category"].value;
      this.parking_area = (typeof this.aircraft[0]["parking_area"] =='undefined')? "" : this.aircraft[0]["parking_area"].value;
      this.physical_class = (typeof this.aircraft[0]["physical_class"] =='undefined')? "" : this.aircraft[0]["physical_class"].value;
    });
  }
  getAllAircraft(){
    this.dataService.get_all_aircrafts().subscribe((result : any[])=>{
      this.allAircraft = result;
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

    this.aircraftDatasource.sort = this.sort.toArray()[0];
    this.aircraftDatasource.sortingDataAccessor = (item, property) => {
      return item[property].value;

    };

    this.aircraftPredictionDatasource.sort = this.sort.toArray()[1];
    this.aircraftPredictionDatasource.sortingDataAccessor = (item, property) => {
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


setAircraft(a){
  this.aircraft_id = a.value
  this.displayAircraftInfo(a.value)
}

predictResult(q,t){

  var question = q.value;
  

  this.dataService.get_facts(this.aircraft_id,question,t).subscribe((result : any[])=>{
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
      this.aircraftDatasource.paginator = this.paginator.toArray()[0];
  });

  this.dataService.get_prediction(this.aircraft_id,question,t).subscribe((result : any[])=>{
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
      this.aircraftPredictionDatasource.paginator = this.paginator.toArray()[0];
  });



}

}
