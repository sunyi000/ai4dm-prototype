import { AfterViewInit, Component, OnInit,ViewChild, ViewChildren,QueryList, Query } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';


@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.css']
})
export class EventComponent implements OnInit, AfterViewInit {
  @ViewChildren(MatPaginator) paginator=new QueryList<MatPaginator>();
  @ViewChildren(MatSort) sort= new QueryList<MatSort>();


  @ViewChildren(MatPaginator) set matPaginator(mpp: QueryList<MatPaginator>) {
    this.dataService.colDs.paginator = mpp.toArray()[0];
    this.dataService.colPredictDs.paginator= mpp.toArray()[1];
    this.setDataSourceAttributesPrediction();
}

  event_id : string;
  event : any;
  elabel;
  edescription;
  ename;
  eregion;
  eventdate;
  etype;
  
 

  colDatasource;
  colPredictionDatasource;

  questionsal = [];
  questionsalobj = [];

  allEvents;

  selectedEvent;

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

    this.event_id = this.route.snapshot.paramMap.get('event_id')

    if (this.event_id)
    {

      this.displayEventInfo(this.event_id);

    }
    this.dataService.get_all_events().subscribe((result : any[])=>{
      this.allEvents = result;
    });
    
     
    this.dataService.get_event_predicates().subscribe((result : any[])=>{
      this.questionsal = result;
    });



  }

  displayEventInfo(id){
      this.dataService.get_event_by_id(id).subscribe((result : any[])=>{
      this.selectedEvent = id;
      this.event = result;

      this.ename = (typeof this.event[0]["name"] =='undefined')? "" : this.event[0]["name"].value;
      this.elabel = (typeof this.event[0]["label"] =='undefined')? "" : this.event[0]["label"].value;
      this.edescription = (typeof this.event[0]["description"] =='undefined')? "" : this.event[0]["description"].value;
      this.eventdate = (typeof this.event[0]["date"] =='undefined')? "" : this.event[0]["date"].value;
      this.etype = (typeof this.event[0]["type"] =='undefined')? "" : this.event[0]["type"].value;
      this.eregion = (typeof this.event[0]["region"] =='undefined')? "" : this.event[0]["region"].value;

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

setEvent(a){
  this.event_id = a.value
  this.displayEventInfo(a.value)
}

predictResult(q,t){

  var question = q.value;
  

  this.dataService.get_facts(this.event_id,question,t).subscribe((result : any[])=>{
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

  this.dataService.get_prediction(this.event_id,question,t).subscribe((result : any[])=>{
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
