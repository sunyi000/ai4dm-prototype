import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';

@Component({
  selector: 'app-runway',
  templateUrl: './runway.component.html',
  styleUrls: ['./runway.component.css']
})
export class RunwayComponent implements OnInit {

  runway_id;
  lighted;
  surface;
  width;
  airport_id;
  aircrafts =[];

  runway :any[]=[];

  constructor(private route: ActivatedRoute,private dataService: DataService,private helperService:HelperService) {

  }

  ngOnInit(): void {
    this.runway_id = this.route.snapshot.paramMap.get('runway_id')
    this.dataService.get_runway_by_id(this.runway_id).subscribe((result : any[])=>{
        this.runway = result;

        this.lighted = this.runway[0]["lighted"].value;
        this.surface = this.runway[0]["surface"].value;
        this.width = this.runway[0]["width"].value;
        this.airport_id = this.runway[0]["airport"].value;

        this.aircrafts = this.runway[0]["aircraft"].value.split(",")

        

    });
  }

}
