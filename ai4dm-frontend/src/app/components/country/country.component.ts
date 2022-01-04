import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';

@Component({
  selector: 'app-country',
  templateUrl: './country.component.html',
  styleUrls: ['./country.component.css']
})
export class CountryComponent implements OnInit {


  country_id;
  code;
  continent;
  wiki;

  country :any[]=[];

  constructor(private route: ActivatedRoute,private dataService: DataService,private helperService:HelperService) {

  }
  ngOnInit(): void {
    this.country_id = this.route.snapshot.paramMap.get('country_id')
    this.dataService.get_country_by_id(this.country_id).subscribe((result : any[])=>{
        this.country = result;

        this.code =  (typeof this.country[0]["country_code"] =='undefined')? "" : this.country[0]["country_code"].value;
        this.continent = (typeof this.country[0]["continent"] =='undefined')? "" : this.country[0]["continent"].value;
        this.wiki = (typeof this.country[0]["wk"] =='undefined')? "" : this.country[0]["wk"].value;

        

    });
  }

}
