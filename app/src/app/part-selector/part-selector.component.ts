import { Component, OnInit, ViewChild } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { ComponentsService } from "./../components.service";
import { Observable, Subscription } from "rxjs";
import { startWith, map, first } from "rxjs/operators";
import { MatAutocompleteModule } from "@angular/material/autocomplete";
import {
  FormArray,
  ReactiveFormsModule,
  FormControl,
  FormsModule
} from "@angular/forms";

@Component({
  selector: 'app-part-selector',
  templateUrl: './part-selector.component.html',
  styleUrls: ['./part-selector.component.css']
})

export class PartSelectorComponent implements OnInit {
  @ViewChild('PartName') inputName
  myControl = new FormControl();
  components: string[] = [];
  partData;
  filteredComponens: Observable<string[]>;
  componentsSubscription: Subscription;

  @Output() selectedPartNumber = new EventEmitter<string>();
  constructor(private componentsService: ComponentsService) {
    this.componentsService
      .getComponents()
        .pipe(first())
          .toPromise().then(components => {
            this.components = components;
            this.filteredComponens = this.myControl.valueChanges.pipe(
            startWith(""),
            map(value => this._filter(value))
          );
        });


  }

  handleClearBox()
  {
    // this.inputName.nativeElement.value = ' ';
    this.myControl.setValue('');
    this.selectedComponent('');
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.components.filter(option =>
      option.toLowerCase().includes(filterValue)
    );
  }

  selectedComponent(PN: string) {
    this.selectedPartNumber.emit(PN)
  }

  ngOnInit() {
    this.componentsService
      .getComponents()
        .subscribe(components => {
            this.components = components;
            this.filteredComponens = this.myControl.valueChanges.pipe(
            startWith(""),
            map(value => this._filter(value))
          );
        });
  }
  

}
