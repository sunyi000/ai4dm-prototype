import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';

@Component({
  selector: 'app-institution',
  templateUrl: './institution.component.html',
  styleUrls: ['./institution.component.css']
})
export class InstitutionComponent implements OnInit {


  label;
  type;
  region;

  inst_id;
  inst :any[]=[];

  constructor(private route: ActivatedRoute,private dataService: DataService,private helperService:HelperService) {

  }
  ngOnInit(): void {
    this.inst_id = encodeURIComponent(this.route.snapshot.paramMap.get('institution_id'))

    this.dataService.get_institution_by_id(this.inst_id).subscribe((result : any[])=>{
        this.inst = result;

        this.label =  (typeof this.inst[0]["label"] =='undefined')? "" : this.inst[0]["label"].value;
        this.type = (typeof this.inst[0]["type"] =='undefined')? "" : this.inst[0]["type"].value;
        this.region = (typeof this.inst[0]["region"] =='undefined')? "" : this.inst[0]["region"].value;

        

    });
  }

}
