import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges, OnChanges } from '@angular/core';
import { FormGroup, FormBuilder, FormArray } from "@angular/forms";
import { ComponentsService } from "./../components.service";
import { first } from "rxjs/operators";
import { Injectable } from '@angular/core';
import { NgModule } from '@angular/core';


@Component({
  selector: 'app-part-viewer',
  templateUrl: './part-viewer.component.html',
  styleUrls: ['./part-viewer.component.css']
})
export class PartViewerComponent implements OnInit, OnChanges {

  @Input() part:string;
  @Input() mode:string;
  @Output() EditedPartData = new EventEmitter<string>();
  
  partData;
  constructor(private componentsService: ComponentsService, private fb: FormBuilder) { }


  ngOnInit() {
  }
  save() {
    this.EditedPartData.emit(this.partData)
  }

  getObjectProperties():string[] 
  {
    let ret : string[]=[];
    for(let prop in this.partData){
      if ((prop === 'Box' || prop === 'Stock') && this.mode == 'adjustStock')
      {
        ret.push(prop);
      }
      else if (this.mode != 'adjustStock')
      {
        ret.push(prop);
      }
      
    }

    return ret;
  }


  ngOnChanges(changes: SimpleChanges){
    if(this.part!= ''){
      this.componentsService.setSelectedPart(this.part)
    this.componentsService
    .getPartInfo().pipe(first())
    .toPromise().then(data=>{
      this.partData = data;    
    });
    }
    else {
      this.partData = []
    }
    
  }

}
