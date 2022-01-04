import { Component, OnInit,AfterViewInit,ViewChild } from '@angular/core';
import { DataService } from '../../common/services/data.service';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { HelperService } from 'src/app/common/services/helper.service';

@Component({
  selector: 'app-airport-table',
  templateUrl: './airport-table.component.html',
  styleUrls: ['./airport-table.component.css']
})
export class AirportTableComponent implements AfterViewInit,OnInit {

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) set matPaginator(mp: MatPaginator) {
      this.paginator = mp;
      this.setDataSourceAttributes();
  }

  dataSource;
  constructor(private dataService: DataService,private helperService:HelperService){      
    this.dataSource = this.dataService.dataSource;  
    
  }

  ngOnInit(): void {

  }


  setDataSourceAttributes() {
    this.dataService.dataSource.paginator = this.paginator;

    if (this.paginator) {
      this.applyFilter('');
    }
  }
  ngAfterViewInit(){

    this.dataService.dataSource.sortingDataAccessor =(obj, property) =>{
      return obj[property].value;
    } ;

    this.dataService.dataSource.filterPredicate =  (data, filter: string) => {
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

    this.dataSource.sort = this.sort;
    this.dataSource.sortingDataAccessor = (item, property) => {
      console.log(property)
      return item[property].value;

    };
 

  }

  // showHideColumns(event){
  //    //console.log(event.source.id);
  //    if(event.checked)
  //    {
  //      console.log(this.heads);
  //      if (!(event.source.id in this.heads)){
  //        this.heads.push(event.source.id);
  //      }
  //    }else{
  //     this.heads.forEach( (item, index) => {
  //       if(item === event.source.id) this.heads.splice(index,1);
  //     });
  //      console.log(this.heads);
  //      //this.cols = this.heads;
  //    }
  // }

  applyFilter(value:string){
    this.dataService.dataSource.filter = value;
  }

  get airports():any[] {
      return this.dataService.airports;
  }

  set airports(value:any[]){        
      this.dataService.airports = value;
  }
  get heads():any[]{
      return this.dataService.heads;
  }

  set heads(value:any[]){
      this.dataService.heads = value;
  }

  get cols():any[]{
    return this.dataService.cols;
  }

  set cols(value:any[]){
    this.dataService.cols = value;
}

}
