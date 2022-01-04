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
  selector: 'app-person',
  templateUrl: './person.component.html',
  styleUrls: ['./person.component.css']
})
export class PersonComponent implements OnInit, AfterViewInit {
  @ViewChildren(MatPaginator) paginator=new QueryList<MatPaginator>();
  @ViewChildren(MatSort) sort= new QueryList<MatSort>();


  @ViewChildren(MatPaginator) set matPaginator(mpp: QueryList<MatPaginator>) {
    this.dataService.colDs.paginator = mpp.toArray()[0];
    this.dataService.colPredictDs.paginator= mpp.toArray()[1];
    this.setDataSourceAttributesPrediction();
}
  person_id : string;
  person : any;
  name;
 

  colDatasource;
  colPredictionDatasource;

  questionsal = [];
  questionsalobj = [];

  allPersons;

  selectedPerson;

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

    this.person_id = this.route.snapshot.paramMap.get('person_id')

    if (this.person_id)
    {

      this.displayPersonInfo(this.person_id);

    }
    this.dataService.get_all_persons().subscribe((result : any[])=>{
      this.allPersons = result;
    });
    
     
    this.dataService.get_person_predicate("subj").subscribe((result : any[])=>{
      this.questionsal = result;
    });

    this.dataService.get_person_predicate("obj").subscribe((result : any[])=>{
      this.questionsalobj = result;
    });

  }

  decodeComponent(c)
  {
    return decodeURIComponent(c)
  }
  displayPersonInfo(id){
      this.dataService.get_person_by_id(id).subscribe((result : any[])=>{
      this.selectedPerson = id;
      this.person = result;

      this.name = (typeof this.person[0]["name"] =='undefined')? "" : this.person[0]["name"].value;

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

setPerson(a){
  this.person_id = a.value
  this.displayPersonInfo(a.value)
}

predictResult(q,t){

  var question = q.value;
  

  this.dataService.get_facts(this.person_id,question,t).subscribe((result : any[])=>{
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

  this.dataService.get_prediction(this.person_id,question,t).subscribe((result : any[])=>{
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
