import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';

@Component({
  selector: 'app-region',
  templateUrl: './region.component.html',
  styleUrls: ['./region.component.css']
})
export class RegionComponent implements OnInit {


  region_id;
  code;
  continent;
  country;
  wiki;

  region :any[]=[];

  constructor(private route: ActivatedRoute,private dataService: DataService,private helperService:HelperService) {

  }
  ngOnInit(): void {
    this.region_id = this.route.snapshot.paramMap.get('region_id')
    this.dataService.get_region_by_id(this.region_id).subscribe((result : any[])=>{
        this.region = result;

        this.code =  (typeof this.region[0]["region_code"] =='undefined')? "" : this.region[0]["region_code"].value;
        this.continent = (typeof this.region[0]["continent"] =='undefined')? "" : this.region[0]["continent"].value;
        this.wiki = (typeof this.region[0]["wk"] =='undefined')? "" : this.region[0]["wk"].value;
        this.country = (typeof this.region[0]["country"] =='undefined')? "" : this.region[0]["country"].value;

        

    });
  }

}
