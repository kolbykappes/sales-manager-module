import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface User {
  user_id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.apiUrl}/users`;

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    console.log('Fetching users from:', this.apiUrl);
    return this.http.get<User[]>(this.apiUrl, { 
      observe: 'response',
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      })
    }).pipe(
      tap(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        console.log('Response body:', response.body);
      }),
      map(response => response.body as User[])
    );
  }
}
