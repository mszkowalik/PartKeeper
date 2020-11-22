import { Injectable } from "@angular/core";
import { environment } from "./../environments/environment";
import { HttpClient } from "@angular/common/http";
import { Observable, Subject } from "rxjs";

@Injectable()
export class ComponentsService {
  componentsSubscription = new Subject<string[]>();
  partSubscription = new Subject<any>();
  components: string[];
  selectedPart: string;
  constructor(private http: HttpClient) {
    this.components;
    // this.getPartsList();
    // this.getPart("");
  }
  getComponents(): Observable<string[]> {
    this.getPartsList()
    return this.componentsSubscription.asObservable();
  }
  getPartInfo(): Observable<string[]> {
    return this.partSubscription.asObservable();
  }

  setSelectedPart(PN: string) {
    this.selectedPart = PN;
    this.getPart(this.selectedPart);
  }

  setStock(partData:any)
  {
    // console.info(partData);
    const formData = new FormData();
    formData.append("PartNumber", partData['Part Number']);
    formData.append("Box", partData['Box']);
    formData.append("Stock", partData['Stock']);

    this.http
      .post(environment.apiUrl + "/adjust_stock", formData)
        .subscribe((data: string[]) => {
          this.componentsSubscription.next(data)
        });
 
  }
  private getPartsList() {
    this.http
      // .get(environment.apiUrl + "/getPartsList")
      .get("api/getPartsList")
      .subscribe((data: string[]) => {
        this.componentsSubscription.next(data);
        this.components = data;
        console.info("Here")
      });
  }
  private getPart(partNumber: string) {
    const formData = new FormData();
    formData.append("PartNumber", partNumber);
    // this.http
    //   .post(environment.apiUrl + "/getPart", formData)
    //   .subscribe((data: any) => {
    //     this.partSubscription.next(data);
    //   });
  }
}
